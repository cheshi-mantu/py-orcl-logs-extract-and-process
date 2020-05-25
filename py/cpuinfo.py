import os
import sys
import xtractor
"""
constants
"""
constForReading = "r"
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
targetHeaders = ["FileName","Machine Name", "Operating System Name","Operating System Release","Processor", "model name", "cpu cores",
                      "physical id", "siblings", "core id"]

lstSearchForPhysicalSrv = ["FileName", "Machine Name", "Operating System Name","Operating System Release","processor:", "model name", "cpu cores",
                      "physical id", "siblings", "core id"]
lstSearchForVM_A = ["FileName", "Machine Name", "Operating System Name", "Operating System Release", "processor:", "model name", "cpu cores",
                    ]
lstSearchForVM_B = ["FileName", "Machine Name", "Operating System Name", "Operating System Release", "processor:", "model name", "cpu cores",
                    ]
strFileName = "C:\\code\\lmnr\\cpu_only\\d1lt-ddmdb01-ct_cpuq.txt"
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
    f = open(strFullPath,constForReading)
    fileContent = f.read().splitlines()
    f.close()
    fileContent = fileContent[fileContent.index("[END SCRIPT INFO]")+1:]
    fileContent = [s.replace("\t", "") for s in fileContent]
    fileContent = [s.replace(": ", ":") for s in fileContent]
    fileContent = [s.replace("=", ":") for s in fileContent]
    fileContent.insert(0,"FileName:" + strFileName.split("\\")[-1])

    return fileContent
lstServerData = {}
strLines = getFileContent(strFileName)
for line in strLines:
    print(line)
    for item in lstSearchForPhysicalSrv:
        lstResults = [i for i in strLines if item in i]
        print (lstResults)
        #print (lstResults)
        if ":" in lstResults[0]:
            tmpLst = lstResults[0].split(":")
            if tmpLst[0] in lstServerData:
                if tmpLst[1].isdigit():
                    lstServerData[tmpLst[0]] += int(tmpLst[1])
                else:
                    lstServerData[tmpLst[0]] += tmpLst[1]
            else:
                if tmpLst[1].isdigit():
                    lstServerData[tmpLst[0]] = 1
                else:
                    lstServerData[tmpLst[0]] = tmpLst[1]

             tmpLst = lstResults