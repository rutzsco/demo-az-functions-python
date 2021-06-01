import os
import pyodbc
import requests
import json

# Sample data wrangling function. A single record is queried from Azure SQL DB and 
# returned as a pandas dataframe.
def GetPythonModelData():
    
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
            cursor.execute("SELECT TOP 1 * FROM Diabetes ORDER BY NEWID()")
            row = cursor.fetchone()
            while row:
                final_data = row
                row = cursor.fetchone()

    # Return queried data as a list of data
    return list(final_data)
    
# Function accepts a pandas dataframe, sends a request to an AML model endpoint, and returns a result.
# Note: deployed python model expects a JSON payload containing a list of data (list of lists), and a specified method.
def PythonModelInference(data):

    # Create request body and headers
    request_body = json.dumps({
        'data': data,
        'method': 'predict'
    })
    headers = {
        'Content-Type': 'application/json'
    }

    # Send request to AML endpoint
    response = requests.post(url=os.environ.get('PYTHON_MODEL_ENDPOINT'), data=request_body, headers=headers)
    
    # If request is successful return result
    if response.status_code==200:
        return response.json()

    # Otherwise return the error text
    return response.text


