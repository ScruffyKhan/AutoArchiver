DXOTAMLSAutoArchiver(R) version 1.0 07/25/2019

GENERAL USAGE NOTES
-----------------------

-	This Script takes in several different inputs for directory paths and archives the
   	folders/files inside based off of the names containing a specific string pattern that represents 
   	the month and year that the file was created in. It then zips the files together into monthly zips 
   	and archives them into the specified folder.

- 	The variable DELETE_FILES can be set to: 
	0 to keep all files that are being archived. 
	or 1 to delete all files after they are archived.

-	The PATH_TO_ENVIRONMENT variable is the path to the environment that you want to archive.

-	The ENVIRONMENT variable is prefixed to the zip name and the zip name is created using the path leading to the file and the month and year the file
	represents. I.E. all files that match the pattern for 03-2019 and are located in the DEV environment at /Input/Party/Filtered would get archived into
	a zip file named DEVInputPartyFiltered-03-2019.zip.

-	The script works by searching for patterns in 3 different manners:
	It searches for folders located using the PATH_TO_FOLDERS variable and archives them based off of the PATTERN_DATE_FOR_FOLDERS variable.
	It searches for .txt/.csv files located using the PATH_TO_TXT/PATH_TO_CSV variables and archives them based off of the PATTERN_DATE_FOR_FILES variable.


- 	The ZIP_LOCATION is the path where all archived files will be placed.


---------------------------------------------------------------------------------------------------------------------------------------------------------------

Running the script
-------------------


-	The script has been verified to run on python version 2.6.6 and above and can be run using the python scriptname syntax.

===============================================================================================================================================================

Contacts:

Developer:		Elliot Carter
Developer Contact: ecarter1117@gmail.com	
