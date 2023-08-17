"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from Challenge import views as challenge_views
from Core import views as core_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", core_views.Login_View.as_view(), name="login"),
    path("logout/", core_views.logout_user, name="logout"),
    path("", core_views.Home.as_view(), name="home"),
    path("comittee", challenge_views.CommitteeView.as_view(), name="committee"),
    path("teams", challenge_views.TeamView.as_view(), name="teams"),
    path("addons", challenge_views.AddOnView.as_view(), name="addon"),
    path("success", core_views.success, name="success"),
    path("test",core_views.test() ,name="sucess")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
