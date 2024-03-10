from gym import spaces
import numpy as np

class CondiSpace (spaces.Dict):
    
    def __init__(self, condi_space: spaces.Box | spaces.Discrete):
        super.__init__(self, {"condi": condi_space, "duration": spaces.Box(low=0, shape=(), dtype=np.float32)})