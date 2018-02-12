
macro(main)
	cmake_minimum_required(VERSION 3.7.2)
	

	get_directory_name()

	include("${DIRECTORY_NAME}ConfigVersion.cmake")	
	include("${DIRECTORY_NAME}Config.cmake")
	
	project(${PROJECT_NAME})
	
	set_compiler()

	set_variables()
	
	set_directories()
	
	set_options()
	
	set_flags()

	create_project(${PROJECT_NAME} ${PROJECT_SOURCE_DIR})
	
	set_environment_paths()
	
	#create_installer(${PROJECT_NAME})
endmacro()

macro(get_directory_name)
	get_filename_component(DIRECTORY_NAME ${CMAKE_SOURCE_DIR} NAME)
endmacro()

macro(set_variables)
	set(Release_KEYWORD optimized)
	set(Release_LOWER_CASE release)
	set(Release_UPPER_CASE RELEASE)
	set(Release_CONFIGURATION_DIR ${COMPILER}/release/${ARCHITECTURE}/${${PROJECT_NAME}_LINK_TYPE}/${${PROJECT_NAME}_THREADS})
	set(Debug_KEYWORD debug)
	set(Debug_LOWER_CASE debug)
	set(Debug_UPPER_CASE DEBUG)
	set(Debug_CONFIGURATION_DIR ${COMPILER}/debug/${ARCHITECTURE}/${${PROJECT_NAME}_LINK_TYPE}/${${PROJECT_NAME}_THREADS})
	set(dynamic_UPPER_CASE DYNAMIC)
	set(static_UPPER_CASE STATIC)
endmacro()

macro(set_directories)
	include(GNUInstallDirs)
		
	set_include_directories()
	
	set_build_directories()
	
	set_install_directory()
	
	# Set directory from target to find the test project based on that path. (If path does not exist, the test project is not added to the solution
	set(${PROJECT_NAME}_DIR ${PROJECT_SOURCE_DIR})
	
endmacro()

macro(set_include_directories)
	include_directories(
		${PROJECT_SOURCE_DIR}
		${PROJECT_SOURCE_DIR}/src
		${PROJECT_SOURCE_DIR}/include
	)
endmacro()

macro(set_build_directories)
	set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/build) # necessary for Windows
	set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/build)
	set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/build)
endmacro()

macro(set_install_directory)
	if (CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
		set (CMAKE_INSTALL_PREFIX "${CMAKE_SOURCE_DIR}/install" CACHE PATH "default install path" FORCE )
	endif()
endmacro()

macro(set_compiler)
	if(NOT MSVC)
		message(FATAL_ERROR "Only Visual Studio is currently supported." )
	endif()
	if(MSVC_VERSION EQUAL 1700)
		set(COMPILER "vc110")
		set(COMPILER_VERSION "11.0")
	elseif(MSVC_VERSION EQUAL 1800)
		set(COMPILER "vc120")
		set(COMPILER_VERSION "12.0")
	elseif(MSVC_VERSION EQUAL 1900)
		set(COMPILER "vc140")
		set(COMPILER_VERSION "14.0")
	endif() 
endmacro()

macro(set_architecture TARGET_NAME)
	if (NOT DEFINED ARCHITECTURE OR ARCHITECTURE STREQUAL "")
		if (NOT ${ARGV1} STREQUAL "")
			set(ARCHITECTURE ${ARGV1})
		else()
			if (DEFINED CMAKE_SYSTEM_PROCESSOR)
				if(CMAKE_SYSTEM_PROCESSOR STREQUAL "AMD64")
					set(ARCHITECTURE "x64")
				else()
					set(ARCHITECTURE "x86")
				endif()
			else()
				set(ARCHITECTURE "x64")
			endif()
		endif()
	endif()
	message(STATUS "${TARGET_NAME} architecture: ${ARCHITECTURE}")
endmacro()

macro(set_options)
	option(${PROJECT_NAME}_COPY_DEPENDENCIES_TO_INSTALL_DIRECTORY "Copy header files to install directory?" OFF)
endmacro()

macro(set_flags)
	set_compiler_flags()

	set_linker_flags()
	
	#add_definitions(/D_VARIADIC_MAX=10)
endmacro()

macro(set_compiler_flags)
	if (NOT MSVC)
		set(CMAKE_CXX_FLAGS "-Wall") # -std=c++11 is specified where needed
		set(CMAKE_CXX_FLAGS_DEBUG "-g3 -O0")
		set(CMAKE_CXX_FLAGS_RELEASE "-O3")
	else (NOT MSVC)
		add_definitions(-DBOOST_ALL_NO_LIB)
		# DO NOT ENABLE THIS IN CASE OF USING CUDA RELATED FUNCTIONS! (cannot be compiled then because compiler flags seem to change something else also):
		# set(CMAKE_CXX_FLAGS_DEBUG "/DEBUG /Od")
		# set(CMAKE_CXX_FLAGS_RELEASE "/Ox")
	endif (NOT MSVC)
endmacro()

macro(set_linker_flags)
	if (${PROJECT_NAME}_LINK_TYPE STREQUAL static)
		string(REPLACE "/MD" "/MT" CMAKE_CXX_FLAGS_RELEASE ${CMAKE_CXX_FLAGS_RELEASE})
		string(REPLACE "/MDd" "/MTd" CMAKE_CXX_FLAGS_DEBUG ${CMAKE_CXX_FLAGS_DEBUG})
	endif()
endmacro()

macro(create_project TARGET_NAME TARGET_SOURCE_DIR)

	get_header_files(${TARGET_NAME} ${TARGET_SOURCE_DIR})
	
	get_source_files(${TARGET_NAME} ${TARGET_SOURCE_DIR})
	
	if(${TARGET_NAME}_TARGET STREQUAL Application)
		create_application(${TARGET_NAME} ${TARGET_SOURCE_DIR})
	elseif(${TARGET_NAME}_TARGET STREQUAL Library)
		create_library(${TARGET_NAME} ${TARGET_SOURCE_DIR})
	else()
		message(FATAL_ERROR "Please set the type in ${TARGET_NAME}'s Config.cmake to Application or Library" )
	endif()
	
	add_libraries(${TARGET_NAME})
	
	if (EXISTS ${${TARGET_NAME}_DIR}/src/test/${TARGET_NAME}TestConfig.cmake)
		option(${TARGET_NAME}_ADD_TEST_PROJECT "Add test project for ${TARGET_NAME}?" ON)
		if(${TARGET_NAME}_ADD_TEST_PROJECT)
			create_test_project(${TARGET_NAME})
		endif()
	endif()
	
	install_target(${TARGET_NAME})
	
	#create_config_files(${TARGET_NAME} ${TARGET_SOURCE_DIR})
endmacro()

macro(get_header_files TARGET_NAME TARGET_SOURCE_DIR)
	file(GLOB ${TARGET_NAME}_HEADERS ${TARGET_SOURCE_DIR}/*.h ${TARGET_SOURCE_DIR}/src/*.h ${TARGET_SOURCE_DIR}/include/*.h, 
	${TARGET_SOURCE_DIR}/*.hpp ${TARGET_SOURCE_DIR}/src/*.hpp ${TARGET_SOURCE_DIR}/include/*.hpp)
endmacro()

macro(get_source_files TARGET_NAME TARGET_SOURCE_DIR)
	file(GLOB ${TARGET_NAME}_SOURCES ${TARGET_SOURCE_DIR}/*.cpp ${TARGET_SOURCE_DIR}/src/*.cpp ${TARGET_SOURCE_DIR}/*.py ${TARGET_SOURCE_DIR}/src/*.py)
endmacro()

macro(create_application TARGET_NAME TARGET_SOURCE_DIR)
	add_executable(${TARGET_NAME} "${${TARGET_NAME}_HEADERS}" ${${TARGET_NAME}_SOURCES})
endmacro()

macro(create_library TARGET_NAME TARGET_SOURCE_DIR)
	
	if(${TARGET_NAME}_SOURCES STREQUAL "")
		add_library(${TARGET_NAME} INTERFACE)
		target_include_directories(${TARGET_NAME} INTERFACE ${TARGET_SOURCE_DIR})
		target_sources(${TARGET_NAME} INTERFACE ${${TARGET_NAME}_HEADERS})
	else()
		if(${${TARGET_NAME}_LINK_TYPE} STREQUAL dynamic)
			set(${TARGET_NAME}_TYPE SHARED)
		else()
			set(${TARGET_NAME}_TYPE STATIC)
		endif()
		#add_library(${TARGET_NAME} ${${TARGET_NAME}_TYPE} ${${TARGET_NAME}_HEADERS} ${${TARGET_NAME}_SOURCES})
		add_library(${TARGET_NAME} STATIC ${${TARGET_NAME}_HEADERS} ${${TARGET_NAME}_SOURCES})
	endif()
	set(${TARGET_NAME}_LIBRARIES ${TARGET_NAME})
endmacro()

macro(add_libraries TARGET_NAME)
	foreach(DEPENDENCY ${${TARGET_NAME}_DEPENDENCIES})
		if (TARGET ${DEPENDENCY})
			target_link_libraries(${TARGET_NAME} ${DEPENDENCY})
		else()
			if (DEFINED ${DEPENDENCY}_HEADERS)
				foreach(HEADER ${${DEPENDENCY}_HEADERS})
					string(FIND ${HEADER} "${CMAKE_INSTALL_INCLUDEDIR}/" INDEX)
					string(LENGTH "${CMAKE_INSTALL_INCLUDEDIR}/" LENGTH)
					math(EXPR INDEX "${INDEX} + ${LENGTH}")
					string(SUBSTRING ${HEADER} 0 ${INDEX} HEADER_INCLUDE_PATH)
					include_directories(${${DEPENDENCY}_DIR}/${HEADER_INCLUDE_PATH})
				endforeach()
			endif()
			if (DEFINED ${DEPENDENCY}_LIBS)
				foreach(LIB ${${DEPENDENCY}_LIBS})
					target_link_libraries(${TARGET_NAME} ${${DEPENDENCY}_DIR}/${LIB})
				endforeach()
			endif()
			
			if (EXISTS "${${DEPENDENCY}_DIR}/info")
				add_prebuilt_dependency(${TARGET_NAME} ${DEPENDENCY})
			else()
				set(${DEPENDENCY}_DIR_CACHE ${${DEPENDENCY}_DIR})
				find_package(
					${DEPENDENCY}
					${${DEPENDENCY}_VERSION}
					COMPONENTS ${${DEPENDENCY}_COMPONENTS}
					QUIET
					MODULE
				)
				if(${${DEPENDENCY}_FOUND})
					include_directories(${${DEPENDENCY}_INCLUDE_DIRS})
					target_link_libraries(${TARGET_NAME} ${${DEPENDENCY}_LIBRARIES})
				else()
					find_package(
						${DEPENDENCY}
						${${DEPENDENCY}_VERSION}
						COMPONENTS ${${DEPENDENCY}_COMPONENTS}
						QUIET
						CONFIG
					)
					if(${${DEPENDENCY}_FOUND})
						include_directories(${${DEPENDENCY}_INCLUDE_DIRS})
						create_project(${DEPENDENCY} "${${DEPENDENCY}_DIR}")
						target_link_libraries(${TARGET_NAME} ${${DEPENDENCY}_LIBRARIES})
					else()
						set(${DEPENDENCY}_DIR ${${DEPENDENCY}_DIR_CACHE})
					endif()
				endif()
			endif()
		endif()
	endforeach(DEPENDENCY)
endmacro()

# Add prebuild library to the project
macro(add_prebuilt_dependency TARGET_NAME DEPENDENCY)

	list(APPEND ${TARGET_NAME}_PREBUILT_DEPENDENCIES ${DEPENDENCY})				# ${TARGET_NAME}_PREBUILT_DEPENDENCIES - List of all prebuild libraries
	include_directories(${${DEPENDENCY}_DIR}/include)							# Include the prebuild include folder in the project. e.g. "C:\libs\PackageLibs\DummyLib\include"

	foreach(BUILD_TYPE ${${DEPENDENCY}_BUILD_TYPES})
			# Set CONFIGURATION_DIR for each build type
			# CONFIGURATION_DIR is the relativ path from the library directory to the lib files e.s. "vc120/debug/x64/static/multi-threaded"
		set(CONFIGURATION_DIR ${COMPILER}/${${BUILD_TYPE}_LOWER_CASE}/${ARCHITECTURE}/${${PROJECT_NAME}_LINK_TYPE}/${${DEPENDENCY}_THREADS})	

			# ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIB_DIR - Path to the folder of the lib files from library DEPENDENCY in build type BUILD_TYPE e.s. "C:\libs\PackageLibs\DummyLib\lib\vc120\debug\x64\static\"
		set(${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIB_DIR ${${DEPENDENCY}_DIR}/lib/${CONFIGURATION_DIR})		
		set(${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_BIN_DIR ${${DEPENDENCY}_DIR}/bin/${CONFIGURATION_DIR})
	endforeach()
	

	# If DEBUG_STATIC_LIBS or DEBUG_DYNAMIC_LIBS or RELEASE_DYNAMIC_LIBS or RELEASE_STATIC_LIBS are not defined in .cmake file, all libraries in the libs folder of the library are linked
	if ( (NOT ${DEPENDENCY}_DEBUG_STATIC_LIBS ) AND (NOT ${DEPENDENCY}_DEBUG_DYNAMIC_LIBS) AND (NOT ${DEPENDENCY}_RELEASE_DYNAMIC_LIBS) AND(NOT ${DEPENDENCY}_RELEASE_STATIC_LIBS))	

		foreach(BUILD_TYPE ${${DEPENDENCY}_BUILD_TYPES})							# ${DEPENDENCY}_BUILD_TYPES - List of all build types the project is build for e.g. [Debug, Release]		
		
			# Link lib files from DEPENDENCY to the project libraries (The libraries are not linked by wildcard *.lib to be able to change the individual libraries in the project)
				# BUILD_TYPE - Build type e.s. Release
				# ${BUILD_TYPE}_KEYWORD - Build type is mapped to the cmake keyword  e.s. optimized. The mapping is defined in the macro "set_variables".
			if(EXISTS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIB_DIR})
				file(GLOB DEPENDENCY_LIBS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIB_DIR}/*.lib)	
				
				# Iteration over ${DEPENDENCY_LIBS} because the command "target_link_libraries" does not work the same way with a list. All libraries in a list are linked in debug and release independent from keyword "optimized" or "debug". I don't know why! (FoB)
				foreach(LIB ${DEPENDENCY_LIBS})
					target_link_libraries(${TARGET_NAME} ${${BUILD_TYPE}_KEYWORD} ${LIB})
				endforeach()
			endif()
		endforeach()
	else()
	
		foreach(BUILD_TYPE ${${DEPENDENCY}_BUILD_TYPES})
		
			if("${${TARGET_NAME}_LINK_TYPE}" STREQUAL "static")
				
				# Add DEBUG_STATIC_LIBS
				if("${BUILD_TYPE}" STREQUAL "Debug")	
					foreach(LIB ${${DEPENDENCY}_DEBUG_STATIC_LIBS})	
						target_link_libraries(${TARGET_NAME} ${${BUILD_TYPE}_KEYWORD} ${${DEPENDENCY}_DIR}/${LIB})	
					endforeach()
				endif()
				
				# Add RELEASE_STATIC_LIBS
				if("${BUILD_TYPE}" STREQUAL "Release")					
					foreach(LIB ${${DEPENDENCY}_RELEASE_STATIC_LIBS})	
						#message(STATUS "RELEASE_STATIC_LIBSt: ${${BUILD_TYPE}_KEYWORD} ${${DEPENDENCY}_DIR}/${${DEPENDENCY}_RELEASE_STATIC_LIBS}")
						target_link_libraries(${TARGET_NAME} ${${BUILD_TYPE}_KEYWORD} ${${DEPENDENCY}_DIR}/${LIB})	
					endforeach()		
				endif()
			
			endif()
			
			if("${${TARGET_NAME}_LINK_TYPE}" STREQUAL "dynamic")

				# Add DEBUG_DYNAMIC_LIBS
				if("${BUILD_TYPE}" STREQUAL "Debug")	
					foreach(LIB ${${DEPENDENCY}_DEBUG_DYNAMIC_LIBS})	
						target_link_libraries(${TARGET_NAME} ${${BUILD_TYPE}_KEYWORD} ${${DEPENDENCY}_DIR}/${LIB})	
					endforeach()
				endif()
				
				# Add RELEASE_DYNAMIC_LIBS
				if("${BUILD_TYPE}" STREQUAL "Release")			
					foreach(LIB ${${DEPENDENCY}_RELEASE_DYNAMIC_LIBS})	
						target_link_libraries(${TARGET_NAME} ${${BUILD_TYPE}_KEYWORD} ${${DEPENDENCY}_DIR}/${LIB})	
					endforeach()
				endif()
			endif()

		endforeach()
	endif()
	
endmacro()  

macro(create_test_project TARGET_NAME)
	if (EXISTS ${${TARGET_NAME}_DIR}/src/test/${TARGET_NAME}TestConfig.cmake)
		include("${${TARGET_NAME}_DIR}/src/test/${TARGET_NAME}TestConfig.cmake")
		create_project("${TARGET_NAME}Test" "${${TARGET_NAME}_DIR}/src/test")
		target_link_libraries("${TARGET_NAME}Test" ${TARGET_NAME})
	endif()
endmacro()

macro(install_target TARGET_NAME)

	# Create info folder in install folder during installation process
	install(DIRECTORY DESTINATION ${CMAKE_INSTALL_PREFIX}/info)
	
	install_binaries(${TARGET_NAME})
	
	install_dependencies(${TARGET_NAME})
	
	# Install the doc folder into the install folder of doc folder exists
	install_doc(${TARGET_NAME})
	
	# Install all headers fron dependencies (Last command in "install_target macro" that the user can cancle the process if headers are already "Up-to-date" and install process takes a lot of time)
	install_headers(${TARGET_NAME})
	
endmacro()

# Install the doc folder into the install folder
macro(install_doc TARGET_NAME)
	if (EXISTS ${PROJECT_SOURCE_DIR}/doc)
		install(DIRECTORY "${PROJECT_SOURCE_DIR}/doc" DESTINATION "${CMAKE_INSTALL_PREFIX}")
	endif()
endmacro()

macro(install_headers TARGET_NAME)
	install(FILES ${${TARGET_NAME}_HEADERS} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
endmacro()

macro(install_binaries TARGET_NAME)
	foreach(BUILD_TYPE ${${TARGET_NAME}_BUILD_TYPES})
		install(
			TARGETS ${TARGET_NAME} 
			ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}/${${BUILD_TYPE}_CONFIGURATION_DIR}
			LIBRARY DESTINATION ${CMAKE_INSTALL_BINDIR}/${${BUILD_TYPE}_CONFIGURATION_DIR}
			RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}/${${BUILD_TYPE}_CONFIGURATION_DIR}
			ARCHIVE CONFIGURATIONS ${BUILD_TYPE}
			LIBRARY CONFIGURATIONS ${BUILD_TYPE}
			RUNTIME CONFIGURATIONS ${BUILD_TYPE}
		)
	endforeach()
endmacro()

macro(install_dependencies TARGET_NAME)
	
	if(${PROJECT_NAME}_COPY_DEPENDENCIES_TO_INSTALL_DIRECTORY)
		foreach(DEPENDENCY ${${TARGET_NAME}_PREBUILT_DEPENDENCIES})
			install_dependency_binaries(${TARGET_NAME} ${DEPENDENCY})
			install_dependency_headers(${TARGET_NAME} ${DEPENDENCY})
		endforeach()
	endif()
endmacro()

macro(install_dependency_binaries TARGET_NAME DEPENDENCY)
	
	# Install binaries in install folder
	foreach(BUILD_TYPE ${${DEPENDENCY}_BUILD_TYPES})
	
		find_dependency_binaries(${TARGET_NAME} ${DEPENDENCY} ${BUILD_TYPE})			# Collect all required header, lib files and dll files from libraries
		
		install(
			FILES ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIBS} ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_PDBS}
			DESTINATION ${CMAKE_INSTALL_LIBDIR}/${${BUILD_TYPE}_CONFIGURATION_DIR}
			CONFIGURATIONS ${BUILD_TYPE}
		)
		install(
			FILES ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_DLLS}
			DESTINATION ${CMAKE_INSTALL_BINDIR}/${${BUILD_TYPE}_CONFIGURATION_DIR}
			CONFIGURATIONS ${BUILD_TYPE}
		)
		
		install(
			FILES ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIBS}
			DESTINATION ${CMAKE_INSTALL_LIBDIR}/${${BUILD_TYPE}_CONFIGURATION_DIR}
			CONFIGURATIONS ${BUILD_TYPE}
		)
	endforeach()
	
	# Install binaries in build/${BUILD_TYPE} folder
	foreach(BUILD_TYPE ${${DEPENDENCY}_BUILD_TYPES})

		install(
			FILES ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_DLLS}
			DESTINATION ${CMAKE_BINARY_DIR}/${BUILD_TYPE}
			CONFIGURATIONS ${BUILD_TYPE}
		)

	endforeach()
	
endmacro()

macro(find_dependency_binaries TARGET_NAME DEPENDENCY BUILD_TYPE)

	# Execute if components of the dependency are specified in the .cmake file
	if(DEFINED ${DEPENDENCY}_COMPONENTS)
		# necessary?
		separate_arguments(${DEPENDENCY}_COMPONENTS)
		#
		foreach(COMPONENT ${${DEPENDENCY}_COMPONENTS})
			file(GLOB COMPONENT_LIBS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIB_DIR}/*${COMPONENT}*.lib)
			set(${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIBS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIBS} ${COMPONENT_LIBS})
			file(GLOB COMPONENT_PDBS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIB_DIR}/*${COMPONENT}*.pdb)
			set(${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_PDBS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_PDBS} ${COMPONENT_PDBS})
			file(GLOB COMPONENT_DLLS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_BIN_DIR}/*${COMPONENT}*.dll)
			set(${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_DLLS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_DLLS} ${COMPONENT_DLLS})
		endforeach()
	endif()
	
		#DEPENDENCY_BUILD_AND_LINK_TYPE - e.s. OpenCV_DEBUG_STATIC
	set(DEPENDENCY_BUILD_AND_LINK_TYPE ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_${${${TARGET_NAME}_LINK_TYPE}_UPPER_CASE})
	
	if(DEFINED ${DEPENDENCY_BUILD_AND_LINK_TYPE}_LIBS)
		foreach(DEPENDENCY_LIB ${${DEPENDENCY_BUILD_AND_LINK_TYPE}_LIBS})
			list(APPEND ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIBS ${${DEPENDENCY}_DIR}/${DEPENDENCY_LIB})
		endforeach()
		endif()
	if(DEFINED ${DEPENDENCY_BUILD_AND_LINK_TYPE}_PDBS)
		foreach(DEPENDENCY_PDB ${${DEPENDENCY_BUILD_AND_LINK_TYPE}_PDBS})
			list(APPEND ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_PDBS ${${DEPENDENCY}_DIR}/${DEPENDENCY_PDB})
		endforeach()
		endif()
	if(DEFINED ${DEPENDENCY_BUILD_AND_LINK_TYPE}_DLLS)
		foreach(DEPENDENCY_DLL ${${DEPENDENCY_BUILD_AND_LINK_TYPE}})
			list(APPEND ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_DLLS ${${DEPENDENCY}_DIR}/${DEPENDENCY_DLL})
		endforeach()
	endif()
	
	if(NOT DEFINED ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIBS)
		file(GLOB ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIBS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIB_DIR}/*.lib)
	endif()
	if(NOT DEFINED ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_PDBS)
		file(GLOB ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_PDBS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_LIB_DIR}/*.pdb)
	endif()
	if(NOT DEFINED ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_DLLS)	
		file(GLOB ${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_DLLS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_BIN_DIR}/*.dll)
	endif()
	
	list(APPEND ${PROJECT_NAME}_ENVIRONMENT_PATHS ${${DEPENDENCY}_${${BUILD_TYPE}_UPPER_CASE}_BIN_DIR})
endmacro()

macro(install_dependency_headers TARGET_NAME DEPENDENCY)
	if(("${${DEPENDENCY}_COMPONENTS}" STREQUAL "") AND ("${${DEPENDENCY}_HEADERS}" STREQUAL ""))
		install(DIRECTORY ${${DEPENDENCY}_DIR}/include DESTINATION .)
	else()
		foreach(COMPONENT ${${DEPENDENCY}_COMPONENTS})
			if(EXISTS ${${DEPENDENCY}_DIR}/include/${COMPONENT})
				install(DIRECTORY ${${DEPENDENCY}_DIR}/include/${COMPONENT} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
			endif()
					
			file(GLOB ITEMS ${${DEPENDENCY}_DIR}/include ${${DEPENDENCY}_DIR}/include/*)
			foreach(ITEM ${ITEMS})
				if(IS_DIRECTORY ${ITEM})
					if(EXISTS ${ITEM}/${COMPONENT})
						get_filename_component(ITEM_NAME ${ITEM} NAME)
						install(DIRECTORY ${ITEM}/${COMPONENT} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${ITEM_NAME})
					endif()
				endif()
			endforeach()
			
			file(GLOB COMPONENT_HEADERS ${${DEPENDENCY}_DIR}/include/*${COMPONENT}*)
			install(
				FILES ${COMPONENT_HEADERS}
				DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
			)
		endforeach()
		
		foreach(HEADER ${${DEPENDENCY}_HEADERS})
			string(FIND ${HEADER} "${CMAKE_INSTALL_INCLUDEDIR}/" INDEX REVERSE)
			string(LENGTH "${CMAKE_INSTALL_INCLUDEDIR}/" LENGTH)
			math(EXPR INDEX "${INDEX} + ${LENGTH}")
			string(SUBSTRING ${HEADER} ${INDEX} -1 HEADER_AFTER_INCLUDE)
			get_filename_component(HEADER_PATH ${HEADER_AFTER_INCLUDE} PATH)
			install(FILES ${${DEPENDENCY}_DIR}/${HEADER} DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/${HEADER_PATH})
		endforeach()
	endif()
endmacro()

macro(set_environment_paths)
	if (MSVC)
		file(
			WRITE ${PROJECT_SOURCE_DIR}/build/${PROJECT_NAME}.vcxproj.user
			"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
			"<Project ToolsVersion=\"${COMPILER_VERSION}\" xmlns=\"http://schemas.microsoft.com/developer/msbuild/2003\">\n"
			#"	<PropertyGroup Condition=\"'$(Configuration)|$(Platform)'=='Debug|${ARCHITECTURE}'\">\n"
			"	<PropertyGroup>\n"
			"		<LocalDebuggerEnvironment>PATH=${${PROJECT_NAME}_ENVIRONMENT_PATHS};%PATH% $(LocalDebuggerEnvironment)</LocalDebuggerEnvironment>\n"
			"		<DebuggerFlavor>WindowsLocalDebugger</DebuggerFlavor>\n"
			"	</PropertyGroup>\n"
			"</Project>"
		)
	endif()
endmacro()

macro(create_config_files TARGET_NAME TARGET_SOURCE_DIR)
	#set(${TARGET_NAME}_CONFIG "${CMAKE_CURRENT_BINARY_DIR}/${TARGET_NAME}Config.cmake")
	set(${TARGET_NAME}_CONFIG "${TARGET_SOURCE_DIR}/${TARGET_NAME}Config.cmake")
	configure_file(${TARGET_SOURCE_DIR}/cmake/${TARGET_NAME}Config.cmake.in  ${${TARGET_NAME}_CONFIG} @ONLY)
	#set(${TARGET_NAME}_CONFIG_VERSION "${CMAKE_CURRENT_BINARY_DIR}/${TARGET_NAME}ConfigVersion.cmake")
	set(${TARGET_NAME}_CONFIG_VERSION "${TARGET_SOURCE_DIR}/${TARGET_NAME}ConfigVersion.cmake")
	configure_file(${TARGET_SOURCE_DIR}/cmake/${TARGET_NAME}ConfigVersion.cmake.in ${${TARGET_NAME}_CONFIG_VERSION} @ONLY)
	install(
		FILES ${${TARGET_NAME}_CONFIG} ${${TARGET_NAME}_CONFIG_VERSION}
		DESTINATION ${CMAKE_INSTALL_PREFIX}
	)
endmacro()

macro(create_installer TARGET_NAME)	
	include(InstallRequiredSystemLibraries)
	set(CPACK_RESOURCE_FILE_LICENSE "${PROJECT_SOURCE_DIR}/License.txt")
	set(CPACK_PACKAGE_VERSION_MAJOR "${${TARGET_NAME}_MAJOR_VERSION}")
	set(CPACK_PACKAGE_VERSION_MINOR "${${TARGET_NAME}_MINOR_VERSION}")
	include(CPack)
endmacro()

macro(set_version TARGET_NAME)
	set(options "")
	set(oneValueArgs MAJOR_VERSION MINOR_VERSION PATCH_VERSION)
	set(multiValueArgs "")
	cmake_parse_arguments(${TARGET_NAME} "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
	set(${TARGET_NAME}_VERSION ${${TARGET_NAME}_MAJOR_VERSION}.${${TARGET_NAME}_MINOR_VERSION}.${${TARGET_NAME}_PATCH_VERSION})
	message(STATUS "${TARGET_NAME} version: ${${TARGET_NAME}_VERSION}")
	check_compatability(${${TARGET_NAME}_VERSION})
endmacro()

macro(check_compatability TARGET_VERSION)
	if("${TARGET_VERSION}" VERSION_LESS "${PACKAGE_FIND_VERSION}")
	  set(PACKAGE_VERSION_COMPATIBLE FALSE)
	else()
	  set(PACKAGE_VERSION_COMPATIBLE TRUE)
	  if ("${PACKAGE_VERSION}" VERSION_EQUAL "${PACKAGE_FIND_VERSION}")
		set(PACKAGE_VERSION_EXACT TRUE)
	  endif()
	endif()
endmacro()

macro(configure TARGET_NAME)
	if("${PROJECT_NAME}" STREQUAL "")
		set(PROJECT_NAME ${TARGET_NAME})
	endif()

	set(options MULTI_THREADED WINDOWS_EXPORT_ALL_SYMBOLS)
	set(oneValueArgs TYPE ARCHITECTURE)
	set(multiValueArgs BUILD_TYPES LINK_TYPES DEPENDENCIES DEPENDENCY_HEADERS DEPENDENCY_DEBUG_BINARIES DEPENDENCY_RELEASE_BINARIES)
	cmake_parse_arguments(CONFIGURATION	"${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})
	set_target(${TARGET_NAME} ${CONFIGURATION_TYPE})
	set_architecture(${TARGET_NAME} ${CONFIGURATION_ARCHITECTURE})
	set_build_type(${TARGET_NAME} "${CONFIGURATION_BUILD_TYPES}")
	set_link_type(${TARGET_NAME} "${CONFIGURATION_LINK_TYPES}")
	set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ${CONFIGURATION_WINDOWS_EXPORT_ALL_SYMBOLS})
	set_threads(${TARGET_NAME} ${CONFIGURATION_MULTI_THREADED})
	set_dependencies(${TARGET_NAME} "${CONFIGURATION_DEPENDENCIES}")
	set(${TARGET_NAME}_INCLUDE_DIRS ${${TARGET_NAME}_INCLUDE_DIRS} ${${TARGET_NAME}_DIR} ${${TARGET_NAME}_DIR}/src ${${TARGET_NAME}_DIR}/include)
endmacro()

macro(set_target TARGET_NAME TYPE)
	set(${TARGET_NAME}_TARGET ${TYPE})
	message(STATUS "${TARGET_NAME} type: ${TYPE}")
endmacro()

macro(set_build_type TARGET_NAME TYPES)
	set(${TARGET_NAME}_BUILD_TYPES ${TYPES})
	message(STATUS "${TARGET_NAME} build types: ${${TARGET_NAME}_BUILD_TYPES}")
endmacro()

macro(set_link_type TARGET_NAME TYPES)
	set(${TARGET_NAME}_LINK_TYPE dynamic CACHE STRING "Link type")
	set_property(CACHE ${TARGET_NAME}_LINK_TYPE PROPERTY STRINGS "${TYPES}")
	message(STATUS "${TARGET_NAME} link type: ${${TARGET_NAME}_LINK_TYPE}")
endmacro()

macro(set_threads TARGET_NAME MULTI_THREADED)
	if(${MULTI_THREADED} STREQUAL "TRUE")
		set(${TARGET_NAME}_THREADS "multi-threaded")
	else()
		set(${TARGET_NAME}_THREADS "single-threaded")
	endif()
	message(STATUS "${TARGET_NAME} multi-threaded: ${MULTI_THREADED}")
endmacro()

macro(set_dependencies TARGET_NAME DEPENDENCY_CONFIGURATIONS)
	foreach(DEPENDENCY_CONFIGURATION ${DEPENDENCY_CONFIGURATIONS})
		parse_string(
			${DEPENDENCY_CONFIGURATION}
			COMPONENTS
			HEADERS
			DEBUG_DYNAMIC_LIBS DEBUG_DYNAMIC_DLLS DEBUG_DYNAMIC_PDBS
			DEBUG_STATIC_LIBS DEBUG_STATIC_DLLS DEBUG_STATIC_PDBS
			RELEASE_DYNAMIC_LIBS RELEASE_DYNAMIC_DLLS
			RELEASE_STATIC_LIBS RELEASE_STATIC_DLLS
		)
	
		if(TARGET ${NAME})
			continue()
		endif()
		
		set(${NAME}_DIR "" CACHE PATH "${DEPENDENCY} directory")
		set(${NAME}_BUILD_TYPES "${${PROJECT_NAME}_BUILD_TYPES}")
		set(${NAME}_THREADS "${${PROJECT_NAME}_THREADS}")
		list(APPEND ${TARGET_NAME}_DEPENDENCIES ${NAME})
	endforeach()
	message(STATUS "${TARGET_NAME} dependencies: ${${TARGET_NAME}_DEPENDENCIES}")
endmacro()

# Parsing the dependencies strings and decompose string in NAME, ${NAME}_VERSION and ${NAME}_${ARGUMENT} e.s. "Boost 1.61.0 DEBUG_STATIC_LIBS lib/vc120/debug/x64/static/libboost_wserialization-vc120-mt-sgd-1_61.lib"
# is composed in NAME=Boost, Boost_VERSION=1.61.0, Boost_DEBUG_STATIC_LIBS
function(parse_string STRING)
	if(STRING STREQUAL "")
		return()
	endif()
	separate_arguments(STRING)	# Decompose the string into a list of words and put the resulting list in the string variable
	
	# Extract the library name e.s. "Boost" from the list and remove the entry in the list
	list(GET STRING 0 NAME)
	set(NAME ${NAME} PARENT_SCOPE)
	list(REMOVE_AT STRING 0)
	if(STRING STREQUAL "")
		return()
	endif()
	
	# Extract the library version number e.s. "1.61.0" from the list and remove the entry in the list
	list(GET STRING 0 VERSION)
	if (VERSION MATCHES "^([0-9]+)\\.([0-9]+)\\.([0-9]+)$")
		set(${NAME}_VERSION ${VERSION} PARENT_SCOPE)
		list(REMOVE_AT STRING 0)
	endif()
	
	# Remove all white spaces to write string over multiple lines
	foreach (ITEM ${STRING})
		string(STRIP ${ITEM} ITEM_TMP)
		LIST(APPEND STRING_TMP "${ITEM_TMP}")
	endforeach()
	set(STRING  ${STRING_TMP})
	
	foreach (ITEM ${STRING})
		list(FIND ARGN ${ITEM} INDEX)										# ARGN - Is the list of all possible configurations of a library: COMPONENTS, HEADERS, DEBUG_DYNAMIC_LIBS, DEBUG_DYNAMIC_DLLS, DEBUG_DYNAMIC_PDBS, DEBUG_STATIC_LIBS, DEBUG_STATIC_PDBS, RELEASE_DYNAMIC_LIBS, RELEASE_DYNAMIC_DLLS, RELEASE_STATIC_LIBS		
		if(INDEX EQUAL -1)
			set(${NAME}_${ARGUMENT} ${${NAME}_${ARGUMENT}} ${ITEM})
			set(${NAME}_${ARGUMENT} ${${NAME}_${ARGUMENT}} PARENT_SCOPE)
		else()
			set(ARGUMENT ${ITEM})			# Variable ARGUMENT stores the current configuration from configurations e.s. DEBUG_STATIS_LIBS
		endif()
	endforeach()

endfunction()

main()