from abc import abstractmethod
import sys
import os
sys.path.append(os.getcwd())

from Transformation.transformation import Transformation

class OperationMathematiques(Transformation):
    
    @abstractmethod
    def appliquer(donnee):
        pass