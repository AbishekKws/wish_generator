from django.urls import path
from . import views

urlpatterns = [
    # -- FRONTEND URLs -- #
    path('create/', views.create_wish, name='create_wish'),
    path('surprise/<slug:slug>/', views.surprise_view, name='surprise_view'),

    # -- BACKEND URLs -- #
    path('backend/interactive-wishes/', views.admin_interactive_wish_list, name='admin_interactive_list'),
    path('backend/interactive-wishes/delete/<path:slug>/', views.admin_interactive_delete, name='admin_interactive_delete'),
]