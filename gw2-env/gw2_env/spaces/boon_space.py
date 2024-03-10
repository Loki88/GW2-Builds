from gym import spaces
import numpy as np

class BoonSpace (spaces.Dict):
    
    def __init__(self, boon_space: spaces.Box | spaces.Discrete):
        super.__init__(self, {"boon": boon_space, "duration": spaces.Box(low=0, shape=(), dtype=np.float32)})