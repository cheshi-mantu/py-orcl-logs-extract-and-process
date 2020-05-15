main 
'====================================================================
Sub main ()
'WScript.Echo Now
Dim objFS, objStartFolder, objFolder, objFile, objShell, objLogFile, arrListFilesList
Dim strFoderPath
Dim str7ZipExecFile
' path to 64 bits 7 zip archiver executable
' 2DO: check if the executable exists and throw the message to download and install 7zip 64 bits executable 
str7ZipExecFile = get7zipPath()
'str7ZipExecFile = "C:\Program Files\7-Zip\7z.exe"
Dim strCommandLineOptions
Set arrListFilesList = CreateObject("System.Collections.ArrayList")
Set objShell = CreateObject("Shell.Application")
' 1 select folder with files
' 1.1 if there are files, then first walk through all files and extract
' 1.2 highest level archive files will be moved to folder "done"
' 2 1st pass extract all the data from ech file to the folder with intial file name
' 3 2nd pass through all the folders, check if there is any file in folder with ".tar", extract data from each .tar 
' creting file system object to select starting folder with archve files

Set objFS = CreateObject("Scripting.FileSystemObject")
	strFolderPath = selectFolder("Select folder with archives")
	
	If Len(strFolderPath) > 1 Then  
' assign starting folder to foder object
		Set objStartFolder = objFS.getFolder(strFolderPath)
	Else
		MsgBox "You haven't selected any folder" & vbCrLf & _
		"Script now will exit. Please restart", _ 
		vbOKOnly, "Error"
		Exit sub		
	End If
	' check if folder "done" exists in the starting folder
' if "done" does not exist, then create one
	If Not objFS.FolderExists (strFolderPath+"\done\") Then
		objFS.CreateFolder (strFolderPath+"\done\")
	End If 

' If in starting folder there are files, add full paths to list array for further moving to "done folder"
' then execute the extraction 
	If objStartFolder.Files.Count > 0 Then
		For Each item In objStartFolder.Files
			If InStr(item.Path, "xls") = 0 Then
				arrListFilesList.add(item.Path)
			End If
		Next

' create command line options parameter
		strCommandLineOptions = "x -o* " + Chr(34) + objStartFolder.Path + "\*.*" + Chr(34)
		debug.WriteLine strCommandLineOptions
' execute extraction with command line options
		objShell.ShellExecute str7ZipExecFile, strCommandLineOptions, objStartFolder.Path, "", 1
	End If
' Msg box is needed as script does not know if all files are extracted
' maybe there is a way to check if 7zip is running or not, but not now
MsgBox "Please press OK only if no windows are open", vbOKOnly, "READ the message below!!!"
'remember to ignore "done" folder while traversing the subfolders
' move all processed files to "done" folder
	For Each item In arrListFilesList
		Set objFile = objFS.GetFile(Item)
		objFile.Move objStartFolder.Path + "\done\"
	Next	
' clear array list object for storing paths to archives in subfolders
arrListFilesList.Clear
' scanning the subfolders with number of files more than 0 except "done" folder
	For Each objSubFolder In objStartFolder.SubFolders
		If (objSubFolder.Files.Count > 0) And (InStr(objSubFolder.Name, "done") = 0) Then
			'creating list of tar files than will be deleted after 7zip extraction completed
			For Each tarfile In objSubFolder.Files
				If instr(tarfile.Name, ".tar") > 0 Then
					arrListFilesList.Add(tarfile.Path)
				End If	
			Next
			' create command line parameters string for specific folder
			' this bitch requires commas if there are spaces
			strCommandLineOptions = "x " + Chr(34) +  objSubFolder.Path + "\\*.tar" + Chr(34)
 			' execute extraction with 7Zip
			objShell.ShellExecute str7ZipExecFile, strCommandLineOptions, objSubFolder.Path, "", 1
		End If 	
	Next
' MSG box is needed as script does not know if all 7zip operations finished
MsgBox "Please press OK only if no windows are open", vbOKOnly, "READ the message below!!!"
' removing archives with extracted files
	For Each item In arrListFilesList
		Set objFile = objFS.GetFile(Item)
		objFile.Delete
	Next	
End sub
'function for folder selection
'no exceptions handling here
'updated 20200423 to handle if Esc/Cancel is pressed
Function selectFolder (strMsg)
Dim objShell, objFolder
Set objShell  = CreateObject( "Shell.Application" )
Set objFolder = objShell.BrowseForFolder( 0, strMsg, 0, 17 )
	If Not (objFolder is Nothing) Then
		selectFolder = objFolder.Self.Path
		Debug.WriteLine objFolder.Self.Path
	Else 
		Debug.WriteLine "No folder is selected, making the path to empty string"
		selectFolder = ""	
	End If
'cleanup
Set objShell = Nothing
end Function
'-------------------------------------------------------------------

Function get7zipPath ()
Const ForReading = 1, ForWriting = 2, ForAppending = 8, strStdPath = "C:\Program Files\7-Zip\7z.exe"
Dim objFS, objTXTSettingsFile, str7zipPath, strFolderPath, objShell
str7zipPath = ""
Set objFS = CreateObject("Scripting.FileSystemObject")

	'check if 7zip path is already known (file "7zippath.inf" must exist)  
	If objFS.FileExists ("7zippath.inf") Then
			If objFS.GetFile("7zippath.inf").Size > 0 Then 
				Set objTXTSettingsFile = objFS.OpenTextFile("7zippath.inf", ForReading, 1, -2)
				str7zipPath = objTXTSettingsFile.ReadLine
				objTXTSettingsFile.Close
				Debug.WriteLine str7zipPath
			End if
	Else 
		firstRun()
		'if does not exist then create and open for writing
		Set objTXTSettingsFile = objFS.OpenTextFile("7zippath.inf", ForWriting, 1, -2)
		
		If objFS.FileExists (strStdPath) Then
			objTXTSettingsFile.WriteLine(strStdPath)
			objTXTSettingsFile.Close
		Else
			strFolderPath  = selectFolder("Please select FOLDER where you have installed 7Zip archiver")
			If strFolderPath <> "" Then
				str7zipPath = strFolderPath + "\7z.exe"	
				objTXTSettingsFile.WriteLine(str7zipPath)
				objTXTSettingsFile.Close
			Else
				objTXTSettingsFile.Close
				MsgBox "You haven't selected right folder, please consider visiting https://www.7-zip.org," + vbCrLf + _
				"download and install 64bit version of 7zip" + vbCrLf + _
				"I'm going to open 7-zip main web page", _
				vbOKOnly, "Errrrror"
				Set objShell = CreateObject("WScript.Shell")
	   				iURL = "https://www.7-zip.org/"
	   				objShell.run(iURL)
   				Set objShell = Nothing
			End If
		End If 
	End If
Set objFS = Nothing
Set objTXTSettingsFile = Nothing
get7zipPath = str7zipPath
End Function
'------------------------------------------------------------------
Sub firstRun()
MsgBox "It seems you're running this script first time." + vbCRLF + _
"Here is the information you need to know:" + vbCRLF + _
"0) Save the archive you received to a local directory on your PC" + vbCRLF + _ 
"1) Extract all the files from the single archive you've got to some directory." + vbCRLF + _
"2) Continue this script execution. You have to install 7zip archiver (64bits version preferably) to extract the files" + vbCRLF + _
"3) If you installed 7Zip to default folder, then nothing to be updated script will find it automaticlly." + vbCRLF + _
"4) if you installed 32bits version or used custom path, you'll need to specify the installed directory." + vbCRLF + _
"5) then show the script where your files are located" + vbCRLF + _
"6) that's pretty much it." , vbOKOnly, "First run detected"


End Sub
