import json
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from quizzer.models import GameHistory
from django.utils import timezone

def level(request):
    """ made a hello world program to test the initial setup of the django project

    Args:
        request (request): receives request parameter

    Returns:
        httpresponse: returns hello as httpresponse
    """
    return HttpResponse("hello")
    

@csrf_exempt  # Disable CSRF protection for simplicity. In a production environment, handle CSRF properly.
def handle_game_activity(request):
    """ stores the user game activity in gamehistory table

    Args:
        request (post request): gets user game activity in json format

    Returns:
        True or False: if record is saved returns true else return false
    """
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request
            data = json.loads(request.body.decode('utf-8'))

            # Process the game activity data
            user_id = data.get('userId')
            score = data.get('score')
            quiz_level = data.get('quizLevel')

            # Add more processing logic as needed
            print(user_id,score,quiz_level)
            print(request.user.username)
            print(request.user.id)
            tq = int(quiz_level) * 5
            student = User.objects.get(pk=request.user.id)

            game_history = GameHistory.objects.create(
                student=student,
                gamedate=timezone.now(),
                level_achieved=quiz_level,  
                total_questions=tq,
                score=score,
                remarks="good"
            )
            d =game_history.save()
            print(d)

            # Return a JSON response
            response_data = {'status': 'success', 'message': 'Game activity data received successfully'}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def testlevel(request):
    """ gets post request from frontend with game data made for testing

    Args:
        request (user , level , correct, active , totalquestions): gets these from the post request

    Returns:
        json data: maps all the the provided data from post request into json formate and returns it
    """

    if request.method == 'POST':
        user = request.POST.get('user')
        level = request.POST.get('level')
        correct = request.POST.get('correct')
        active = request.POST.get('was_active')
        totalquestion = request.POST.get('totalquestions')

        status = bool(active)
        print(" somethiong")
        print(status)
        if status:
            print("result is true")
        else:
            print("result is false")

        if correct <= totalquestion:
            data = {
                'user':user,
                'level':level,
                'correct':correct,
                'active':active,
                'totalquestion':totalquestion        }
            print(user) 
            return JsonResponse(data)
        else:
            return JsonResponse({
                "data":"invalid request"
            })
    else:
        return HttpResponse(" no data received")