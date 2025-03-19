from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    # Přihlašovací URL na /login/ – tato cesta bude použita vždy, když je vyžadováno přihlášení
    path('login/', auth_views.LoginView.as_view(template_name='budget/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Ostatní URL cesty aplikace
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('delete/<int:pk>/', views.delete_transaction, name='delete_transaction'),


]
