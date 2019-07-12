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
from zipfile import ZipFile 

#List of current PATH_TO_ENVIRONMENTS i.e. //server/environmentName/   ############################################################               
PATH_TO_ENVIRONMENTS = []

##################################################################################################

#List of all directories inside all environments with FOLDERS to zip i.e. after environmentName - folder/subfolder/
PATH_TO_FOLDERS = []
                      
#List of all directories inside all environments with FILES to zip i.e. after environmentName - folder/subfolder/
PATH_TO_FILES = []       

  
#List of all directories inside all environments with csv FILES to zip
PATH_TO_CSV = ['Input/Party/',
                   'Process/Reconciliation/',]

                    
#List of all directories inside all environments with txt FILES to zip
PATH_TO_TXT = ['Process/Archive/output/EODPolicy/',
                   'Process/Archive/output/Events/',
                   'Process/Archive/Party/',
                   'Process/Archive/Policy/',
                   'Process/Archive/Relationship/',
                   'Process/Archive/Transaction/',]
                   
                   
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
                        '04..2019'
                        '05..2019'
                        '06..2019']

#Location where all zip file will be placed withing the current environment by month.. i.e. '//tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/zip_location/MM-YYYY'                     
ZIP_LOCATION = 'Zip/'
    
#Creates the name of zip file for folders
# date = month and year or the files being archived... i.e. 'MM-YYYY'
# path_to_folder = path leading to but not including the file to be archived... i.e. 'Process/Archive/output/EODPolicy/'
# path_to_environment = path leading to the environment of the file to be archived.. i.e. //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_sys/' or 'O:/q_thrivent_tamls_sys/' ##TRAILING / MUST BE INCLUDED IN PATH NAME ##
#
#Returns string containing the zip name
def get_folder_zip_file_name(date, path_to_folder, path_to_envionment):
    #split path_to_folder
    path_to_folder_split = path_to_folder.split('/')    
    #split environment_directory and then grab only the environment name i.e. q_thrivent_tamls_dev and take the last 3 letter to get DEV
    environment_directory_split = path_to_envionment.split('/') 
    environment = environment_directory_split[-2] # This is why the following / in the path name is important! If it is not there the -2 needs to be -1
    environment = environment[-3:].upper()
    #insert the environment name into the front of the path list and then create zip name with list
    path_to_folder_split.insert(0,environment)
    zip_file_name = ''.join(path_to_folder_split)+ '-' + date + '.zip'
    return zip_file_name   

#Creates the name of zip file for files
# date = month and year or the files being archived... i.e. 'MM-YYYY'
# path_to_file = path leading to but not including the file to be archived... i.e. 'Process/Archive/output/EODPolicy/'
# path_to_environment = path leading to the environment of the file to be archived.. i.e. //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_sys/' or 'O:/q_thrivent_tamls_sys/' ##TRAILING / MUST BE INCLUDED IN PATH NAME ##
#
#Returns string containing the zip name
def get_file_zip_file_name(date,path_to_file,path_to_envionment):
    #split path_to_file 
    path_to_file_split = path_to_file.split('/')
    #split environment_directory and then grab only the environment name i.e. q_thrivent_tamls_dev and take the last 3 letter to get DEV
    environment_directory_split = path_to_envionment.split('/') 
    environment = environment_directory_split[-2]  # This is why the following / in the path name is important! If it is not there the -2 needs to be -1
    environment = environment[-3:].upper()   
    #insert the environment name into the front of the path list and then create zip name with list
    path_to_file_split.insert(0,environment)
    zip_file_name = ''.join(path_to_file_split)+ '-' + date + '.zip'
    return zip_file_name    
    
#Helper method for txt_files_archive - Takes a list of files and their current directory location and zips them into monthly archives and print out number of files to be archived
# files_list = a list of paths to each file found matching current pattern... i.e. ['//tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/Process/Archive/output/Events\\EventContract_Output_BankInfo_11282018_00001.txt', .....]               
# directory = path to current directory being searched... i.e.  //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/Process/Archive/output/Events/ 
# environment = path to current environment... i.e.  //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/
# path_to_file = path to current file within current environment... i.e. Process/Archive/output/Events/
def montly_archives_file_list(files_list,directory,environment,path_to_file): 
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
            print('Files found in ' + directory + ': ' + str(num_files) + ' for date: ' + real_date)
            print(" ")  
            #Here is where I need to archive the files
            #archive_files(files_to_archive,directory,zip_file_name,environment,real_date)                   
    if total_files != 0:
        print(str(total_files) + ' total files found in ' + directory)
    else:
        print('Files found in ' + directory + ' but they do not match any of the dates.')

#Takes a list of files their current directory the name of a zip and the location where the zips are to be placed and zips them all up and places them in specified directory           
# file_list = a list of paths to each file found matching the current patern... i.e.  ['//tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/Process/Archive/output/Events\\EventContract_Output_BankInfo_11282018_00001.txt',...]
# directory = path to current directory being searched... i.e.  //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/Process/Archive/output/Events/ 
# zip_file_name = the name of the file to be zipped... i.e.  DEVInputEODPolicyFiltered-09-2018.zip
# environment = path to current environment... i.e.   //tnfiles002b/ft_cifs_thrivent_tamls$/q_thrivent_tamls_dev/
# date = date of current search... i.e. MM-YYYY
def archive_files(file_list,directory,zip_file_name,environment,date):
    zip_location = environment + ZIP_LOCATION + date + '/'
    zip_file_name = zip_location + zip_file_name       
    print('The current directory to be zipped is ' + directory)   
    # printing the list of all files to be zipped 
    print('Following files will be zipped:') 
    for file in file_list: 
        print(file)
    print(' ')
    print('Create zip file named: ' + zip_file_name)
    print(' ')
    # verify you want to archive these files    
    print('Your files will be zipped into the following directory: ' + zip_location)
    print('Are you sure you want to archive these files?')
    answer = input("Enter y or n: ")    
    if answer == "y": 
        if not os.path.exists(zip_location):
            os.makedirs(zip_location)
        # writing files to a zipfile 
        print('Adding files to archive')
        with ZipFile(zip_file_name,'w') as zip: 
         #writing each file one by one 
            for file in file_list: 
                zip.write(file) 
                print('.')
        print('All files zipped successfully!')  
        print(" ")
        print(" ")
        print(" ")
    elif answer == "n":
        exit()         
    else:
        print("Please enter yes or no.")
        
#Searches through all directories in the PATH_TO_FOLDERS list for any folders matching the PATTERN_DATE_FOR_FOLDERS list and archives 
#them by path and pattern and places them into the ZIP_LOCATION + MM-YYYY of the current environment.
#
#Returns Total Number of files found      
def folders_archive():
    #Total files found
    total_files = 0
    #loop through all dates in the dates to archive
    for date in PATTERN_DATE_FOR_FOLDERS:
        #convert date to dd-yyyy
        real_date = date[0:3] + date[6:10]    
        #loop through every environment
        for environment in PATH_TO_ENVIRONMENTS:
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
                            #create pattern looking for all xml files in the current folder
                            glob_pattern = full_path + folder +  "/*.xml"
                            #add all files found to the file_list var
                            file_list += glob.glob(glob_pattern)            
                            num_folders += 1
                    #if folders are found containing files print where they were found and archive them
                    if(num_folders > 0):                        
                        print('Folders found in ' + full_path + ': ' + str(num_folders) + ' for date: ' + real_date)
                        print(" ")
                        #archiving will happen in this function call
                        archive_files(file_list,full_path,zip_file_name,environment,real_date)
                    total_files += num_folders
                else:
                    print(full_path + ' does not exist.') 
                    print(' ')
    return total_files

#Archives all csv files in the PATH_TO_CSV in every PATH_TO_ENVIRONMENTS into monthly archives     
def csv_files_archive():
    #loop through every environment
    for environment in PATH_TO_ENVIRONMENTS:
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
                print(directory + ' does not exist.')

#Archives all txt files in the PATH_TO_TXT in every PATH_TO_ENVIRONMENTS into monthly archives     
def txt_files_archive():      
    #loop through every environment
    for environment in PATH_TO_ENVIRONMENTS:
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
                print(directory + ' does not exist.')                
        
#Runs the Program        
def main():
    folders_archive()
    csv_files_archive()
    txt_files_archive()

#needed to run main    
if __name__ == "__main__": 
    main()