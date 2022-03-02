import os
import re
from Data_Validation.Prediction_Validate import Predict_Data_Validater
from Db_Operations.Insert_test_db import Test_Db_op


class Test_Loader:
    """
    This Class Loads a Dataset from Prediction_Batch_Files.
    Parameters:-
    -----------
    train_folder:- Test Folder Where Test Files are present.
    train_json:-   Schema Testing Json File
    """
    def __init__(self,folder="Prediction_Batch_Files/") -> None:
        self.train_folder=folder
        self.train_json="schema_prediction.json"
    def get_df(self):
        """
        This Function does following operations:-
        a. Data-Validation:-  Are the files in proper format 
        b. Loading Data in Db:- We load the files in My-SQL Database Table
        c. Export Data:-  We export the My-SQL Database Table in .csv file in Datasets/Test.csv file
        """
        train_validater=Predict_Data_Validater(self.train_folder,self.train_json)
        pattern,LengthOfDateStampInFile,LengthOfTimeStampInFile,test_column_names,NumberofColumns=train_validater.Valuesfromschema()
        train_validater.NameFormatCheck(LengthOfDateStampInFile,LengthOfTimeStampInFile)
        train_validater.validate_Column_Length(NumberofColumns)

        test_db=Test_Db_op()
        test_db.create_table(test_column_names)
        test_db.Insert_Data()
        test=test_db.Export()
        return test
        