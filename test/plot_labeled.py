from msmbuilder.dataset import dataset
from matplotlib import pyplot as plt
import numpy as np

trajs = dataset('labeled_trajs.h5')    # Load file
trajs = np.concatenate(trajs)       # Flatten list of trajectories
trajs.transpose()
for i in range(trajs.shape[0]):
    print trajs[i]

