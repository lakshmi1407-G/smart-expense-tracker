from django.contrib import admin
from django.urls import path
from tracker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard),   # 👈 change this
    path('add/', views.add_expense),
    path('edit/<int:id>/', views.edit_expense),
path('delete/<int:id>/', views.delete_expense),
]
from django.contrib.auth import views as auth_views

