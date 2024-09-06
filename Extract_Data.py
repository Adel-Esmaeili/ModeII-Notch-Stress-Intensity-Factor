# This code uses all the Job_1, Job_2, Job_3,..., to extract S12 (Shear Stress) along the specific path, in this code, the path is the first 3000 nodes that their Y value is zero #
# This code specificly made for Notched Speciment to extract S12 on the bisector line, but can be used for everything only after some changes #
# The code is made by Adel Esmaeili Atrabi #
# The CopyRight is Reserved #


# Import required modules
from odbAccess import openOdb
import odbAccess
import math
import numpy    
import os
import shutil
import csv
from collections import defaultdict

# Set the maximum number of iterations
Max_iterations = 7396

# Open a file to write the results
sortie = open('Results_fromODB.txt', 'w')
sortie.write('\n')

# Loop through all the jobs
for q in range(7283, Max_iterations + 1):
    # Set up the ODB file path
    odbname = 'Job_%d' % (q)
    path = './'
    myodbpath = path + odbname + '.odb'    
    odb = openOdb(myodbpath)
    
    # Get the last frame of the first step
    step = odb.steps['Step-1']
    last_frame = step.frames[-1]
    S = last_frame.fieldOutputs['S']
    
    # Get the assembly and instance
    assembly = odb.rootAssembly
    instance = assembly.instances.values()[0]
    
    # Use defaultdict to accumulate S12 values and counts for each node
    node_data = defaultdict(lambda: {'sum_S12': 0.0, 'count': 0, 'coords': None})
    
    # Calculate average S12 for each node
    for value in S.values:
        s12 = value.data[3]  # S12 is the 4th component (index 3) of the stress tensor
        element = instance.elements[value.elementLabel - 1]
        for node in element.connectivity:
            if node_data[node]['coords'] is None:
                node_data[node]['coords'] = instance.nodes[node - 1].coordinates
            node_data[node]['sum_S12'] += s12
            node_data[node]['count'] += 1
    
    # Filter nodes with Y=0 and calculate average S12
    y0_nodes = []
    for node, data in node_data.items():
        if data['coords'][1] == 0:  # Y coordinate is 0
            avg_s12 = data['sum_S12'] / data['count'] if data['count'] > 0 else 0
            y0_nodes.append([node, data['coords'][0], avg_s12])
    
    # Sort nodes by X coordinate
    y0_nodes.sort(key=lambda x: x[1])
    
    # Take first 3000 nodes
    y0_nodes = y0_nodes[:3000]
    
    # Calculate total_S12 using a regular for loop
    total_S12 = 0.0
    for node in y0_nodes:
        total_S12 += node[2]
    
    # Calculate average S12
    avg_S12 = total_S12 / len(y0_nodes) if y0_nodes else 0
    
    # Write results to CSV file
    csv_filename = 'S12_values_Y0_nodes_Job_%d.csv' % (q)
    with open(csv_filename, 'wb') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Node', 'X', 'S12'])
        for data in y0_nodes:
            csv_writer.writerow(data)
    
    # Close the ODB file
    odb.close()
    
    # Write average S12 to the results file
    sortie.write('\n Average S12 (shear stress) for Y=0 nodes from Job-%d is: %f \n' % (q, avg_S12))
    print("S12 values for Y=0 nodes (sorted by X, first 3000) for Job-{0} have been saved to {1}".format(q, csv_filename))

# Close the results file
sortie.close()
print("Results have been written to Results_fromODB.txt")