from django.urls import path
from . import views, views_admin

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/guru/', views.guru_dashboard, name='guru_dashboard'),
    path('dashboard/siswa/', views.siswa_dashboard, name='siswa_dashboard'),
    path('dashboard/proktor/', views.proktor_dashboard, name='proktor_dashboard'),
    path('dashboard/waka/', views.waka_dashboard, name='waka_dashboard'),
    
    # Admin Data Master Users
    path('master/user/<str:role>/', views_admin.user_list, name='user_list'),
    path('master/user/<str:role>/create/', views_admin.user_create, name='user_create'),
    path('master/user/<str:role>/<int:pk>/edit/', views_admin.user_edit, name='user_edit'),
    path('master/user/<str:role>/<int:pk>/delete/', views_admin.user_delete, name='user_delete'),
    
    # Import
    path('master/import/<str:role>/', views_admin.import_user, name='user_import'),
    path('master/import/<str:role>/template/', views_admin.download_template_user, name='user_template_download'),
]
