from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.contrib.auth import login
# Create your views here.
def index(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin:index')
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('game')
    return render (request, 'main/index.html',{})
    # return redirect('game')

def cadmin(request):
    return render (request,'dashboard/index.html',{})

def game(request):
    # return render (request,'main/quiz/userdash.html',{})
    return render (request,'main/quiz/landing.html',{})
    # return render (request,'main/quiz/index.html',{})

def play(request):
    return render (request,'main/quiz/test.html',{})


def login():
    return HttpResponse("user logged in")




from django.contrib.auth import login, authenticate  # add to imports

# def login_page(request):
#     if request.method == 'POST':
#        username =  request.POST['username']
#        password =  request.POST['password']
#        print(username,password)
#        user = authenticate(
#                 email=username,
#                 password=password,
#        )
#     if user is not None:
#         login(request, user)
#         return render(request, 'main/quiz/index.html', context={})
#         # message = f'Hello {user.username}! You have been logged in'
#     else:
#         # message = 'Login failed!'
#         return redirect('/')

from django.contrib.auth import logout
from django.contrib import messages
def logout_view(request):
    logout(request)
    return redirect('/')



def login_page(request):
    if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        print(email,password)
        user = authenticate(username=email, password=password)
        print(user)



        if user is not None:
            print("user exists")
            login(request, user)

            if user.is_staff and user.is_superuser:
                # Redirect to a staff dashboard or page
                return redirect('admin:index')
            elif user.is_staff and not user.is_superuser:
                return redirect('cadmin')
            else:
                # Redirect to a regular user dashboard or page
                return redirect('game')
        else:
            print("user does not exists")
            messages.error(request, 'Invalid username or password. Please try again.')
            # Handle invalid login here, e.g., display an error message
            return redirect('/')
            # return render(request, '/', {'error_message': 'Invalid login credentials'})

    # If it's not a POST request, render the login page
    return render(request, '/')

from .gameview import calculate_user_rank,get_student_game_history
def leaderboard(request):
    ranked_users = calculate_user_rank()
    print(ranked_users)
    print("leaderboard")
    return render(request,'main/quiz/leaderboard.html',{'ranked_users': ranked_users})

def history(request):
    print("history")
    history = get_student_game_history(request)
    print(history)
    return render(request,'main/quiz/history.html',{'history':history})

# rank users
