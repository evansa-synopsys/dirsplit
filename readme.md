Modify the configuration file conf/scan.properties and add the following Black Duck information (required): 
bdURL=<URL-To-BD-Host>
bdAPIToken=<BD_API_TOKEN>
bdProjectName=<Target_Project_Name>
bdProjectVersion=<Target_Project_Version>

usage: ps-scan.py [-h] -d TARGET_DIRECTORY [-s SIZE] [-r REFRESH]
                  [-c CONFIG_FILE]

A python script that splits a large directory into subdirectories and calls BD
Detect on each of them

optional arguments:
  -h, --help            show this help message and exit
  -d TARGET_DIRECTORY, --target-directory TARGET_DIRECTORY
                        Absolute path to directory containing source files to
                        be split
  -s SIZE, --size SIZE  Size limit in bytes. Default is 2000000000B or 2GB
  -r REFRESH, --refresh REFRESH
                        delete generated subdirectories if they exist
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        Name of config file to use. Default is
                        scan.properties.
