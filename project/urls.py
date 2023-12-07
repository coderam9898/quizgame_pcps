from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from quizzer.views import logout_view
# import debug_toolbar

urlpatterns = [
    path('admin/logout/', logout_view, name='admin_logout'),
    path('admin/', admin.site.urls,name='admin'),
    path('',include('quizzer.urls'),name='quizzer'),
    path('api/',include('quizzer.api.urls'),name='quizapi'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += path('__debug__/', include(debug_toolbar.urls)),