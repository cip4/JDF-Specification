import logging
import os
#import shutil
import sys
import time
#import pathlib
import configparser
from subprocess import call
from subprocess import Popen


# constants
FILE_RUNTIME_FM = "C:\Program Files (x86)\Adobe\AdobeFrameMaker2015\FrameMaker.exe"
FILE_RUNTIME_ETSC = "C:\Program Files (x86)\Adobe\Adobe ExtendScript Toolkit CC\ExtendScript Toolkit.exe"
FILE_ADOBE_TRUSTED_SCRIPTS = "~\Documents\Adobe Scripts"
FILE_SPEC_BUILDER_JSX = "spec-builder.jsx"
FILE_BUILD_CONFIG = "snapshot.ini"
FOLDER_TARGET = "target"
FOLDER_SOURCE = "FrameMaker"
#PROCESS_ID = "p" + str(current_milli_time())

# Configuration file access keys
KEY_CONFIG_SECTION = "build"
KEY_FILE_BOOK = "file.book"
KEY_FILE_TEMPLATE = "file.template"

COVER_TITLE = "doc.cover.title"
COVER_VERSION = "doc.cover.version"
RUNNING_TITLE = "doc.running.title"
#COVER_BANNER_1 = "doc.cover_banner_1"
#COVER_BANNER_2 = "doc.cover_banner_2"

KEY_DIR_SOURCE = "dir.source"
KEY_DIR_TARGET = "dir.target"

KEY_BUILD_FILENAME = "build.filename"
KEY_BUILD_LOCKFILE = "build.lock.file"
KEY_BUILD_FILELOG = "file.buildlog"


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging_formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(logging_formatter)
logger.addHandler(c_handler)
logger.info("Python version: " + str(sys.version_info))

# This is the primary function 
def main():

    # This is the full path to the build directory - it is the root of all evil and
    # gives all the related directories
    build_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.dirname(build_dir)
    source_dir = os.path.join(root_dir, FOLDER_SOURCE)
    target_dir = os.path.join(root_dir, FOLDER_TARGET)
    
    # Get the build 'run specific' params (Other build parameters are in the config file)
    paramConfigFile = sys.argv[1]
    paramBuildFileName = sys.argv[2]
    paramCoverVersion = sys.argv[3]
    paramBuildRunNumber = sys.argv[4]
    
    # Construct the actual build run parameters
    BuildFileName = paramBuildFileName + ".pdf"
    BuildRootName = paramConfigFile.split(".")[0]
    BuildLogFileName = BuildRootName + paramBuildRunNumber + ".log" 
    BuildLogFile = os.path.join(target_dir, BuildLogFileName)
    CoverVersion = paramCoverVersion
    
    # Define the build lock file - used to determine when the jsx file has completed
    BuildLockFileName = BuildRootName + paramBuildRunNumber + ".lck" 
    BuildLockFile = os.path.join(target_dir, BuildLockFileName)
    if os.path.isfile(BuildLockFile):
        os.remove(BuildLockFile,)
    
    # Put the local file system IO in the try/catch
    try:
        # Clean the target directory. Then (and only then) add the file handler and start logging
        cleanCreateTarget(target_dir)

        # Add a file log (uses same file as the extend script log)
        # NOTE: This file will be removed by the clean target directory... don't use until then
        f_handler = logging.FileHandler(os.path.join(target_dir, BuildLogFile))
        f_handler.setLevel(logging.INFO)
        f_handler.setFormatter(logging_formatter)
        logger.addHandler(f_handler)
        logging.info("Clean or Create build target directory: %s", target_dir)
        logging.info("Created Log File")

        # Clean the source directory of stale locks backups etc
        logging.info("Clean Framemaker source directory: %s", source_dir)
        cleanupSources(source_dir)
        
        # Update the target configuration with the build variables
        logging.info("Update target configuration")
        config = loadConfiguration(os.path.join(build_dir, paramConfigFile))
        configBuild = config[KEY_CONFIG_SECTION]
        configBuild[KEY_DIR_SOURCE] = source_dir
        configBuild[KEY_DIR_TARGET] = target_dir
        configBuild[KEY_BUILD_FILENAME] = BuildFileName
        configBuild[COVER_VERSION] = CoverVersion
        configBuild[KEY_BUILD_FILELOG] = BuildLogFile

        # Finally add a maker parameter to inform the script file that the configuration
        # file has been updated and can be trusted.
        configBuild[KEY_BUILD_LOCKFILE] = BuildLockFile
        
        # Save the updated configuration
        config_target = os.path.join(target_dir, FILE_BUILD_CONFIG)
        saveConfiguration(config, config_target)
        logging.info("Build Configuration: " + os.path.basename(config_target))
        
    except Exception as e:
        logger.error("Error preparing build environment.")
        logger.error("Exception: " + str(e))
        sys.exit()
        
    logging.info("Terminate running FrameMaker.exe if exists.")
    Popen("TASKKILL /F /IM FrameMaker.exe")
    time.sleep(5)
    
    logging.info("Start Framemaker...")
    FRAMEMAKER_PROCESS = Popen("\"" + FILE_RUNTIME_FM + "\"")
    
    PAUSE_PERIODE = 6
    logging.info("Wait for FrameMaker (%d sec.)..." % (PAUSE_PERIODE * 10))
    
    while PAUSE_PERIODE > 0:
        time.sleep(10)
        PAUSE_PERIODE -= 1
        logging.info("%d secs..." % (PAUSE_PERIODE * 10))
    
    logging.info("Start processing '" + BuildRootName + "' ...")
    logging.info("BUILD_FILENAME: " + BuildFileName)

    # start build
    src_script = os.path.join(build_dir, FILE_SPEC_BUILDER_JSX)
    dest_script = os.path.join(os.path.expanduser(FILE_ADOBE_TRUSTED_SCRIPTS), BuildRootName + ".jsx")
#    JSX_Build_Script_File = os.path.join(trustedScripts_dir, FILE_SPEC_BUILDER_JSX);
    
    logging.info("Start FrameMaker ExtendScript...")
    open(BuildLockFile, "w").close()
    runBuild(src_script, dest_script, config_target)
   
    # check running process
    while os.path.isfile(BuildLockFile):
        time.sleep(3)
    
    logging.info("Close FrameMaker...")
    FRAMEMAKER_PROCESS.terminate()
    
    # Purge build specific files 
    os.remove(dest_script)
    
    logging.info("-----------------------------")
    logging.info(" BUILD SUCCESSFUL")
    logging.info("-----------------------------")

#
# Clean up the Framemaker Sources of the JDF Specification.
#
def cleanupSources(source_dir):
    # String array of file EXTENSIONS to delete
    extensions = [".lck", ".backup.fm", ".recover.fm"]

    files = os.listdir(source_dir)
    for f in files:
        for e in extensions:
            if f.endswith(e):
                os.remove(os.path.join(source_dir, f))

#
# Clean or create the build target directory
#
def cleanCreateTarget(target_dir):    
    if os.path.isdir(target_dir):
        files = os.listdir(target_dir)
        for f in files:
            os.remove(os.path.join(target_dir, f))
    else:
        os.makedirs(target_dir)

#
# Read load and update the configuration file
def loadConfiguration(srcConfigFile):
        # Read the configuration ini file
    config = configparser.ConfigParser()
    config.sections()
    config.read(srcConfigFile)
    return config
    
def saveConfiguration(config, destfile):
    with open(destfile, 'w') as outConfigFile:
        config.write(outConfigFile, False)

#
# Run build process.
#
def runBuild(src_script, dest_script, config_file):
    # Copy and revise the source script to the trusted execution area
    fileSrc = open(src_script, "r")
    fileDest = open(dest_script, "w")

    # The only change is to provide the full path to the new configuration file
    for line in fileSrc:
        if "var FILE_CONFIG ="  in line:
            line = 'var FILE_CONFIG ="' + config_file.replace("\\", "\\\\") + '";\n'

        fileDest.write(line)

    fileSrc.close()
    fileDest.close();

    # run process
#    jsx_build_script = os.path.join(build_dir, FILE_SPEC_BUILDER_JSX)
    logging.info("Execute FrameMaker ExtendScript: " + dest_script)
    call([FILE_RUNTIME_ETSC, "-run", dest_script])

######
# Call the main function
main()
sys.exit()
