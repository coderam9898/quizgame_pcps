from django.urls import path
from .import views,authview
urlpatterns = [
    path('',views.index, name='index'),
    path('cadmin',views.cadmin, name='cadmin'),
    path('game',views.game, name='game'),
    path('play',views.play, name='play'),
    path('login_page',views.login_page, name='login_page'),
    path('logout_view',views.logout_view, name='logout_view'),
    path('leaderboard',views.leaderboard, name='leaderboard'),
    path('history',views.history, name='history'),
    path('register',authview.register_user, name='register'),
    path('signup',authview.register_form, name='register_form'),
]