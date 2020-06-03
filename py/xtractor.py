import os
import sys

from py.helpers import getWorkingFolder

"""
extracting archives 1 y 1 using 7zip executable installed in the OS
command line parameters for 7zip.exe: " x -o* ", i.e. extract and create directory with the name of source archive
"""
#path to 7Zip x64 bits executable
str7ZipExecFile = "C:\\Program Files\\7-Zip\\7z.exe"
# variable to store consumable string to execute in shell
str7ZipSysExecPath = "" # will be set further after we are sure executable exists

#folder where we expecting all the archives to be stored
strFilesFolder = ""
# func checks if 7Zip executable exists in the system and sets variable for 7Zip execution from shell
def extractorSysCheck():
    global str7ZipSysExecPath
    if os.path.isfile(str7ZipExecFile):
        print(f"Executable file {str7ZipExecFile} exists. Proceeding to next step.")
        str7ZipSysExecPath = "\"" + str7ZipExecFile + "\""
        return True
    else:
        print(f"Executable file {str7ZipExecFile} does not exist. Please install x64 bits version of 7Zip archiver and restart")
        return False
        quit()

def debugMove(strFilesFolder):
    for root, dirs, files in os.walk(strFilesFolder):
        if not os.path.exists(strFilesFolder+"\\done"):
            os.mkdir(strFilesFolder+"\\done")
        for file in files:
            if ("debug_" in file):
                os.replace(root+"\\"+file, root+"\\done\\"+file)
        break

# extract files from .Z archives, move Z archives and archives with "debug" string in file name to done folder
# we have no use for debug files so no further extraction for them is needed
def extractAndMove(str7ZipSysExecPath, strFilesFolder, listStrToExtract, strHowToExtract):
    if strHowToExtract == "here":
        strCmdLineZ = " x -o" + strFilesFolder + " "
    elif strHowToExtract == "subfolder":
        strCmdLineZ = " x -o" + strFilesFolder + "\\* "
    # traversing the strFileFolders for all files that contain "Collection" in their names
    #first pass is to extract all .Z files as they are archives with tar inside and we need tar to be extracted
    for root, dirs, files in os.walk(strFilesFolder):
        for file in files:
            # if ("tar.Z" in file) or ("tar.bz2" in file):
            #     print(f"Processing {root}\\{file}")
            #     os.system(str7ZipSysExecPath + strCmdLineZ + root + "\\" + file)
            #     os.replace(root + "\\" + file, root + "\\done\\" + file)
            for testSubstring in listStrToExtract:
                if testSubstring in file:
                    print(f"Processing {root}\\{file}")
                    os.system(str7ZipSysExecPath + strCmdLineZ + root + "\\" + file)
                    os.replace(root + "\\" + file, root + "\\done\\" + file)
        break
#
"""
Now runnig the scripts
"""
if extractorSysCheck():
    strFilesFolder = getWorkingFolder(strFilesFolder)
    debugMove(strFilesFolder)
    extractAndMove(str7ZipSysExecPath, strFilesFolder, [".tar.Z", ".tar.bz"], "here")
    extractAndMove(str7ZipSysExecPath, strFilesFolder, [".tar"], "subfolder")