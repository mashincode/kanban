from graphene import ObjectType, String, Field, List, Mutation, Boolean
from dynamodb_utils import create_task, read_task, update_task, delete_task, read_all_tasks

class TaskType(ObjectType):
    task_id = String()
    title = String()
    status = String()

class TaskListType(ObjectType):
    tasks = List(TaskType)

class Query(ObjectType):
    task = Field(TaskType, task_id=String(required=True))
    tasks = Field(TaskListType)

    def resolve_task(self, info, task_id):
        task = read_task(task_id)
        if 'error' in task:
            raise Exception(task['error'])
        return TaskType(
            task_id=task['task_id']['S'],
            title=task['title']['S'],
            status=task['status']['S']
        )

    def resolve_tasks(self, info):
        all_tasks = read_all_tasks()
        if 'error' in all_tasks:
            raise Exception(all_tasks['error'])
        return TaskListType(
            tasks=[
                TaskType(
                    task_id=task['task_id']['S'],
                    title=task['title']['S'],
                    status=task['status']['S']
                ) for task in all_tasks
            ]
        )

class CreateTask(Mutation):
    class Arguments:
        task_id = String(required=True)
        title = String(required=True)
        status = String(required=True)

    Output = TaskType

    def mutate(self, info, task_id, title, status):
        response = create_task(task_id, title, status)
        if 'error' in response:
            raise Exception(response['error'])
        return TaskType(task_id=task_id, title=title, status=status)

class UpdateTask(Mutation):
    class Arguments:
        task_id = String(required=True)
        title = String()
        status = String()

    Output = TaskType  # Change to return TaskType

    def mutate(self, info, task_id, title=None, status=None):
        response = update_task(task_id, title, status)
        if 'error' in response:
            raise Exception(response['error'])
        # Assuming `update_task` returns the updated task details
        return TaskType(
            task_id=task_id,
            title=title if title is not None else response.get('title'),
            status=status if status is not None else response.get('status')
        )

class DeleteTask(Mutation):
    class Arguments:
        task_id = String(required=True)

    Output = Boolean

    def mutate(self, info, task_id):
        response = delete_task(task_id)
        if 'error' in response:
            raise Exception(response['error'])
        return True

class Mutation(ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()
