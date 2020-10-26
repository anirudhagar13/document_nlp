# Abstract class fixing behaviour of encoders

from abc import ABCMeta, abstractmethod
from ..files import read_from_pkl, write_to_pkl

# Logger
import logging
logger = logging.getLogger(__name__)

class Encoder(metaclass=ABCMeta):

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
    def inverse_transform(self):
        pass

    def save_model(self, model, model_path, encoder):
        '''
        Parent implementation for saving model
        Default function. Implementation not forced on child
        '''
        logger.info('Saving Model : {0}'.format(encoder))

        try:
            write_to_pkl(model, model_path)
        except Exception as e:
            logger.error('Error in saving trained model !!', e, sep='\n')

        logger.info('Saved Model : {0}'.format(encoder))

    def load_model(self, model_path, encoder):
        '''
        Parent implementation for saving model
        Default function. Implementation not forced on child
        '''
        model = object()

        # Restoring model module as per encoder
        logger.info('Restoring Model : {0}'.format(encoder))

        try:
            model = read_from_pkl(model_path)              
        except Exception as e:
            logger.error('Error in restoring trained model !!\n {0}'.format(e))

        # Restoring model module as per encoder
        logger.info('Restored Model : {0}'.format(encoder))

        return model

    @abstractmethod
    def __str__(self):
        pass
        