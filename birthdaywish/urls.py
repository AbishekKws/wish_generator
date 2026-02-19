from django.urls import path
from . import views

app_name = 'birthday'

urlpatterns = [
    # -- FRONTEND URLs -- #
    path('create/', views.create_wish, name='create_wish'),
    path('success/<slug:slug>/', views.wish_success, name='wish_success'),
    path('view/<slug:slug>/', views.surprise_page, name='surprise_page'),

    # -- BACKEND URLs -- #
    path('admin-panel/wishes/', views.admin_wish_list, name='admin_wish_list'),
    path('admin-panel/wishes/delete/<int:pk>/', views.admin_wish_delete, name='admin_wish_delete'),
]