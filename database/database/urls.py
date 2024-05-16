"""database URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from web.views import account, project, part, bushing, interface, link, winding, user, department
from web.views.load_parts import load_parts, load_interfaces

urlpatterns = [
    # path('', account.login),
    # path('accounts/login/', account.login),
    path('login/', account.login),
    path('logout/', account.logout),
    path('img/code/', account.img_code),
    path('home/', account.home),
    path('upload/', account.upload),
    path('check/', account.check),
    path('changePassword/', account.changePassword),

    path('project/list/', project.project_list),
    # path('project/input/', project.project_input),
    path('project/add/', project.project_add),

    # /project/edit/123/
    path('project/edit/<int:aid>/', project.project_edit),

    # /project/delete/?aid=123
    path('project/delete/', project.project_delete),

    path('part/list/', part.part_list),
    # path('part/input/', part.part_input),
    path('part/add/', part.part_add),
    path('part/edit/<int:aid>/', part.part_edit),
    path('part/delete/', part.part_delete),

    path('bushing/list/', bushing.bushing_list),
    # path('bushing/input/', bushing.bushing_input),
    path('bushing/add/', bushing.bushing_add),
    path('bushing/edit/<int:aid>/', bushing.bushing_edit),
    path('bushing/delete/', bushing.bushing_delete),
    path('bushing/load-parts/', load_parts, name='load_parts'),
    path('bushing/add-multiple/', bushing.bushing_add_multiple),

    path('interface/list/', interface.interface_list),
    # path('interface/input/', interface.interface_input),
    path('interface/add/', interface.interface_add),
    path('interface/edit/<int:aid>/', interface.interface_edit),
    path('interface/delete/', interface.interface_delete),
    path('interface/load-parts/', load_parts, name='load_parts'),
    path('interface/add-multiple/', interface.interface_add_multiple),

    path('link/list/', link.link_list),
    # path('link/input/', link.link_input),
    path('link/add/', link.link_add),
    path('link/edit/<int:aid>/', link.link_edit),
    path('link/delete/', link.link_delete),
    path('link/load-parts/', load_parts, name='load_parts'),
    path('link/load-interface/', load_interfaces, name='load_interfaces'),
    path('link/add-multiple/', link.link_add_multiple),

    path('user/list/', user.user_list),
    path('user/edit/<int:aid>/', user.user_edit),
    path('user/delete/', user.user_delete),
    path('user/add-multiple/', user.user_add_multiple),

    path('department/list/', department.department_list),
    path('department/edit/<int:aid>/', department.department_edit),
    path('department/delete/', department.department_delete),
    path('department/add-multiple/', department.department_add_multiple),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)