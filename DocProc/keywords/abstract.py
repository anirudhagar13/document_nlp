# Abstract class fixing behaviour of Keyword extraction implementations
from abc import ABCMeta, abstractmethod

class Extractor(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_keywords(self):
        pass

    @abstractmethod
    def __str__(self):
        pass