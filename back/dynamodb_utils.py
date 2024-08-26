import boto3
from botocore.exceptions import ClientError

TABLE_NAME = 'tasks'

client = boto3.client(
    'dynamodb',
    aws_access_key_id='dummy',
    aws_secret_access_key='dummy',
    region_name='dummy',
    endpoint_url='http://dynamodb:8000'
)

def create_task(task_id, title, status):
    try:
        client.put_item(
            TableName=TABLE_NAME,
            Item={
                'task_id': {'S': task_id},
                'title': {'S': title},
                'status': {'S': status}
            }
        )
        return {"message": f"Task with ID {task_id} created successfully."}
    except ClientError as e:
        return {"error": f"Failed to create task: {e.response['Error']['Message']}"}

def read_task(task_id):
    try:
        response = client.get_item(
            TableName=TABLE_NAME,
            Key={
                'task_id': {'S': task_id}
            }
        )
        if 'Item' in response:
            return response['Item']
        else:
            return {"error": f"Task with ID {task_id} not found."}
    except ClientError as e:
        return {"error": f"Failed to read task: {e.response['Error']['Message']}"}

def update_task(task_id, title=None, status=None):
    update_expression = "SET "
    expression_attribute_values = {}
    expression_attribute_names = {}

    if title:
        update_expression += "#title = :title, "
        expression_attribute_values[':title'] = {'S': title}
        expression_attribute_names['#title'] = 'title'

    if status:
        update_expression += "#status = :status, "
        expression_attribute_values[':status'] = {'S': status}
        expression_attribute_names['#status'] = 'status'

    update_expression = update_expression.rstrip(', ')

    try:
        response = client.update_item(
            TableName=TABLE_NAME,
            Key={
                'task_id': {'S': task_id}
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="UPDATED_NEW"
        )
        return {"message": f"Task with ID {task_id} updated successfully.", "updated_attributes": response['Attributes']}
    except ClientError as e:
        return {"error": f"Failed to update task: {e.response['Error']['Message']}"}

def delete_task(task_id):
    try:
        client.delete_item(
            TableName=TABLE_NAME,
            Key={
                'task_id': {'S': task_id}
            }
        )
        return {"message": f"Task with ID {task_id} deleted successfully."}
    except ClientError as e:
        return {"error": f"Failed to delete task: {e.response['Error']['Message']}"}

def read_all_tasks():
    try:
        response = client.scan(
            TableName=TABLE_NAME
        )
        if 'Items' in response:
            return response['Items']
        else:
            return []
    except ClientError as e:
        return {"error": f"Failed to read all tasks: {e.response['Error']['Message']}"}


def create_table_if_not_exists():
    try:
        client.describe_table(TableName=TABLE_NAME)
        print(f"Table {TABLE_NAME} already exists.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"Table {TABLE_NAME} does not exist. Creating...")
            client.create_table(
                TableName=TABLE_NAME,
                KeySchema=[
                    {
                        'AttributeName': 'task_id',
                        'KeyType': 'HASH' 
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'task_id',
                        'AttributeType': 'S'  
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            print(f"Table {TABLE_NAME} created successfully.")
        else:
            raise

create_table_if_not_exists()





