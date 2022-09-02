"""exam_invigilator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.login,name='login'),

    path('signin',views.signin,name='home'),
    
    path('exam_duties',views.exam_duties,name='exam_duties'),
      path('fac_home',views.fac_home,name='fac_home'),
       path("logout",views.logout,name='logout'),
        path("admin_home",views.admin_home,name='admin_home'),
        path("admin_fac",views.admin_fac,name='admin_fac'),
         path("admin_room",views.admin_room,name='admin_room'),
          path("admin_exam",views.admin_exam,name='admin_exam'),
          path("edit",views.admin_home,name='edit'),
          path("print_inv",views.print_inv,name='print_inv'),
          path("print_all",views.print_all,name='print_all'),
          path("print_dc",views.print_dc,name='print_dc'),
          path("DUTY",views.DUTY,name='DUTY'),
          path("delete_all",views.delete_all,name='delete_all'),
          path("edit_fac",views.edit_fac,name='edit_fac')
      
]
