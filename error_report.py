import sys
import os
import re
import pandas as pd
import datetime

# Get the path to the main folder from user parameter
#test_files_folder = r''
test_files_folder = sys.argv[1]

# 
original_files_folder = os.path.join(test_files_folder, 'original_files')
cleaned_folder = os.path.join(test_files_folder, 'cleaned')
output_folder = os.path.join(test_files_folder, 'output')

# Check for correct folder with original files to be processed.
if not os.path.exists(original_files_folder):
    raise Exception("Files to be processed need to be in folder: ", original_files_folder)
else:
    print('Folder for files exists at: ', original_files_folder)

# Check for a folder for cleaned files or create one.
if not os.path.exists(cleaned_folder):
    os.mkdir(cleaned_folder)

# Check for a folder for output files or create one.
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Print a count of how many files there are to process.
print('Files to be processed: ', len([name for name in os.listdir(original_files_folder) \
                                      if os.path.isfile(os.path.join(original_files_folder, name))]))

# The original files need to be cleaned up before we process them.
# In this case no newline was added before the From field.

# Loop through the files
for file in os.listdir(original_files_folder):
    
    # Only open the files, not directories.
    if os.path.isfile(os.path.join(original_files_folder, file)):
        
        # Open the files in read mode with a context manager.
        with open(os.path.join(original_files_folder, file), 'r') as rf:
            
            # Tell the user what action is taking place.
            print('Opened file at: ', os.path.join(original_files_folder, file))
            
            # Open the file in the cleaned directory in append mode.
            with open(os.path.join(cleaned_folder, file), 'a') as wf:
                
                # Loop through the lines in the original file.
                for line in rf:
                    
                    # Search the line to see if the From line is present without a line break.
                    fromtext = re.search(r'[A-Za-z]From:', line)
                    
                    # Add a line break in front of the from if it's present.
                    if fromtext:
                        line = line.replace("From:", "\nFrom")
                        
                    # Write the line to the cleaned file
                    wf.write(line)
                    
                # Tell the user what action is taking place after we're done writing to the file.
                print('Cleaned file created at: ', os.path.join(cleaned_folder, file))
                
# Create an empty dictionary.
body_dict = {}

# Loop through the files.
for file in os.listdir(cleaned_folder):
    
    # Only open files, not directories.
    if os.path.isfile(os.path.join(cleaned_folder, file)):
        
        # Open the files in read mode with a context manager.
        with open(os.path.join(cleaned_folder, file), 'r') as rf:
            
            # Loop through the lines of the file.
            for line in rf:
                
                # Search the line for a message matching this format.
                body = re.search(r'^Response .* Please Map this NCID >> *([0-9]*) *dictionary.*', line)
                
                # group(0) is the entire message if there is a match.
                # Groups are indexed according to the order of parentheses in the regular expression.
                if body:
                    found0 = body.group(0)
                    found1 = body.group(1)
                    
                    # Check the dictionary to see if the error message is already present as a key. If not, add it.
                    # The numeric identifier and the count are going into a list.
                    if found0 not in body_dict:
                        body_dict[found0] = [found1, 1]
                        
                    # If the error message is present in the dictionary, increase the count by 1.
                    else:
                        body_dict[found0][1] += 1
                        
# Tell the user the dictionary has been created.
print('Dictionary created.')



# Convert the dictionary to a Pandas dataframe.
df = pd.DataFrame.from_dict(body_dict, orient = 'index', columns = ['NCID','Count'])

# Change the error message from the index to a regular column and name the column.
df.reset_index(inplace=True)import datetime

# Get the current date and time to name the file.
now = datetime.datetime.now()

# Change format to YYYY-mm-dd-H-M-S
dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")

# Create the name of the file.
file_name_string = 'error_counts_' + dt_string + '.xlsx'

# Save the dataframe as an Excel file.
df.to_excel(os.path.join(output_folder, file_name_string), index = False)

# Tell the user where the final output was saved.
print('Error report saved at: ', os.path.join(output_folder, file_name_string))
df = df.rename(columns = {'index':'error_message'})

# Sort the dataframe by the count in descending order.
df = df.sort_values(by ='Count', ascending = 0)

# Tell the user the dictionary has been converted to a dataframe.
print('Dictionary converted to dataframe.')

# Get the current date and time to name the file.
now = datetime.datetime.now()

# Change format to YYYY-mm-dd-H-M-S
dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")

# Create the name of the file.
file_name_string = 'error_counts_' + dt_string + '.xlsx'

# Save the dataframe as an Excel file.
df.to_excel(os.path.join(output_folder, file_name_string), index = False)

# Tell the user where the final output was saved.
print('Error report saved at: ', os.path.join(output_folder, file_name_string))