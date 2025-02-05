# Builtins import
import json

# Third party imports
import lxml
import pandas as pd

def lambda_handler(event, context):
    data = {"Nombre": ["Gustavo", "Ana", "Carlos"], "Edad": [30, 25, 35]}
    df = pd.DataFrame(data)

    return {
        "statusCode": 200,
        "body": df.to_json(orient="records")
    }
