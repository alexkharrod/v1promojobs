from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('save_search/', views.save_search, name='save_search'),
    path('saved_searches/', views.saved_searches, name='saved_searches'),
    path('delete_saved_search/<int:pk>/', views.delete_saved_search, name='delete_saved_search'),
]
