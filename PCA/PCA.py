import numpy as np
import sys
import argparse


# ------------------------------------------
#    Parse                
# ------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('-o','--output',    dest="OutputFile",  required=True,   help="Output file with transformed date")
parser.add_argument('-i','--input',     dest="InputFile",   required=True,   help="Input file")
parser.add_argument('-nv','--num_vec',  dest="NVectors", required=True,      help="Number of vectors to build projected data")
parser.add_argument('-s','--spectrum',  dest="SpectrumFile", required=True,  help="Eigenvalue spectrum file")


args = parser.parse_args()
NVectors = int(args.NVectors)
InputFile  = args.InputFile
OutputFile = args.OutputFile
SpectrumFile = args.SpectrumFile

#--------------------------------------------
#    Open InputFile reading the following 
#    format: 
#
#    #Coments....................
#         1    x1  x2  x3  ...
#         2    x1  x2  x3  ...
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
        sys.exit('tICA.py: Error. Some line of input file contains incomplete data.')


    # Add coordinates array to samples array
    data.append( array )

data = np.array(data,dtype=np.float64)


#-------------------------------------------
#    Make PCA
#-------------------------------------------

C = np.cov(np.transpose(data))
w, v = np.linalg.eigh( C )

w = w[::-1]
v = v[:,::-1]

#-------------------------------------------
#    Write spectrum file
#-------------------------------------------
SpectrumFile = open(SpectrumFile,'w')

for i in range(w.size):
    SpectrumFile.write('%8i %12.6f \n' %( i+1, w[i] ))

SpectrumFile.close()


#-------------------------------------------
#    Project data
#-------------------------------------------
P = v[:,0:NVectors]
newdata = np.dot(data,P)


OutputFile = open(OutputFile,'w')

for i in range(newdata.shape[0]):

    OutputFile.write('%8i' %(i+1))
    for j in range(newdata.shape[1]):
        OutputFile.write('%12.6f ' %newdata[i,j])
    OutputFile.write('\n')

OutputFile.close()

