from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate  
from django.contrib.auth import logout
from django.contrib import messages
from .gameview import calculate_user_rank,get_student_game_history
# Create your views here.
def index(request):
    """ gets request as parameter as render a html page

    Args:
        request (request): a request for indexpage

    Returns:
        html page: renders html page in the clients browser
    """
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('admin:index')
    elif request.user.is_authenticated and not request.user.is_superuser:
        return redirect('game')
    return render (request, 'main/index.html',{})
    # return redirect('game')

def cadmin(request):
    """ Redirects and renders custom admin page

    Args:
        request (request): request the index urls from urls.py file

    Returns:
        render : renders custom admin page
    """
    return render (request,'dashboard/index.html',{})

def game(request):
    """ Redirects and renders the game dashboard page

    Args:
        request (request): request the game urls from urls.py file

    Returns:
        render : renders game dashboard page
    """
    # return render (request,'main/quiz/userdash.html',{})
    return render (request,'main/quiz/landing.html',{})
    # return render (request,'main/quiz/index.html',{})

def play(request):
    """Renders the game page where users play the game

    Args:
        request (request): gets the request from urls

    Returns:
        renders page: users play the game in game page
    """
    return render (request,'main/quiz/test.html',{})

def logout_view(request):
    """Logout's user from the session and destroys the session cookie from the clients computer

    Args:
        request (request): gets user data from request and destroys the user session

    Returns:
         logouts user: destroys the user session
    """
    logout(request)
    return redirect('/')

def login_page(request):
    """Get user's username and password vai post request and validates user and login the user

    Args:
        request (username , password): get username and password via post request

    Returns:
        login user: login the user and creates a user session
    """
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
    """get the leaderboard players data from calculate_user_rank function

    Args:
        request (request): gets user info from the request

    Returns:
        list of users: returns list users ranked based on score
    """
    ranked_users = calculate_user_rank()
    print(ranked_users)
    print("leaderboard")
    return render(request,'main/quiz/leaderboard.html',{'ranked_users': ranked_users})

def history(request):
    """Gets the user's game history

    Args:
        request (request): gets user info from the request

    Returns:
        list of user played games: returns list of games played by the user
    """
    print("history")
    history = get_student_game_history(request)
    print(history)
    return render(request,'main/quiz/history.html',{'history':history})

# rank users
