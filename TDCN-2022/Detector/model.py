import abc 

class Model(metaclass=abc.ABCMeta):
    """이미지를 통한 우울증 예측 모델"""
    
    @abc.abstractmethod
    def predict(self, data):
        pass


class DataLoader(metaclass=abc.ABCMeta):
    """Pytorch 모델의 데이터셋"""

    @abc.abstractmethod
    def __getitem__(self):
        pass