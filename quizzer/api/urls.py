from django.urls import path
from .import views
urlpatterns = [
    path('savelevel',views.handle_game_activity,name='userlevel'),
    # path('savelevel',views.testlevel,name='userlevel')
]