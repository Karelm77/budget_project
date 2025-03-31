
from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import save_note, dashboard, delete_note

from . import views

from .views import save_note

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
    path('kontakt/', views.contact, name='kontakt'),
    path('save-note/', save_note, name='save_note'),
    path('', dashboard, name='dashboard'),
    path('delete-note/<int:pk>/', delete_note, name='delete_note'),
    path('cookies/', include('cookie_consent.urls')),



]
