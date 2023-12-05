# utils.py
from django.contrib.auth.models import User
from .models import GameHistory,studentHistory
from django.db import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json




def calculate_user_rank():
    # users = User.objects.all()
    users = User.objects.filter(is_superuser=False, is_staff=False)
    ranked_users = []

    for idx, user in enumerate(users, start=1):
        total_games_played = GameHistory.objects.filter(student=user).count()
        total_levels = GameHistory.objects.filter(student=user).aggregate(models.Sum('level_achieved'))['level_achieved__sum'] or 0
        highest_level = GameHistory.objects.filter(student=user).aggregate(models.Max('level_achieved'))['level_achieved__max'] or 0

        # Customize your ranking algorithm based on total_games_played, total_levels, and other criteria
        rank_score = total_games_played + total_levels

        ranked_users.append({'rank':idx,'user': user, 'rank_score': rank_score, 'games_played':total_games_played ,'total_levels':highest_level})

    # Sort users based on rank score in descending order
    ranked_users = sorted(ranked_users, key=lambda x: x['rank_score'], reverse=True)

    return ranked_users


def get_student_game_history(request):  
    history = GameHistory.objects.filter(student=request.user).order_by('-gamedate').values()
    return history



@csrf_exempt
def store_game_history(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            student_id = data.get('student_id')
            level_achieved = data.get('level_achieved', 0)
            total_questions = data.get('total_questions', 0)
            score = data.get('score', 0)
            remarks = data.get('remarks', 'No remarks')

            student = User.objects.get(pk=student_id)

            game_history = GameHistory.objects.create(
                student=student,
                gamedate=timezone.now(),
                level_achieved=level_achieved,
                total_questions=total_questions,
                score=score,
                remarks=remarks
            )

            return JsonResponse({'message': 'Game history stored successfully'}, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)