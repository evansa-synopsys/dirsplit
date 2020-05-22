#!/usr/bin/env python
#
# Requirements
#  * Python 2.7
#
import argparse
import os
import sys
import subprocess
import re

parser = argparse.ArgumentParser(
    description='A python script that splits a large directory into subdirectories and calls BD Detect on each of them')
parser.add_argument('-d', '--target-directory', required=True,
                    help='Absolute path to directory containing source files to be split')
parser.add_argument('-s', '--size', default=2000000000, help='Size limit in bytes. Default is 2000000000B or 2GB')
parser.add_argument('-r', '--refresh', default=True, help='delete generated subdirectories if they exist')
parser.add_argument('-c', '--config-file', default='scan.properties',
                    help='Name of config file to use. Default is scan.properties.')

arguments = parser.parse_args()
rootDir = os.path.dirname(os.path.realpath(__file__))
confFile = os.path.join(rootDir, "conf", arguments.config_file)
print("root dir = " + rootDir)
print("confFile = " + confFile)

dirsplit = '.\\dirsplit.py'

if arguments.refresh:
    for fileName in os.listdir(rootDir):
        if os.path.isfile(fileName) and fileName.startswith('chunk-'):
            print("removing %s " % fileName)
            os.remove(fileName)

sys.argv = [dirsplit, arguments.target_directory, arguments.size, rootDir]

execfile(dirsplit)

# for each chunk-* in rootDir
# pass it to detect for a scan
bdURL = ""
bdAPIToken = ""
bdProjectName = ""
bdProjectVersion = ""

# get the configuration from scan.properties
with open(confFile, "r") as cf:
    for line in cf:
        if line.startswith('bdURL'):
            bdURL = line.split("bdURL=")[1]
            print("bdURL=%s" % bdURL)
        elif line.startswith('bdAPIToken='):
            bdAPIToken = line.split("bdAPIToken=")[1]
            print("bdAPIToken=%s" % bdAPIToken)
        elif line.startswith("bdProjectName="):
            bdProjectName = line.split("bdProjectName=")[1]
            print("bdProjectName=%s" % bdProjectName)
        elif line.startswith("bdProjectVersion="):
            bdProjectVersion = line.split("bdProjectVersion=")[1]
            print("bdProjectVersion=%s" % bdProjectVersion)
        else:
            break

detectCommand = '--blackduck.url={0} --blackduck.api.token={1} --blackduck.trust.cert=true --detect.project.name={2} --detect.project.version.name={3} --detect.source.path={4}\\chunk- --detect.code.location.name={2}_{3}_chunk-_code --detect.bom.aggregate.name={2}_{3}_chunk-_PKG --detect.excluded.detector.types=ALL'.format(
    bdURL.strip(), bdAPIToken.strip(), bdProjectName.strip(), bdProjectVersion.strip(), rootDir)

# Make sure you can run powershell scripts (it is disabled by default).
for fileName in os.listdir(rootDir):
    if os.path.isfile(fileName) and fileName.startswith('chunk-'):
        detectScriptPath = "%s\\detect.ps1" % rootDir
        detectCommand = re.sub("(chunk-\d*)", fileName, detectCommand)
        print('passing detectCommand to detect script= %s' % detectCommand)
        p = ["java", "-jar", "synopsys-detect-6.2.1.jar"]
        p.extend(detectCommand.split())
        # p = subprocess.Popen(["powershell.exe", detectScriptPath, detectCommand], stdout=sys.stdout)
        s = subprocess.Popen(p, shell=True)
        s.wait()