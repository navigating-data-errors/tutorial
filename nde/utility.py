from datascope.importance import SklearnModelAccuracy
from datascope.importance.shapley import ShapleyImportance, ImportanceMethod
from sklearn.preprocessing import LabelEncoder


class SklearnPipelineAccuracy:
    
    def __init__(self, whole_pipeline):
        self.encoding_ = whole_pipeline[:-1][0]
        self.label_encoder_ = LabelEncoder()
        self.utility_ = SklearnModelAccuracy(whole_pipeline[-1])

    def __call__(self, train, train_labels, test, test_labels):    
        X_train = self.encoding_.fit_transform(train)
        X_test = self.encoding_.fit_transform(test)

        y_train = self.label_encoder_.fit_transform(train_labels)
        y_test = self.label_encoder_.transform(test_labels)       

        return self.utility_(X_train, y_train, X_test, y_test)