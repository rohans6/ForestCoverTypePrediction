# Import Necessary Libraries
import os
import shutil
import json
import re
import pandas as pd

class Predict_Data_Validater:
    """
    This Class Validates the Training files
    
    Parameters:-
    ------------
    a. path:- Path where training files are stored.
    b. file_path:- Schema File Path
    
    """
    def __init__(self,path,schema_file_path):
        """
        path:- Path where Files are Located
        schema_file_path:- Path of the Schema File Path
        """
        self.path=path
        self.schema_file_path=schema_file_path
        self.pattern="forest_cover_[\d]+_[\d]+.csv"

    def Valuesfromschema(self):
        """
        This Function retrieves the values from Schema file.
        """
        try:
            with open(self.schema_file_path,'r') as file:
                data=json.load(file)
            pattern = data['SampleFileName']
            LengthOfDateStampInFile = data['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = data['LengthOfTimeStampInFile']
            column_names = data['ColName']
            NumberofColumns = data['NumberofColumns']
            
        except Exception as e:
            print(e)
        return pattern,LengthOfDateStampInFile,LengthOfTimeStampInFile,column_names,NumberofColumns
    
    def deleteExistingGoodFolder(self):
        """
        This Function deletes Good Folder.
        """
        if os.path.isdir("Prediction_Validated_Files/Good/"):
            shutil.rmtree("Prediction_Validated_Files/Good/")

    def deleteExistingBadFolder(self):
        """
        This Function deletes a Bad Folder.
        """
        if os.path.isdir("Prediction_Validated_Files/Bad/"):
            shutil.rmtree("Prediction_Validated_Files/Bad/")

    def createFolders(self):
        """
        This Function created 2 Folders:- a. Good b. Bad
        """
        if not os.path.isdir("Prediction_Validated_Files/Good/"):
            os.mkdir("Prediction_Validated_Files/Good/")
        if not os.path.isdir("Prediction_Validated_Files/Bad/"):
            os.mkdir("Prediction_Validated_Files/Bad/")
    
    def NameFormatCheck(self,LengthOfDateStampInFile,LengthOfTimeStampInFile):
        """
        This Function checks name format of a training files.
        
        Parameters:-
        ------------
        LengthOfDateStampInFile:- Length of Date Stamp from Schema Training File.
        LengthOfTimeStampInFile:- Length of Time Stamp from Schema Training File.
        """
        self.deleteExistingGoodFolder()
        self.deleteExistingBadFolder()
        self.createFolders()
        file_names=list(os.listdir(self.path))
        for file_name in file_names:
            if re.match(self.pattern,file_name):
                names=file_name.split(".csv")[0]
                names=names.split("_")
                if len(names[2])==LengthOfDateStampInFile:
                    if len(names[3])==LengthOfTimeStampInFile:
                        path=shutil.copy(self.path+"/"+file_name,"Prediction_Validated_Files/Good/")
                    else:
                       
                        path=shutil.copy(self.path+"/"+file_name,"Prediction_Validated_Files/Bad/")
                else:
                    
                    path=shutil.copy(self.path+"/"+file_name,"Prediction_Validated_Files/Bad/")
            else:
                
                path=shutil.copy(self.path+"/"+file_name,"Prediction_Validated_Files/Bad/")
    
    def validate_Column_Length(self,number_columns):
        """
        This Function validates number of columns present in csv file.
        
        Parameters:-
        ------------
        number_columns:- Number of Columns that should be present in a file to be a valid file.
        """
        try:
            files=os.listdir("Prediction_Validated_Files/Good/")
            for file in files:
                df=pd.read_csv("Prediction_Validated_Files/Good/"+file)
                if not ((df.shape[1]==number_columns) or (df.shape[1]==55)):
                    path=shutil.move("Prediction_Validated_Files/Good/"+file,"Prediction_Validated_Files/Bad/")    
                else:
                    pass
        except Exception as e:
            print(e)  