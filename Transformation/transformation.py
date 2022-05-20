import sys
import os
sys.path.append(os.getcwd())

from abc import ABC, abstractmethod

class Transformation(ABC):

        @abstractmethod
        def appliquer(donnee):
                pass