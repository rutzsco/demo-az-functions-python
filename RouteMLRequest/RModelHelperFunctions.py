import os
import pyodbc
import requests
import pandas as pd

# Sample data wrangling function. A single record is queried from Azure SQL DB and 
# returned as a pandas dataframe.
def GetRModelData():
    
    # SQL connection parameters referenced from environment variables
    server = os.environ.get('SQL_SERVER')
    database = os.environ.get('SQL_DATABASE')
    username = os.environ.get('SQL_USERNAME')
    password = os.environ.get('SQL_PASSWORD')
    driver = '{ODBC Driver 17 for SQL Server}'  

    final_data = None
    
    # Execute a query against Azure SQL DB to collect a single row of data
    with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT TOP 1 * FROM Iris ORDER BY NEWID()")
            row = cursor.fetchone()
            while row:
                final_data = row
                row = cursor.fetchone()
 
    # Return queried data as a pandas dataframe
    final_df = pd.DataFrame([list(final_data)], columns = ['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width'])
    return final_df

# Function accepts a pandas dataframe, sends a request to an AML model endpoint, and returns a result.
# Note: deployed R model expects a list of JSON records for inferencing.
def RModelInference(data):

    # Create request headers
    headers = {
        'Content-Type': 'application/json'
    }

    # Send request to AML endpoint
    response = requests.post(url=os.environ.get('R_MODEL_ENDPOINT'), data=data.to_json(orient='records'), headers=headers)
    
    # Return successful results
    if response.status_code==200:
        return response.json()

    # If request is unsuccessful return the error text
    return response.text


