from django.conf.urls import include, url
from rest_framework import routers


urlpatterns = [
    url(r"^v1/", include(
            [
                url(r'^accounts/', include('dj_rest_auth.urls')),
                url(r'^accounts/registration/', include('dj_rest_auth.registration.urls'))
            ]
        )
    )
]