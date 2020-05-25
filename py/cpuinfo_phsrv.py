import os
import sys

"""
>>>>>>>>>>> 1 type: physical server
Machine Name=d1lt-ddmdb01 <<<<<<<<< collect to 1st record of dict
Operating System Name=Linux  <<<<<<<<<<<< collect and combine with next 2ns record of dict
Operating System Release=3.8.13-98.7.1.el7uek.x86_64 <<<<<<<<<<< collect and combine with previous - add to 2nd record of dict
+ cat /proc/cpuinfo <<<<<<<<<< marker
processor	: 0 <<<<<<<<<<<<<< collect and count each next if does not exist in dic then add and assign = 1, then add for each new rec
model name	: Intel(R) Xeon(R) CPU E5-2667 v4 @ 3.20GHz <<<<<<<<<<<<< collect once = 3rd record of dict
physical id	: 0 <<<<<<<<<<<<<<<< consider add to 4th record and count each next if does not exist in dic then add and assign = 1, then add for each new rec
siblings	: 3 <<<<<<<<<<<<<<<< collect take the value and add to the 4th record and then sum with next ones
core id		: 0 <<<<<<<<<<<<<<<< collect and count to 5th record
cpu cores	: 3 <<<<<<<<<<<<<<<< collect and sum to 6th record
"""
def getFileContent(strFullPath):
    """
    Returns a list containing lines from the file omitting script information
    Replaces "=" with ":" \n
    Replaces tabs with nothing \n
    Replaces ": " with ":" \n
    Adds file name to 1st position of the list \n
    :param strFullPath: Path to a file to read
    :return: list with all strings, 1 element of the list is 1 string from the file
    """
    fileContent = []
    f = open(strFullPath, constForReading)  # open file for reading
    fileContent = f.read().splitlines()  # read full file and send it content spitted in lines to a list
    f.close()  # close file (atta boy!)
    fileContent = fileContent[fileContent.index(
        "[END SCRIPT INFO]") + 1:]  # find [END SCRIPT INFO] marker and cut file as we don't need the script info at all
    fileContent = [s.replace("\t", "") for s in fileContent]  # replace all TAB chars with empty strings
    fileContent = [s.replace(": ", ":") for s in fileContent]  # replace : followed by space by just :
    fileContent = [s.replace("=", ":") for s in
                   fileContent]  # replace all = sign with : so it will be easier to process
    fileContent.insert(0, "FileName:" + strFileName.split("\\")[-1])  # add file name to 1st position in list
    return fileContent


def cpuInfoPhysicalServer(strFileName):
    lstSearchForPhysicalSrv = ["FileName", "Machine Name", "Operating System Name","Operating System Release","processor", "model name", "cpu cores",
                          "physical id", "siblings"]
    # constant
    constForReading = "r"
    #
    #CAREFULLY WITH THIS ONE
    #NEEDS TO BE COMMENTED BEFORE NORMAL USAGE
    #strFileName = "X:\\Oracle\\Latvia\\Collection-apolon1.dnb.lv_DB\\CPUQ\\apolon1.dnb.lv-ct_cpuq.txt"

    lstServerData = {} #store server data here in this dict
    strLines = getFileContent(strFileName) #file content
    for item in lstSearchForPhysicalSrv:
        lstResults = [i for i in strLines if item in i]
        print (lstResults)
        for itemLine in lstResults:
            tmpLst = itemLine.split(":")
            if "processor" in tmpLst[0]:
                lstServerData[tmpLst[0]] = len(lstResults)
            else:
                if tmpLst[0] in lstServerData:
                    if tmpLst[1].isdigit():
                        lstServerData[tmpLst[0]] += int(tmpLst[1])
                    else:
                        if tmpLst[1] == lstServerData[tmpLst[0]]:
                            pass
                        else:
                            lstServerData[tmpLst[0]] += tmpLst[1]
                else:
                    if tmpLst[1].isdigit():
                        lstServerData[tmpLst[0]] = int(tmpLst[1])
                    else:
                        lstServerData[tmpLst[0]] = tmpLst[1]
    return lstServerData
