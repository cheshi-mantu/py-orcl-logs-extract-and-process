import os
import sys
"""
Machine Name=d1lt-ddmdb01 <<<<<<<<< collect to 1st record of dict
Operating System Name=Linux  <<<<<<<<<<<< collect and combine with next 2ns record of dict
Operating System Release=3.8.13-98.7.1.el7uek.x86_64 <<<<<<<<<<< collect and combine with previous - add to 2nd record of dict

+ cat /proc/cpuinfo <<<<<<<<<< marker
processor	: 0 <<<<<<<<<<<<<< collect and count each next if does not exist in dic then add and assign = 1, then add for each new rec
model name	: Intel(R) Xeon(R) CPU E5-2667 v4 @ 3.20GHz <<<<<<<<<<<<< collect once = 3rd record of dict
physical id	: 0 <<<<<<<<<<<<<<<< consider add to 4th record and count each next if does not exist in dic then add and assign = 1, then add for each new rec
siblings	: 3 <<<<<<<<<<<<<<<< collect take the value and add to the 4th record and then sum with next ones
core id		: 0 <<<<<<<<<<<<<<<< collect anc count to 5th record
cpu cores	: 3 <<<<<<<<<<<<<<<< collect and sum to 6th record
1 type: physical server
2 type: virtual machine
"""


