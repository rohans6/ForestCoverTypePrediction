import shutil
import mysql.connector as connection
import csv
import os
import pandas as pd

class Train_Db_op:
    """
    This Class loads the Training Files in a My-SQL Table
    
    """
    def __init__(self):
        self.good="Training_Validated_Files/Good/"
        self.bad="Training_Validated_Files/Bad/"
        self.Connection()

    def Connection(self):
        """
        This Function makes a My-SQL Connection
        """
        try:
            mysql=connection.connect(host="127.0.0.1",user="root",password="Rohansans6#")
            cursor=mysql.cursor()
            cursor.execute("DROP DATABASE IF EXISTS ForestCover")
            cursor.execute("CREATE DATABASE IF NOT EXISTS ForestCover")
            if mysql.is_connected():
                print("Sucessfully Connected to My SQL Database")
            
        except Exception as e:
            print(e)
    
    def create_table(self,col_dtypes):
        """
        This Function creates a Table.
        
        Parameters:-
        ------------
        
        col_dtypes:- A dictionary containing Col Names as keys and corresponding data types as values.
        """
        mysql=connection.connect(host="127.0.0.1",user="root",password="Rohansans6#",database="ForestCover")
        cursor=mysql.cursor()
        file=list(os.listdir(self.good))[0]
        df=pd.read_csv(self.good+"/"+file)
        column_names=list(df.columns)

        cursor.execute("USE ForestCover")
        cursor.execute("DROP TABLE IF EXISTS Train")
        try:
            for col in column_names:
                try:
                    query=f"CREATE TABLE Train({col} {col_dtypes[col]})"
                    cursor.execute(query)
                except:
                    query='ALTER TABLE Train ADD COLUMN {col_name} {value}'.format(col_name=col,value=col_dtypes[col])
                    cursor.execute(query)
            mysql.commit()
            mysql.close()
            print("Table Created Sucessfully")
        except Exception as e:
            print(e)
    
    def Insert_Data(self):
        """
        This Function Inserts the Data in my-sql Table.
        """
        files=[file for file in os.listdir(self.good)]
        mysql=connection.connect(host="127.0.0.1",user="root",password="Rohansans6#",database="ForestCover")
        cursor=mysql.cursor()
        cursor.execute("USE ForestCover")
        for file in files:
            
            try:
                with open(self.good+"/"+file,'r') as file_object:
                    next(file_object)
                    data_csv=csv.reader(file_object)
                    for i in data_csv:
                       

                        
                        query=",".join([b for b in i[:]])
                       
                        cursor.execute(f'INSERT INTO Train values ({query})')
                        
                          
            except Exception as e:
                print(e)
        print("All Files Loaded")
        mysql.commit()
        mysql.close()
    
    def Export(self,subset="Train"):
        """
        This Function exports the data in my-sql table to a csv file
        """
        mysql=connection.connect(host="127.0.0.1",user="root",password="Rohansans6#",database="ForestCover")
        cursor=mysql.cursor()
        cursor.execute("USE ForestCover")
        query="SELECT * FROM Train"
        df=pd.read_sql(query,mysql)
        df=df.drop_duplicates()
        if os.path.isfile("Datasets/Train.csv"):
            os.remove("Datasets/Train.csv")
        df.to_csv("Datasets"+"/"+"Train.csv",index=None)
        mysql.close()
        return df