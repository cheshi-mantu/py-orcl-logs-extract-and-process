#THIS TO BE REWRITTEN FULLY

import os
import sys
"""
constants
"""
constForReading = "r"
"""
______________________________________________________________________
>>>>>>>>>>> 2 type A: virtual machine
Machine Name=ddmdbp1
Operating System Name=HP-UX
Operating System Release=B.11.31
=== Processor information ====
+ /usr/sbin/ioscan -fkC processor
Class       I  H/W Path  Driver    S/W State   H/W Type     Description
========================================================================
processor   0  120       processor   CLAIMED     PROCESSOR    Processor
processor   1  121       processor   CLAIMED     PROCESSOR    Processor
processor   2  122       processor   CLAIMED     PROCESSOR    Processor
processor   3  123       processor   CLAIMED     PROCESSOR    Processor
processor   4  124       processor   CLAIMED     PROCESSOR    Processor
processor   5  125       processor   CLAIMED     PROCESSOR    Processor
processor   6  126       processor   CLAIMED     PROCESSOR    Processor
processor   7  127       processor   CLAIMED     PROCESSOR    Processor
processor   8  128       processor   CLAIMED     PROCESSOR    Processor
processor   9  129       processor   CLAIMED     PROCESSOR    Processor
+ /usr/bin/getconf MACHINE_MODEL
ia64 hp server Integrity Virtual Machine
+ /usr/contrib/bin/machinfo
CPU info:  <<<<<<<<<<<<<<<<< Marker #1
   Intel(R)  Itanium(R)  Processor 9560 (2.53 GHz, 32 MB)
   1 core, 1 logical processor per socket
   6.38 GT/s QPI, CPU version D0
          Active processor count: <<<<<<<<<<<<<<<< Marker #2
          10 sockets
          10 cores
_________________________________________________________________________          
>>>>>>>>> 2 type B: virtual machine
Machine Name=ddmdbp1
Operating System Name=HP-UX
Operating System Release=B.11.31
=== Processor information ====
+ /usr/sbin/ioscan -fkC processor
Class       I  H/W Path  Driver    S/W State   H/W Type     Description
========================================================================
processor   0  120       processor   CLAIMED     PROCESSOR    Processor
processor   1  121       processor   CLAIMED     PROCESSOR    Processor
processor   2  122       processor   CLAIMED     PROCESSOR    Processor
processor   3  123       processor   CLAIMED     PROCESSOR    Processor
processor   4  124       processor   CLAIMED     PROCESSOR    Processor
processor   5  125       processor   CLAIMED     PROCESSOR    Processor
processor   6  126       processor   CLAIMED     PROCESSOR    Processor
processor   7  127       processor   CLAIMED     PROCESSOR    Processor
+ /usr/bin/getconf MACHINE_MODEL
ia64 hp server Integrity Virtual Machine
+ /usr/contrib/bin/machinfo
CPU info:
  8 Intel(R) Itanium 2 9100 series processors (1.59 GHz, 9 MB)
          266 MHz bus, CPU version A1
______________________________________________________________________          
"""
def cpuInfoPhysicalServer(strFileName):
    targetHeaders = ["FileName","Machine Name", "Operating System Name","Operating System Release","Processor", "model name", "cpu cores",
                          "physical id", "siblings"]

    lstSearchForPhysicalSrv = ["FileName", "Machine Name", "Operating System Name","Operating System Release","processor", "model name", "cpu cores",
                          "physical id", "siblings"]
    lstSearchForVM_A = ["FileName", "Machine Name", "Operating System Name", "Operating System Release", "processor:", "model name", "cpu cores"]
    lstSearchForVM_B = ["FileName", "Machine Name", "Operating System Name", "Operating System Release", "processor:", "model name", "cpu cores" ]
    strFileName = "X:\\Oracle\\Latvia\\Collection-apolon1.dnb.lv_DB\\CPUQ\\apolon1.dnb.lv-ct_cpuq.txt"
    def getFileContent(strFullPath):
        """
        Returns a list containing information  information omitting script information
        Replaces "=" with ":" \n
        Replaces tabs with nothing \n
        Replaces ": " with ":" \n
        Adds file name to 1st position of the list \n
        :param strFullPath: Path to a file to read
        :return: list with all strings, 1 element of the list is 1 string from the file
        """
        fileContent = []
        f = open(strFullPath,constForReading) #open file for reading
        fileContent = f.read().splitlines() #read full file and send it content spitted in lines to a list
        f.close() #close file (atta boy!)
        fileContent = fileContent[fileContent.index("[END SCRIPT INFO]")+1:] #find [END SCRIPT INFO] marker and cut file as we don't need the script info at all
        fileContent = [s.replace("\t", "") for s in fileContent] # replace all TAB chars with empty strings
        fileContent = [s.replace(": ", ":") for s in fileContent] #replace : followed by space by just :
        fileContent = [s.replace("=", ":") for s in fileContent] #replace all = sign with : so it will be easier to process
        fileContent.insert(0,"FileName:" + strFileName.split("\\")[-1]) #add file name to 1st position in list
        return fileContent
    #
    #

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
