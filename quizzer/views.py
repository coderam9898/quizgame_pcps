from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate  
from django.contrib.auth import logout
from django.contrib import messages
from .gameview import calculate_user_rank,get_student_game_history
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

def logout_view(request):
    logout(request)
    return redirect('/')

def login_page(request):
    try:
        if request.method == 'POST':
            email = request.POST['username']
            password = request.POST['password']
            print(email,password)
            user = authenticate(username=email, password=password)
            print(user)
            if user is not None:
                print("user exists")
                res = login(request, user)
                print(res)

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
                return render(request,'main/index.html',{})    
                
                # return render(request, '/', {'error_message': 'Invalid login credentials'})

        # If it's not a POST request, render the login page
        return render(request,'main/index.html',{})
        # return redirect('/')
    except Exception as e:
        print(e)
        messages.error(request, 'Something went wrong register for new account')
        return render(request,'main/index.html',{})


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
