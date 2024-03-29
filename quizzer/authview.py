# views.py
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from django.contrib import messages

@csrf_exempt
def register_user(request):
    """ registers user from the post request , from register page

    Args:
        request (user info): gets registrations details of the user

    Returns:
        redirects to game dashboard: redirects to game dashboard after login the user
    """
    if request.method == 'POST':
        try:
            # Extract user data from the form
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password != password2:
                messages.error(request, 'both password no did not matched!')
                # return JsonResponse({'message': 'both password no did not matched'}, status=201)
                return redirect('register_form')
                
            # Check if username, email, and password are provided
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User is already registered')
                # return JsonResponse({'message': 'both password no did not matched'}, status=201)
                return redirect('register_form')
                # return JsonResponse({'message': 'User is already registered '}, status=201)
            
            if username and email and password:
                # Create a new user
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                loguser = authenticate(username=username, password=password)
                print(loguser)
                if loguser:
                    print(loguser)
                    login(request, user)
                    return redirect('game')
                else:
                # Return a success message or any relevant data
                    messages.error(request, 'User registered successfully')
                # return JsonResponse({'message': 'both password no did not matched'}, status=201)
                    return redirect('index')
                    # return JsonResponse({'message': 'User registered successfully'}, status=201)

            # Return an error message if username, email, or password is missing
            return JsonResponse({'error': 'Username, email, and password are required'}, status=400)

        except Exception as e:
            # Handle any other exceptions
            return JsonResponse({'error': str(e)}, status=500)

    # Return an error for non-POST requests
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def register_form(request):
    """Render register page in the browser

    Args:
        request (request): receives request parameter

    Returns:
        register page: renders register page in the browser
    """
    return render(request,'main/quiz/register.html',{})