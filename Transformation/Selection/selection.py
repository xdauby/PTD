from abc import abstractmethod
import sys
import os
sys.path.append(os.getcwd())

import numpy as np
from Transformation.transformation import Transformation

class Selection(Transformation):
    
    @abstractmethod
    def appliquer(donnee):
        pass