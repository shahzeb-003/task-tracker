from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Task
import json
from django.views.decorators.csrf import csrf_exempt

# Responsible for handling the list of tasks
@csrf_exempt
@require_http_methods(['GET', 'POST'])
def task_list(request):
    """
    Handle the list of tasks.
    Supports GET to retrieve a list of tasks and POST to create a new task.
    """

     
    if request.method == 'GET':
        tasks = Task.objects.all()
        task_list = [{'id': task.id, 'title': task.title, 'due_date': task.due_date, 'priority': task.priority, 'email': task.email} for task in tasks]
        return JsonResponse(task_list, safe=False)
     
    elif request.method == 'POST':
        data = json.loads(request.body)
        new_task = Task(title=data['title'], due_date=data['due_date'], priority=data['priority'], email=data['email'])
        new_task.save()
        return JsonResponse({'message': 'Task created successfully'}, status=201)

@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def task_detail(request, task_id):
    """
    Handle a single task.
    Supports GET to retrieve a task, PUT to update a task, and DELETE to delete a task.
    """

    try:
        
        #retrieve a task from the database, It attempts to find a task with the primary key sepcidifed by the 'pk' variable.
        task = Task.objects.get(pk=task_id)

    except Task.DoesNotExist:

        #returns a JSON response to the client with status 404.
        return JsonResponse({'error': 'Task not found'}, status=404)
    
    if request.method == 'GET':

        #gets the data and returns a JSON response with the data
        data = {'id': task.id, 'title': task.title, 'due_date': task.due_date, 'priority': task.priority, 'email': task.email}
        return JsonResponse(data)
    
    #updates the task
    elif request.method == 'PUT':

        #parses the JSON data in the request body. request body contains the raw data sent from the client.
        data = json.loads(request.body)

        #updates the task object with the data
        task.title = data['title']
        task.due_date = data['due_date']
        task.priority = data.get('priority', 0)
        task.email = data.get('email', '')

        #saves the task
        task.save()

        #responds with successful message
        return JsonResponse({'message': 'Task updated successfully'})
    
    elif request.method =='DELETE':

        #deletes the task
        task.delete()

        return JsonResponse({'message': 'Task deleted successfully'}, status=204)