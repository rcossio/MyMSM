

from sklearn.cluster import KMeans
import numpy as np
import sys
import argparse


# ------------------------------------------
#    Parse                
# ------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('-nc','--num_clusters', dest="NClust"    ,  required=True, help="Number of clusters")
parser.add_argument('-o','--output',        dest="OutputFile",  required=True, help="Output file with membership labels")
parser.add_argument('-i','--input',         dest="InputFile",   required=True, help="Input file")
parser.add_argument('-c','--centers',      dest="CentersFile", required=True,  help="File to write centers")

args = parser.parse_args()
NClust  = int(args.NClust)
InputFile  = args.InputFile
OutputFile = args.OutputFile
CentersFile = args.CentersFile


#--------------------------------------------
#    Open InputFile reading the following 
#    format: feature format
#
#    #Coments....................
#         1    Ft1  Ft2  Ft3  ...
#         2    Ft1  Ft2  Ft3  ...
#    
#--------------------------------------------

data=[]

for line in open(InputFile):

    # Skip comments (not you, the python script)
    if line.strip()[0] == "#" : 
        continue

    # Define features array
    array = line.split()[1:]

    # Checks if length is the same  
    if len(data) == 0: 
        length0 = len(array)
 
    length = len(array)
    if length != length0:
        sys.exit('kmeans.py: Error. Some line of features file contains incomplete data.')
     

    # Add features array to samples array
    data.append( array )

data = np.array(data,dtype=np.float64)


#-------------------------------------------
#    Report some stuff
#-------------------------------------------

sys.stdout.write('InputFile:       ' + InputFile + '\n')
sys.stdout.write('OutputFile:      ' + OutputFile+ '\n')
sys.stdout.write('Num of clusters: ' + str(NClust) + '\n')
sys.stdout.write('Num of features: ' + str(length0)+ '\n')
sys.stdout.write('Num of samples:  '  + str(data.shape[0])+ '\n')


#-------------------------------------------
#    Make clusters
#-------------------------------------------

kmeans = KMeans(n_clusters=NClust, random_state=0,max_iter=3000).fit(data)
centers =  kmeans.cluster_centers_



#-------------------------------------------
#    Write centers
#-------------------------------------------

CentersFile = open(CentersFile,'w')

for i in range(centers.shape[0]):
    CentersFile.write('%8i ' %i)
    for j in range(centers.shape[1]):
        CentersFile.write('%12.6f ' %centers[i,j])

    CentersFile.write('\n')
CentersFile.close()

#-------------------------------------------
#    Find and write membership
#-------------------------------------------
OutputFile = open(OutputFile,'w')

for i in range(data.shape[0]):

    array = []

    for j in range(centers.shape[0]):
        point  = data[i,:]
        center = centers[j,:]
        dist = np.linalg.norm(point-center)
        array.append( dist )    
    
    n = np.argmin( array ) + 1

    OutputFile.write('%8i %8i \n' %(i,n))

OutputFile.close()    
    
    
 
