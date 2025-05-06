from datascope.importance import Importance
from typing import Optional, Iterable, Union
from pandas import DataFrame, Series
import numpy as np
from numpy.typing import NDArray
from datascope.utility import Provenance


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
        
        #TODO this should use the provenance instead to correctly remove samples                    
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
