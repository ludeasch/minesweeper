from api.game.serializer import GameStateSerializer, GameSerializer, GameObjectSerializer, GameNewSerializer, GameParamSerializer
from game.models import Game
from rest_framework.decorators import action
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

class MineseeperViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Game.objects.none()
    serializer_class = GameSerializer
    ordering_fields = ["date_added"]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id",)

    def get_serializer_context(self):
        return {"user": self.request.user, "request": self.request}

    def get_queryset(self):
        return Game.objects.filter(user_id=self.request.user_id)


    @action(detail=True, methods=("post",))
    def new(self, request, *args, **kwargs):
        serializer = GameNewSerializer(data=request.data)
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
    viewsets.GenericViewSet
):
    queryset = Game.objects.none()
    serializer_class = GameObjectSerializer
    ordering_fields = ["date_added"]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id",)


    @action(detail=True, methods=("post",))
    def mark_as_flag(self, request,  *args, **kwargs):
        serializer = GameParamSerializer(data=request.data)
        game = self.get_object()
        if serializer.is_valid(raise_exception=True):
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            game.mark_flag_at(x, y)
            game.save()
        serializer = GameObjectSerializer(game, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=("post",))
    def mark_as_question(self, request,  *args, **kwargs):
        serializer = GameParamSerializer(data=request.data)
        game = self.get_object()
        if serializer.is_valid(raise_exception=True):
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            game.mark_question_at(x, y)
            game.save()
        serializer = GameObjectSerializer(game, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=("post",))
    def reveal(self, request,  *args, **kwargs):
        serializer = GameParamSerializer(data=request.data)
        game = self.get_object()
        if serializer.is_valid(raise_exception=True):
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            game.make_click(y, x)
        serializer = GameObjectSerializer(game, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)



class MineseeperStateViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet

):
    queryset = Game.objects.none()
    serializer_class = GameStateSerializer
    ordering_fields = ["date_added"]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id",)