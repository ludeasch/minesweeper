from django.conf.urls import include, url
from rest_framework import routers
from api.game import view as game_views

router = routers.DefaultRouter()
router.register(r"mineswepper", game_views.MineseeperViewSet)
router.register(r"mineswepper/game", game_views.MineseeperObjectViewSet)
router.register(r"mineswepper/state", game_views.MineseeperStateViewSet)


urlpatterns = [
    url(r"^v1/", include(
            [
                url(r"^", include(router.urls)),
                url(r'^accounts/', include('dj_rest_auth.urls')),
                url(r'^accounts/registration/', include('dj_rest_auth.registration.urls'))
            ]
        )
    )
]