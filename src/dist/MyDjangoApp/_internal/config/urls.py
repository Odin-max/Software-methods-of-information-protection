from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_page, name = 'login_page'),
    path('register/', views.register_view, name='register'),
    path('change_password/', views.forgot_password_page, name = "change_password"),
    path('login/', views.login_view, name='login'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin/change_password/', views.admin_change_password, name='admin_change_password'),
    path('admin/add_user/', views.admin_add_user, name='admin_add_user'),
    path('block_user/<int:user_id>/', views.block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('admin_complete_work/', views.admin_complete_work, name='admin_complete_work'), 
    path('handle_password_change/<int:user_id>/', views.handle_password_change, name='handle_password_change'),
    path('toggle_password_restriction/<int:user_id>/', views.toggle_password_restriction, name='toggle_password_restriction'),
    # User URLs
    path('user_panel/', views.user_panel, name='user_panel'),
    path('user/change_password/', views.user_change_password, name='user_change_password'),
    path('user/complete_work/', views.user_complete_work, name='user_complete_work'),
]
