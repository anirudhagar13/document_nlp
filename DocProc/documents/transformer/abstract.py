# Abstract class fixing behaviour of transformers
from abc import ABCMeta, abstractmethod

class Transformer(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def fit_transform(self):
        pass

    @abstractmethod
    def __str__(self):
        pass