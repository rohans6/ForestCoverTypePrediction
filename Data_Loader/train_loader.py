import os
import re
from Data_Validation.Train_Validate import Train_Data_Validater
from Db_Operations.Insert_train_db import Train_Db_op


class Train_Loader:
    """
    This Class Loads a Dataset from Training_Batch_Files.
    Parameters:-
    -----------
    train_folder:- Train Folder Where Training Files are present.
    train_json:-   Schema Training Json File
    """
    def __init__(self) -> None:
        self.train_folder="Training_Batch_Files/"
        self.train_json="schema_training.json"
    def get_df(self):
        """
        This Function does following operations:-
        a. Data-Validation:-  Are the files in proper format 
        b. Loading Data in Db:- We load the files in My-SQL Database Table
        c. Export Data:-  We export the My-SQL Database Table in .csv file in Datasets/Train.csv file
        """
        train_validater=Train_Data_Validater(self.train_folder,self.train_json)
        pattern,LengthOfDateStampInFile,LengthOfTimeStampInFile,train_column_names,NumberofColumns=train_validater.Valuesfromschema()
        train_validater.NameFormatCheck(LengthOfDateStampInFile,LengthOfTimeStampInFile)
        train_validater.validate_Column_Length(NumberofColumns)

        train_db=Train_Db_op()
        train_db.create_table(train_column_names)
        train_db.Insert_Data()
        train=train_db.Export()
        return train
        

