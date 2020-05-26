#helpers.py
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