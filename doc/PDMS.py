# This script compiles the SimplifiedSkeletonLibrary for release and debug
########################################
repo='SimplifiedSkeletonLibrary'
######################################

print('Compiling: ' + repo)
import sys
import subprocess
import os
import shutil

filepath = os.path.dirname(os.path.realpath(__file__))
repo_dir=filepath + '\\..'
build_dir=filepath + '\\..\\build'
install_dir=filepath + '\\..\\install'

# Delete install folder
if os.path.isdir(install_dir):
	#shutil.rmtree(install_dir, ignore_errors=False, onerror=None)
    for i in range(3):
        try:
            shutil.rmtree(install_dir, ignore_errors=False, onerror=None)
            print("Deleting Install folder succeeded")
        except:
            print("Deleting Install folder failed")

# Configure project with Cmake (dynamic)
os.chdir(build_dir)
cmakeCmd = ['cmake.exe',  '-D' , repo + '_LINK_TYPE:STRING=dynamic', '-G', 'Visual Studio 12 2013 Win64', repo_dir]
subprocess.call(cmakeCmd)

# Build project 
os.system(r'devenv ' + build_dir + '\\' + repo + '.sln /project INSTALL /build Debug')
os.system(r'devenv ' + build_dir + '\\' + repo + '.sln /project INSTALL /build Release')

# Configure project with Cmake (static)
os.chdir(build_dir)
cmakeCmd = ['cmake.exe',  '-D' , repo +'_LINK_TYPE:STRING=static', '-G', 'Visual Studio 12 2013 Win64', repo_dir]
subprocess.call(cmakeCmd)

# Build project 
os.system(r'devenv ' + build_dir + '\\' + repo + '.sln /project INSTALL /build Debug')
os.system(r'devenv ' + build_dir + '\\' + repo + '.sln /project INSTALL /build Release')
