# This code is made to create and execution N number of  models (No_of_Files), and save the corresponding  jobs in temp derectory #
# It should be noted that this code accept .txt file as an input, and the input is the code written in .jnl file #
# So, the researcher should first create the first .jnl file manually, then based on their needs, produce the consequent .txt file #
# The name of the .txt file should be File_1, File_2, File_3, ... , File_n  ---> n = No_of_Files   #
# The output is Job_1, Job_2, Job_3, ..., Job_n # 
# The code is made by Adel Esmaeili Atrabi #
# The CopyRight is Reserved #

# Import necessary modules from Abaqus and Python standard library
from abaqus import *
from abaqusConstants import *
import os

# Set the total number of files to process
No_of_Files = 7907  # We want to process File_1, File_2, ..., File_n
# Set the starting file number
Start_No = 7555

# Main loop to process files
for q in range(Start_No, No_of_Files):
    # Generate the filename based on the current iteration
    filename = 'File_%d' % (q)       # set file name here
    path = './'                      # set path here (if in working dir no need to change!)
    filepath = path + filename + '.txt'
    
    # Check if the file exists
    if os.path.exists(filepath):
        print('Processing %s' % filepath)
        
        # Create a new model with a unique name
        model_name = 'Model_%d' % (q)
        mdb.Model(name=model_name)
        
        # Make the new model current
        current_model = mdb.models[model_name]
        
        # Read the content of the file
        with open(filepath, 'r') as file:
            file_content = file.read()
        
        # Modify the content to operate on the current model instead of 'Model-1'
        modified_content = file_content.replace('mdb.models[\'Model-1\']', 'current_model')
        
        # Execute the modified content
        exec(modified_content)
        
        print('Completed processing %s and created %s' % (filepath, model_name))
        
        # Create a job for this model
        job_name = 'Job_%d' % (q)
        mdb.Job(name=job_name, model=model_name, description='Job created for %s' % filename)
        
        print('Created job %s for model %s' % (job_name, model_name))
        
        # Submit the job and wait for completion
        print('Submitting job %s' % job_name)
        mdb.jobs[job_name].submit(consistencyChecking=OFF)
        mdb.jobs[job_name].waitForCompletion()
        print('Completed job %s' % job_name)
        
    else:
        # If the file doesn't exist, print a message and continue to the next iteration
        print('File %s not found. Skipping.' % filepath)

# Final message indicating completion of all processing
print("All specified files have been processed, jobs created and completed.")