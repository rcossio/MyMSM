import numpy as np
import sys
import argparse


# ------------------------------------------
#    Parse                
# ------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument('-lt','--lag_time', dest="LagTime"    ,  required=True,  help="Lag time, multiple of sample time (integer)")
parser.add_argument('-o','--output',    dest="OutputFile",  required=True,   help="Output file with transformed date")
parser.add_argument('-i','--input',     dest="InputFile",   required=True,   help="Input file")
parser.add_argument('-nv','--num_vec',  dest="NVectors", required=True,      help="Number of vectors to build projected data")
parser.add_argument('-s','--spectrum',  dest="SpectrumFile", required=True,  help="Eigenvalue spectrum file")


args = parser.parse_args()
LagTime  = int(args.LagTime)
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
#    AMUSE algorithm 
#-------------------------------------------

#Get principal components
y = np.dot(data,v)

#Normalizing data (check if sense is correct)
y = np.dot(y,np.diag(w))

#Generate time-lagged covariance matrix
N = y.shape[0]
dim = y.shape[1]
C = np.zeros((dim,dim),dtype=np.float64)

for i in range(dim):
    for j in range(dim):
        for k in range(N-LagTime):
            C[i,j] += y[k,i]*y[k+LagTime,j]
        C[i,j] /= N-LagTime-1
              


#Create symmetrized covariance matrix
C = 0.5 *(C+ np.transpose(C))

#Decompose
w, v = np.linalg.eigh( C )

w = w[::-1]
v = v[:,::-1]

#Project data
P = v[:,0:NVectors]
z = np.dot(y,P)


#-------------------------------------------
#    Write spectrum file
#-------------------------------------------
SpectrumFile = open(SpectrumFile,'w')

for i in range(w.size):
    SpectrumFile.write('%8i %12.6f \n' %( i+1, w[i] ))

SpectrumFile.close()


#-------------------------------------------
#    Write data
#-------------------------------------------
OutputFile = open(OutputFile,'w')

for i in range(z.shape[0]):

    OutputFile.write('%8i' %(i+1))
    for j in range(z.shape[1]):
        OutputFile.write('%12.6f ' %z[i,j])
    OutputFile.write('\n')

OutputFile.close()


