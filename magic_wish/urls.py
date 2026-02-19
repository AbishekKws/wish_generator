from django.urls import path
from . import views

urlpatterns = [
    # -- FRONTEND URLs -- #
    
    # Landing Page
    path('', views.landing_page, name='home'), 
    
    # Wish Creation Flow (Step by Step)
    path('create/', views.select_type, name='select_type'),
    path('create/<str:wish_type>/', views.select_template, name='select_template'),
    path('create/<str:wish_type>/<str:template_name>/', views.create_wish, name='create_wish'),
    
    # SEO Friendly Public Views
    path('wish/<slug:slug>/', views.wish_detail, name='wish_detail'),
    path('success/<slug:slug>/', views.wish_success, name='wish_success'),


    # -- BACKEND (ADMIN) URLs -- #
    
    # Wish Management
    path('backend/wishes/', views.admin_wish_list, name='admin_wish_list'),
    path('backend/wishes/delete/<uuid:pk>/', views.admin_wish_delete, name='admin_wish_delete'),

    # Music Library Management
    path('backend/music/', views.admin_music_list, name='admin_music_list'),
    path('backend/music/delete/<int:pk>/', views.admin_music_delete, name='admin_music_delete'),

    # Template Management
    path('backend/templates/', views.admin_template_list, name='admin_template_list'),
    path('backend/templates/delete/<int:pk>/', views.admin_template_delete, name='admin_template_delete'),
]