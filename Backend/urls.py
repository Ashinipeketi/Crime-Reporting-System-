# crimeapp/urls.py

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    # path('signout', views.signout),
    path('report', views.report, name='report'),
    path('fetch', views.fetch, name="fetch"),
    path('delete/<str:username>/', views.delete, name="delete"),
    path('update/<int:case_id>/', views.update, name="update"),
    # Police URLs
    path('police/register/', views.police_register, name='police_register'),
    path('police/login/', views.police_login, name='police_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

