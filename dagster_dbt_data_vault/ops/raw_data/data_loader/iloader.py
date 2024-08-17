from abc import ABC, abstractmethod

import pandas as pd


class IRawDataLoader(ABC):
    @abstractmethod
    def load_data(self, data: pd.DataFrame):
        raise NotImplementedError
