from django.contrib.staticfiles.urls import staticfiles_urlpatterns
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
    path(
        "comittee", challenge_views.CommitteeView.as_view(), name="committee"
    ),
    path('get_options/', challenge_views.get_options, name='get_options'),
    path("teams", challenge_views.TeamView.as_view(), name="teams"),
    # path("addons", challenge_views.AddOnView.as_view(), name="addon"),
    path("success", core_views.success, name="success"),
    path("not-alloted", core_views.sit_back_relax, name="sit-back-relax"),
    path("committee-json", core_views.get_dependent_dropdown),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )


urlpatterns += staticfiles_urlpatterns()
