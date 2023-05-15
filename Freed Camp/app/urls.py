from django.contrib.auth.views import LoginView
from django.urls import path
from django.contrib.auth import views as auth_views

from app import views
from app.views import ProjectView

urlpatterns = [
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('index/<int:id>/', views.index, name='index'),
    path('home', views.home, name='home'),

    path('user_register', views.user_register, name='user_register'),
    path('project/', ProjectView.as_view(), name='project'),
    path('copy', views.copy, name='copy'),
    path('accounts/profile/', ProjectView.as_view(), name='profile'),
    path('projects/', views.profile, name='profile'),
    path('log_out', views.log_out, name='log_out'),
    path('profile_update/<int:pk>/', views.profile_update, name='profile_update'),
    path('profile_view', views.profile_view, name='profile_view'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password/password_reset.html"),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view
    (template_name="password/password_reset_sent.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view
    (template_name="password/password_conform.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view
    (template_name="password/password_reset_complete.html"), name='password_reset_complete'),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html')),

    path('test', views.test, name='test'),
    path('index_test', views.index_test, name='index_test'),
    path('delete_list/<int:pk>/', views.delete_list, name='delete_list'),
    path('delete_project_ajax/<int:id>/', views.delete_project_ajax, name='delete_project_ajax'),
    path('task_update/<int:id>/', views.task_update, name='task_update'),
    path('status_update/<int:id>/', views.status_update, name='status_update'),
    path('priority_update/<int:id>/', views.priority_update, name='priority_update'),
    path('assign_update/<int:id>/', views.assign_update, name='assign_update'),
    # path('add_attachment/<int:id>/', views.add_attachment, name='add_attachment'),

]
