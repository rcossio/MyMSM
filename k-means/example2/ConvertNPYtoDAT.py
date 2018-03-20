import numpy as np

OutputFile = open('00000000.dat','w')
data = np.load('00000000.npy')



OutputFile.write('# Coment \n')

for i in range(data.shape[0]):
    OutputFile.write('%8i ' %i)

    for j in list(data[i,:]):
        OutputFile.write('%12.6f ' %j)

    OutputFile.write('\n')


OutputFile.close()


