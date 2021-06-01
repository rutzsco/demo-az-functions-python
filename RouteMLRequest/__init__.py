import os
import json
import pandas as pd
import logging
from requests import status_codes

import azure.functions as func

from . import PythonModelHelperFunctions, RModelHelperFunctions

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Parse HTTP request body and user-provided arguments.
    # These arguments can be used to dynamically modify queries to back-end data stores
    req_body = req.get_json()
    model_type = req_body.get('model_type')
    arg_1 = req_body.get('arg_1')
    arg_2 = req_body.get('arg_2')
    arg_3 = req_body.get('arg_3')

    # Depending upon the value provided for 'model_type'
    # query the relevant data and score using the appropriate model  
    if model_type=='diabetes_python':
        model_data = PythonModelHelperFunctions.GetPythonModelData()
        model_result = PythonModelHelperFunctions.PythonModelInference(model_data)
    elif model_type=='iris_r':
        model_data = RModelHelperFunctions.GetRModelData()
        model_result = RModelHelperFunctions.RModelInference(model_data)

    # Return model prediction results 
    return func.HttpResponse(
        json.dumps(model_result),
        status_code=200
    )
    