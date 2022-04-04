from lotto import *
import os

if __name__ == "__main__":
    BackupFile()
    drwNo = 1009
    while 1:
        CmdInit()
        n = input("Input Number : ")
        os.system('cls')
        if n == '1':
            GetRandomNum()
        elif n == '2':
            drwNo = GetRecentlyNum(drwNo)
        elif n == '3':
            GetNumSortedProbabilityBase()
        elif n == '4':
            drwNo = UpdateCountFile()
        elif n == '0':
            break
        else:
            print("[Error] You just have put invalid number.\n\tPlease put valid input number.")