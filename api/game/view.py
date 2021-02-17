from api.game.serializer import GameStateSerializer, GameSerializer, GameObjectSerializer
from game.models import Game
from rest_framework.decorators import action

class MineseeperViewSet(
    mixins.ListModelMixin,
):
    queryset = Game.objects.none()
    serializer_class = GameSerializer
    ordering_fields = ["date_added"]
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id",)

    def get_serializer_context(self):
        return {"user": self.request.user, "request": self.request}

    def get_queryset(self):
        return Game.objects.filter(user_id=self.request.user_id)


    @action(details=True methods=['post'])
    def new(self, request, *args, **kwargs):
        serializer = GameNewSerializer(data=request.data)
        game = None
        user = request.user
        if serializer.is_valid(raise_exception=True):
            game = Game.create_game(
                serializer.validated_data['rows'],
                serializer.validated_data['columns'],
                serializer.validated_data['mines'],
                serializer.validated_data['title'],
                user
            )
        serializer = GameSerializer(game, context={'request': request})
        return Response(serializer.data)


class MineseeperObjectViewSet(
    mixins.RetrieveModelMixin,
):
    queryset = Game.objects.none()
    serializer_class = GameObjectSerializer
    ordering_fields = ["date_added"]
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id",)



class MineseeperStateViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,

):
    queryset = Game.objects.none()
    serializer_class = GameStateSerializer
    ordering_fields = ["date_added"]
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id",)