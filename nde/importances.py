from datascope.importance import Importance
from typing import Optional, Iterable, Union
from pandas import DataFrame, Series
import numpy as np
from numpy.typing import NDArray
from datascope.utility import Provenance


class PipelineImportance:
    def __init__(self, pipeline_utility, importance, **kwargs):
        self.pipeline_utility_ = pipeline_utility
        self.importance = importance
        self.kwargs = kwargs

    def fit(self, train, train_labels, provenance=None):    
        self.train_ = train
        self.train_labels_ = train_labels
        self.provenance_ = provenance
        return self

    def score(self, valid, valid_labels):
        X_train = self.pipeline_utility_.encoding_.fit_transform(self.train_)
        y_train = self.pipeline_utility_.label_encoder_.fit_transform(self.train_labels_)
        X_valid = self.pipeline_utility_.encoding_.transform(valid)
        y_valid = self.pipeline_utility_.label_encoder_.transform(valid_labels)       

        importance = self.importance(utility=self.pipeline_utility_.utility_, **self.kwargs)
        
        return importance.fit(X_train, y_train, provenance=self.provenance_).score(X_valid, y_valid)
    

class LooImportance(Importance):
    
    def __init__(self, utility):
        self.utility = utility
        super().__init__()

    def _fit(
        self,
        X: NDArray,
        y: Union[NDArray, Series],
        metadata: Optional[Union[NDArray, DataFrame]],
        provenance: Provenance,
    ) -> "Importance":
        self.X_train_ = X
        self.y_train_ = y
        self.provenance = provenance
        return self

    def _score(
        self,
        X_valid: NDArray,
        y_valid: Optional[Union[NDArray, Series]] = None,
        metadata: Optional[Union[NDArray, DataFrame]] = None,
        **kwargs
    ) -> Iterable[float]:
        
        complete_utility = self.utility(self.X_train_, self.y_train_, X_valid, y_valid).score
                  
        loos = []
        assignment = np.ones(self.provenance.num_units)
        
        previous_index = 0
        for index in range(self.provenance.num_units):
            assignment[previous_index] = 1
            assignment[index] = 0
            previous_index = index    
            outputs = self.provenance.query(assignment)
            # Find indices of zero elements
            indices_to_delete = np.nonzero(outputs==0)[0]            
            X_train_loo = np.delete(self.X_train_, indices_to_delete, 0)
            y_train_loo = np.delete(self.y_train_, indices_to_delete, 0)                    
            loo = complete_utility - self.utility(X_train_loo, y_train_loo, X_valid, y_valid).score
            loos.append(loo)
        return loos
