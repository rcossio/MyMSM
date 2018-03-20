from msmbuilder.dataset import dataset
from matplotlib import pyplot as plt
import numpy as np

trajs = dataset('tica_trajs.h5')    # Load file
trajs = np.concatenate(trajs)       # Flatten list of trajectories
plt.hexbin(trajs[:,0], trajs[:,1], bins='log', mincnt=1)
plt.show()

