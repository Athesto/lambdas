

# Local imports
from Example import say_hello

def lambda_handler(event, context):
    message = say_hello()

    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!',
        'message': message

    }
