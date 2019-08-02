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

#Import 
import os
import re
import glob
import shutil
import datetime
import time
import itertools
import zipfile
from zipfile import ZipFile 

#Variable to delete files after archive 0 if you DO NOT want to delete and 1 if you DO####################
DELETE_FILES = 0
################################################################################

#List of current PATH_TO_ENVIRONMENTS############################################################
PATH_TO_ENVIRONMENTS = ['C:/dserver01/DEV/',
                        'C:/iserver01/ITE/',
                        'C:/sserver01/SYS/',
                        'C:/pserver01/PROD/']
#Current Environment used in naming the zip file i.e. DEV, SYS, ITE, PROD
ENVIRONMENTS = ['DEV', 'ITE', 'SYS', 'PROD']

##################################################################################################

#List of all directories inside all environments with FOLDERS to zip
PATH_TO_FOLDERS = ['Input/EODPolicy/Filtered/',
                      'Input/Events/Filtered/',
                      'Input/Party/Filtered/',
                      'Input/Policy/Filtered/',
                      'Input/Relationship/Filtered/',
                      'Input/Transaction/Filtered/',
                      'Process/archive/',]                       
                   
#List of all directories inside all environments with txt FILES to zip
PATH_TO_FILES = ['Input/Party/',
                   'Process/reconciliation/','Process/archive/output/EODPolicy/',
                   'Process/archive/output/Events/',
                   'Process/archive/output/Party/',
                   'Process/archive/output/Policy/',
                   'Process/archive/output/Relationship/',
                   'Process/archive/output/Transaction/',
                   ]
                                    
#Pattern list of dates that need archiving for folders
PATTERN_DATE_FOR_FOLDERS = ['08-..-2018',
                        '09-..-2018',
                        '10-..-2018',                        
                        '11-..-2018',
                        '12-..-2018',
                        '01-..-2019',
                        '02-..-2019',
                        '03-..-2019',                        
                        '04-..-2019']
                        
#Pattern list of dates that need archiving for files
PATTERN_DATE_FOR_FILES = ['08..2018',
                        '09..2018',
                        '10..2018',                        
                        '11..2018',
                        '12..2018',
                        '01..2019',
                        '02..2019',
                        '03..2019',                        
                        '04..2019'] 

#Location where all zip file will be placed withing the current environment by month.. i.e. '//server/environmentName/zip_location/MM-YYYY'                     
ZIP_LOCATION = 'Zip/'

#List of lists including all zips created and their files i.e.[zip_name,[zip_files]
ZIPS_CREATED = []
    
#Creates the name of the zip file 
# date = month and year or the files being archived... i.e. 'MM-YYYY'
# path_to_folder = path leading to but not including the file to be archived... i.e. 'Process/Archive/output/EODPolicy/'  ##TRAILING / MUST BE INCLUDED IN PATH NAME ##
# path_to_environment = path leading to the environment of the file to be archived.. i.e. //server/environmentName/'  ##TRAILING / MUST BE INCLUDED IN PATH NAME ##
#
# Returns string containing the zip name
def get_zip_file_name(date, path_to_folder, path_to_environment):
    #split path_to_folder
    path_to_folder_split = path_to_folder.split('/')    
    #insert the environment name into the front of the path list and then create zip name with list
    envIndex = PATH_TO_ENVIRONMENTS.index(path_to_environment) 
    path_to_folder_split.insert(0,ENVIRONMENTS[envIndex])
    zip_file_name = ''.join(path_to_folder_split)+ '-' + date + '.zip'
    return zip_file_name       


#Takes a list of files their current directory the name of a zip and the location where the zips are to be placed and zips them all up and places them in specified directory.
#           
#   file_list = a list of paths to each file found matching the current patern... i.e.  ['//server/environmentName/Process/Archive/output/Events\\EventCo18_00001.txt',...]
#   directory = path to current directory being searched... i.e.  //server/environmentName/Process/Archive/output/Events/ 
#   zip_file_name = the name of the file to be zipped... i.e.  DEVInputEODPolicyFiltered-09-2018.zip
#   environment = path to current environment... i.e.   //server/environmentName/
#   date = date of current search... i.e. MM-YYYY
#   delete_folder = boolean to delete the folder the files are in (1) for true or (0) for false
def archive_files(file_list,directory,zip_file_name,environment,date,delete_folder):
    zip_location = environment + ZIP_LOCATION + date + '/'
    orig_zip_file_name = zip_file_name
    zip_file_name = zip_location + zip_file_name
    #temp list for the files added to the zip
    temp_zip_file_list = []
    #current time to print at beginning of every output line
    now = str(datetime.datetime.now()) + "  -  "
    print(now + 'Create zip file named: ' + zip_file_name) # verify you want to archive these files    
    print('Your files will be zipped into the following directory: ' + zip_location)
    print('Are you sure you want to archive these files?')
    answer = input("Enter y or n: ")    
    if answer == "y": 
        if not os.path.exists(zip_location):
            os.makedirs(zip_location) 
        #variable for deleting the directory found after the archive
        dirToRemove =  ''
        #writing files to a zipfile
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
                    if delete_folder:
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
        #current time to print at beginning of every output line
        now = str(datetime.datetime.now()) + "  -  "
        print(now + 'All files zipped successfully!')  
        print(" ")
        
    elif answer == "n":
        exit()  
        
    else:
        print("Please enter y or n.")
        
#Searches through all directories in the PATH_TO_FOLDERS list for any folders matching the PATTERN_DATE_FOR_FOLDERS list and archives 
#them by path and pattern and places them into the ZIP_LOCATION + MM-YYYY of the current environment.
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
        for environment in PATH_TO_ENVIRONMENTS:
            #loop through every directory path that archives by folder
            for folder in PATH_TO_FOLDERS:
                #var for zip file name 
                zip_file_name = get_zip_file_name(real_date,folder,environment)
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
            
#Searches through all directories in the PATH_TO_FILES list for any files of a specified file type (file_ext) matching the PATTERN_DATE_FOR_FOLDERS list and archives 
#them by path and pattern and places them into the ZIP_LOCATION + MM-YYYY of the current environment.
#
#   file_ext = the extension of the type of file you want to archive. I.E. txt, csv, or * for all files
#
# Returns Total Number of files found       
def files_archive(file_ext):      
    #set environment variable
    for environment in PATH_TO_ENVIRONMENTS:
    #loop through every directory path that archives by folder
        for path in PATH_TO_FILES:
            #create each directory call
            directory = environment+path
            #validate directory exists: if it does print the directory 
            if os.path.isdir(directory):
                #create pattern looking for all files in the current folder
                glob_pattern = directory + '*.' + file_ext
                #add all files found to the file_list var
                file_list = glob.glob(glob_pattern)    
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
                    for file in file_list:
                        zip_file_name = get_zip_file_name(real_date,path,environment)  
                        if re.search(date,file):
                            files_to_archive.append(file)                                            
                            num_files += 1
                            total_files += 1
                    if num_files != 0:
                        #archive the files
                        archive_files(files_to_archive,directory,zip_file_name,environment,real_date,delete_folder)      
            else:
                #current time to print at beginning of every output line
                now = str(datetime.datetime.now()) + "  -  "
                print(now + directory + ' does not exist.')                
        return total_files
        
#Runs the Program        
def main():
    print('')
    print('------------------------- This is the start of a new output -------------------------')
    folders_archive()
    files_archive('csv')
    files_archive('txt')
    #Print summary of files archived
    print('')
    print('')
    print('')
    print('')
    print('')
    #current time to print at beginning of every output line
    now = str(datetime.datetime.now()) + "  -  "
    print(now + str(len(ZIPS_CREATED)) + ' zipped archives created. See Below:')
    
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
        
    print(now + str(len(ZIPS_CREATED)) + ' total zipped archives created.')
    print('')
    print('')
    print('')
    print('')
    print('')
        
    return 0

#needed to run main    
if __name__ == "__main__": 
    main()