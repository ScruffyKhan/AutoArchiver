#!/usr/bin/python
#THIS NEED TO BE HERE TO PROPERLY CALL THE SCRIPT WITHOUT THE PYTHON KEYWORD
#THE COMMAND DOS2UNIX NEEDS TO BE RUN ANYTHIME THIS SCRIPT IS UPDATE ON A WINDOWS MACHINE

######################################################################################  
#   Auto Archiver - Written By: Elliot Carter
#
#   This Script takes in several different inputs for directory paths and archives the
#   folders/files inside based off of the names containing a specific string that represents 
#   the month and year that the file was created in. It then zips the files together into monthly zips 
#   and archives them into the specified folder.
#
###################################################################################### 

#Import os module
import os
import re
import glob
import shutil
import datetime
import time
import zipfile
from zipfile import ZipFile

#Days to subtract from current date
DAYS_TO_SUBTRACT = 60

#Variable to delete files after archive 0 if you DO NOT want to delete and 1 if you DO####################
DELETE_FILES = 1
################################################################################
 
#List of current PATH_TO_ENVIRONMENT############################################################
PATH_TO_ENVIRONMENT = '/usr/local/inet/shared/Thrivent_TAMLS/'
#PATH_TO_ENVIRONMENT = 'C:/TAMLSData/q_thrivent_tamls_dev/'
#Current Environment used in naming the zip file i.e. DEV, SYS, ITE, PROD
ENVIRONMENT = "ITE"
##################################################################################################

#List of all directories inside all environments with FOLDERS to zip
PATH_TO_FOLDERS = ['Input/EODPolicy/Filtered/',
                      'Input/Events/Filtered/',
                      'Input/Party/Filtered/',
                      'Input/Policy/Filtered/',
                      'Input/Relationship/Filtered/',
                      'Input/Transaction/Filtered/',
                      'Process/archive/',]     
  
#List of all directories inside all environments with csv FILES to zip
PATH_TO_CSV = ['Input/Party/',
                   'Process/reconciliation/',]
                   
#List of all directories inside all environments with txt FILES to zip
PATH_TO_TXT = ['Process/archive/output/EODPolicy/',
                   'Process/archive/output/Events/',
                   'Process/archive/output/Party/',
                   'Process/archive/output/Policy/',
                   'Process/archive/output/Relationship/',
                   'Process/archive/output/Transaction/',]
                   
#Current date and time
ARCHIVE_DATE_TIME =  datetime.datetime.now() - datetime.timedelta(DAYS_TO_SUBTRACT)
            
#Current month 
ARCHIVE_MONTH = ARCHIVE_DATE_TIME.strftime("%m")

#Current year
ARCHIVE_YEAR = ARCHIVE_DATE_TIME.strftime("%Y")

#Pattern list of dates that need archiving for folders
PATTERN_DATE_FOR_FOLDERS = [ARCHIVE_MONTH+ '-..-' + ARCHIVE_YEAR] 
                      
#Pattern list of dates that need archiving for files
PATTERN_DATE_FOR_FILES = [ARCHIVE_MONTH + '..' + ARCHIVE_YEAR]

#Location where all zip file will be placed withing the current environment by month.. i.e. '//tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/zip_location/MM-YYYY'                     
ZIP_LOCATION = 'Zip/'

#List of all zips created
ZIPS_CREATED = [] 
    
#Creates the name of zip file for folders
# date = month and year or the files being archived... i.e. 'MM-YYYY'
# path_to_folder = path leading to but not including the file to be archived... i.e. 'Process/Archive/output/EODPolicy/'
# path_to_environment = path leading to the environment of the file to be archived.. i.e. //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_sys/' or 'O:/q_thrivent_tamls_sys/' ##TRAILING / MUST BE INCLUDED IN PATH NAME ##
#
# Returns string containing the zip name
def get_folder_zip_file_name(date, path_to_folder, path_to_environment):
    #split path_to_folder
    path_to_folder_split = path_to_folder.split('/')    
    #insert the environment name into the front of the path list and then create zip name with list
    path_to_folder_split.insert(0,ENVIRONMENT)
    zip_file_name = ''.join(path_to_folder_split)+ '-' + date + '.zip'
    return zip_file_name   

#Creates the name of zip file for files
# date = month and year or the files being archived... i.e. 'MM-YYYY'
# path_to_file = path leading to but not including the file to be archived... i.e. 'Process/Archive/output/EODPolicy/'
# path_to_environment = path leading to the environment of the file to be archived.. i.e. //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_sys/' or 'O:/q_thrivent_tamls_sys/' ##TRAILING / MUST BE INCLUDED IN PATH NAME ##
#
# Returns string containing the zip name
def get_file_zip_file_name(date,path_to_file,path_to_environment):
    #split path_to_file 
    path_to_file_split = path_to_file.split('/')
    #insert the environment name into the front of the path list and then create zip name with list
    path_to_file_split.insert(0,ENVIRONMENT)
    zip_file_name = ''.join(path_to_file_split)+ '-' + date + '.zip'
    return zip_file_name    
    
#Helper method for txt_files_archive - Takes a list of files and their current directory location and zips them into monthly archives and print out number of files to be archived
# files_list = a list of paths to each file found matching current pattern... i.e. ['//tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/Process/Archive/output/Events\\EventContract_Output_BankInfo_11282018_00001.txt', .....]               
# directory = path to current directory being searched... i.e.  //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/Process/Archive/output/Events/ 
# environment = path to current environment... i.e.  //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/
# path_to_file = path to current file within current environment... i.e. Process/Archive/output/Events/
def montly_archives_file_list(files_list,directory,environment,path_to_file):
    #var to hold boolean for deleting the folder containing the files
    delete_folder = 0
    #var to hold total number of files found
    total_files = 0
    #var to hold zip name
    zip_file_name = ''   #placeholder  
    #var to hold current zip file name 
    for date in PATTERN_DATE_FOR_FILES:
        #Convert date to dd-yyyy
        real_date = date[0:2] + '-' + date[4:8] 
        files_to_archive = []
        #var to hold number of files found per directory
        num_files = 0
        for file in files_list:
            zip_file_name = get_file_zip_file_name(real_date,path_to_file,environment)  
            if re.search(date,file):
                files_to_archive.append(file)                                            
                num_files += 1
                total_files += 1
        if num_files != 0:
            #archive the files
            archive_files(files_to_archive,directory,zip_file_name,environment,real_date,delete_folder)                   


#Takes a list of files their current directory the name of a zip and the location where the zips are to be placed and zips them all up and places them in specified directory           
# file_list = a list of paths to each file found matching the current patern... i.e.  ['//tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/Process/Archive/output/Events\\EventContract_Output_BankInfo_11282018_00001.txt',...]
# directory = path to current directory being searched... i.e.  //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/Process/Archive/output/Events/ 
# zip_file_name = the name of the file to be zipped... i.e.  DEVInputEODPolicyFiltered-09-2018.zip
# environment = path to current environment... i.e.   //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/
# date = date of current search... i.e. MM-YYYY
# delete_folder = boolean to delete the folder the files are in (1) or not (0)
def archive_files(file_list,directory,zip_file_name,environment,date,delete_folder):
    zip_location = environment + ZIP_LOCATION + date + '/'
    orig_zip_file_name = zip_file_name
    zip_file_name = zip_location + zip_file_name
    #temp list for the files added to the zip
    temp_zip_file_list = []
    #current time to print at beginning of every output line
    now = str(datetime.datetime.now()) + "  -  "
    print(now + 'Create zip file named: ' + zip_file_name)
    if not os.path.exists(zip_location):
        os.makedirs(zip_location)
    #writing files to a zipfile 
    #variable for deleting the directory found after the archive
    dirToRemove =  ''
    newZip = None
    try:
        newZip = zipfile.ZipFile(zip_file_name, 'w',zipfile.ZIP_DEFLATED)
        for file in file_list:           
            newZip.write(file)
            temp_zip_file_list.append(file)
        
    finally:
        newZip.close() 

    ############THIS NEXT LINES DELETE THE FILES AND EMPTY FOLDERS THAT HAVE JUST BEEN ARCHIVED##############
    if DELETE_FILES == 1:
        for file in file_list:
            dirToRemove = os.path.split(file)[0] 
            try:
                os.remove(file)
            except OSError as e: # name the Exception `e`
                #current time to print at beginning of every output line
                now = str(datetime.datetime.now()) + "  -  "
                print (now + "Failed with:", e.strerror) # look what it says
                print (now + "Error code:", e.code)
            #if directory is empty and we want to delete the base folder
            if not os.listdir(dirToRemove):
                if dirToRemove:
                    try:
                        shutil.rmtree(dirToRemove)
                    except Exception as e:
                        #current time to print at beginning of every output line
                        now = str(datetime.datetime.now()) + "  -  "
                        print(now + ' ' + e)
                        raise
    ########################################################################################
            
    temp_array = [str(orig_zip_file_name),temp_zip_file_list]                
    ZIPS_CREATED.append(temp_array)
    #FILES_IN_ZIP.append(temp_zip_file_list)
    #current time to print at beginning of every output line
    now = str(datetime.datetime.now()) + "  -  "
    print(now + 'All files zipped successfully!')  
    print(" ")              
        
#Searches through all directories in the PATH_TO_FOLDERS list for any folders matching the PATTERN_DATE_FOR_FOLDERS list and archives 
# them by path and pattern and places them into the ZIP_LOCATION + MM-YYYY of the current environment.
#
# Returns Total Number of files found      
def folders_archive():
    #var to hold boolean for deleting the folder containing the files
    delete_folder = 1
    #Total files found
    total_files = 0
    #loop through all dates in the dates to archive
    for date in PATTERN_DATE_FOR_FOLDERS:
        #convert date to dd-yyyy
        real_date = date[0:3] + date[6:10]    
        #set environment variable
        environment = PATH_TO_ENVIRONMENT
        #loop through every directory path that archives by folder
        for folder in PATH_TO_FOLDERS:
            #var for zip file name 
            zip_file_name = get_folder_zip_file_name(real_date,folder,environment)
            #var for list of filepaths including filename
            file_list = []
            #var to hold number of folders found per path
            num_folders = 0
            #create each full_path call
            full_path = environment+folder              
            #validate full_path exists: if it does search through it Otherwise: print out directory does not exist
            if os.path.isdir(full_path):
                #update variable with the current directory of folders
                curr_dir_folders = next(os.walk(full_path))[1]
                #loop through all folders in current directory
                for folder in curr_dir_folders:
                    #check all dates against the folder name
                    if re.search(date,folder):
                        #create pattern looking for all files in the current folder
                        glob_pattern = full_path + folder +  "/*"
                        #add all files found to the file_list var
                        file_list += glob.glob(glob_pattern)            
                        num_folders += 1
                #if folders are found containing files print where they were found and archive them
                if(num_folders > 0):                        
                    #archiving will happen in this function call
                    archive_files(file_list,full_path,zip_file_name,environment,real_date,delete_folder)
                total_files += num_folders
            else:
                #current time to print at beginning of every output line
                now = str(datetime.datetime.now()) + "  -  "
                print(now + full_path + ' does not exist.') 
                print(' ')
    return total_files

#Archives all csv files in the PATH_TO_CSV in every PATH_TO_ENVIRONMENT into monthly archives     
def csv_files_archive():
    #set environment variable
    environment = PATH_TO_ENVIRONMENT
    #loop through every directory path that archives by folder
    for csv in PATH_TO_CSV:
        #create each directory call
        directory = environment+csv
        #validate directory exists: if it does search through it Otherwise: print out directory does not exist
        if os.path.isdir(directory):
            #create pattern looking for all xml files in the current folder
            glob_pattern = directory + '*.csv'
            #add all files found to the file_list var
            file_list = glob.glob(glob_pattern)
            #archiving will happen in this function call
            montly_archives_file_list(file_list,directory,environment,csv)
        else:
            #current time to print at beginning of every output line
            now = str(datetime.datetime.now()) + "  -  "
            print(now + directory + ' does not exist.')

#Archives all txt files in the PATH_TO_TXT in every PATH_TO_ENVIRONMENT into monthly archives     
def txt_files_archive():      
    #set environment variable
    environment = PATH_TO_ENVIRONMENT
    #loop through every directory path that archives by folder
    for txt in PATH_TO_TXT:
        #create each directory call
        directory = environment+txt
        #validate directory exists: if it does print the directory 
        if os.path.isdir(directory):
            #create pattern looking for all xml files in the current folder
            glob_pattern = directory + '*.txt'
            #add all files found to the file_list var
            file_list = glob.glob(glob_pattern)
            #archiving will happen in this function call
            montly_archives_file_list(file_list,directory,environment,txt)              
        else:
            #current time to print at beginning of every output line
            now = str(datetime.datetime.now()) + "  -  "
            print(now + directory + ' does not exist.')                
        
#Runs the Program        
def main():
    print('')
    print('------------------------- This is the start of a new output file -------------------------')
    folders_archive()
    csv_files_archive()
    txt_files_archive()
    #Print summary of files archived
    print('')
    print('')
    print('')
    print('')
    print('')
    #current time to print at beginning of every output line
    now = str(datetime.datetime.now()) + "  -  "
    print(now + str(len(ZIPS_CREATED)) + ' zipped archives created for date ' + ARCHIVE_MONTH + '-' +  ARCHIVE_YEAR + '.  See Below:')
    
    for list in sorted(ZIPS_CREATED):
        #current time to print at beginning of every output line
        now = str(datetime.datetime.now()) + "  -  "
        print (now + list[0]) 
        print (now + 'with files')                   
        for file in list[1]:
            #current time to print at beginning of every output line
            now = str(datetime.datetime.now()) + "  -  "
            print (now + file)
        #current time to print at beginning of every output line
        now = str(datetime.datetime.now()) + "  -  "
        print(now + str(len(list[1])) + ' files zipped')
    
    print('')
    print('')
    print('')
    print('')
    print('')
    
    return 0

#needed to run main    
if __name__ == "__main__": 
    main()
