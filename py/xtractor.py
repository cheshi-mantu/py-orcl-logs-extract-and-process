import os
import sys
"""
extracting archives 1 y 1 using 7zip executable installed in the OS
command line parameters for 7zip.exe: " x -o* ", i.e. extract and create directory with the name of source archive
"""
#path to 7Zip x64 bits executable
str7ZipExecFile = "C:\\Program Files\\7-Zip\\7z.exe"
# variable to store consumable string to execute in shell
str7ZipSysExecPath = "" # will be set furteher after we are sure executable exists

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

def getWorkingFolder(strFilesFolder):
    while strFilesFolder == "":
        strFilesFolder = input("Please paste the path to the folder with all archives you have: ")
        if strFilesFolder == "exit":
            print ("User aborted the script. Quitting.")
            quit()
        if os.path.exists(strFilesFolder):
            break
        else:
            strFilesFolder = ""
            print("If you want to exit this script, you can type \"exit\"")
    print(f"We'll proceed with files from {strFilesFolder}")
    return strFilesFolder

# extract files from .Z archives, move Z archives and archives with "debug" string in file name to done folder
# we have no use for debug files so no further extraction for them is needed
def extractZandMove(str7ZipSysExecPath, strFilesFolder):
    strCmdLineZ = " x -o" + strFilesFolder + " "
    # traversing the strFileFolders for all files that contain "Collection" in their names
    #first pass is to extract all .Z files as they are archives with tar inside and we need tar to be extracted
    for root, dirs, files in os.walk(strFilesFolder):
        for file in files:
            if ("Collection" in file) and ("tar.Z" in file):
                print(f"Processing {root}\\{file}")
                os.system(str7ZipSysExecPath + strCmdLineZ + root + "\\" + file)
    # move all .Z files and Debug archives to done folder
    # Debug files have no practival use at the moment
    for root, dirs, files in os.walk(strFilesFolder):
        if not os.path.exists(strFilesFolder+"\\done"):
            os.mkdir(strFilesFolder+"\\done")
        for file in files:
            if ("ebug" in file) or ("tar.Z" in file):
                os.replace(root+"\\"+file, root+"\\done\\"+file)
        break
def extractTarsAndMove(str7ZipSysExecPath, strFilesFolder):
    #command line for 7Zip executable for tar archives extraction
    strCmdLine = " x -o" + strFilesFolder + "\\* "
    #second pass: extracting data from tar files
    # #traverse 1st level of the os.walk
    for root, dirs, files in os.walk(strFilesFolder):
        for file in files:
            if "Collection" in file:
                print(f"Processing {root}\\{file}")
                os.system(str7ZipSysExecPath + strCmdLine + root + "\\" + file)
                os.replace(root + "\\" + file, root + "\\done\\" + file)
        break
"""
Now runnig the scripts
"""
if extractorSysCheck():
    strFilesFolder = getWorkingFolder(strFilesFolder)
    extractZandMove(str7ZipSysExecPath, strFilesFolder)
    extractTarsAndMove(str7ZipSysExecPath, strFilesFolder)


