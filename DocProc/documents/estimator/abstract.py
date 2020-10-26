# Abstract class fixing behaviour of estimators

from abc import ABCMeta, abstractmethod
from ..files import read_from_pkl, write_to_pkl

# Logger
import logging
logger = logging.getLogger(__name__)

class Estimator(metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    def save_model(self, model, model_path, estimator):
        '''
        Parent implementation for saving model
        Default function. Implementation not forced on child
        '''
        logger.info('Saving Model : {0}'.format(estimator))

        try:
            write_to_pkl(model, model_path)
        except Exception as e:
            logger.error('Error in saving trained model !!', e, sep='\n')

        logger.info('Saved Model : {0}'.format(estimator))

    def load_model(self, model_path, estimator):
        '''
        Parent implementation for saving model
        Default function. Implementation not forced on child
        '''
        model = object()

        # Restoring model module as per estimator
        logger.info('Restoring Model : {0}'.format(estimator))

        try:
            model = read_from_pkl(model_path)              
        except Exception as e:
            logger.error('Error in restoring trained model !!\n {0}'.format(e))

        # Restoring model module as per estimator
        logger.info('Restored Model : {0}'.format(estimator))

        return model

    @abstractmethod
    def __str__(self):
        pass
        