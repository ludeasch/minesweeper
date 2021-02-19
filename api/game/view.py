from api.game.serializer import GameStateSerializer, GameSerializer, GameObjectSerializer, GameNewSerializer, GameParamSerializer
from game.models import Game
from rest_framework.decorators import action
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import APIException

class MineseeperViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Main Mineseeper API used to:

    list: list the all games by user
    new: action to create a new board game

    this api need the access token used 
    """
    queryset = Game.objects.none()
    serializer_class = GameSerializer
    ordering_fields = ["date_added"]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id",)

    def get_serializer_context(self):
        return {"user": self.request.user, "request": self.request}

    def get_queryset(self):
        return Game.objects.filter(user_id=self.request.user.id)


    @action(detail=False, methods=("post",))
    def new(self, request, *args, **kwargs):
        """
        This action is used to create a new board

        rows: int 
            min value 9
        columns: int 
            min value 9
        mines: int 
            min value 1
        title: char
            title of the board  
        """
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
        return Response(status=status.HTTP_200_OK, data=serializer.data)

class MineseeperObjectViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """
    Mineseeper API used to:
    
    get the Mineseeper instance

    click_box: action to handler the click event

    this api need the access token used 
    """
    queryset = Game.objects.none()
    serializer_class = GameObjectSerializer
    ordering_fields = ["date_added"]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filterset_fields = ("id",)

    def get_object(self):
        try:
            return Game.objects.get(id=self.kwargs.get('pk'), user_id=self.request.user.id)
        except:
            raise APIException

    @action(detail=True, methods=("post",))
    def click_box(self, request,  *args, **kwargs):
        """
        action to handler the click event

        x: int 
            min value 0
        y: int 
            min value 0
        click_type: char
            type of the click that need to be 'flag' 'question' or 'reveal'
        """

        serializer = GameParamSerializer(data=request.data)
        game = self.get_object()
        if serializer.is_valid(raise_exception=True):
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            click_type = serializer.validated_data['click_type']
            try:
                if click_type == 'flag':
                    game.mark_flag_at(x, y)
                elif click_type == 'question':
                    game.mark_question_at(x, y)
                elif click_type == 'reveal':
                    game.make_click(x, y)
                else:
                    data = {"success": False, "msg": "invalid data click type"}
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            except IndexError:
                data = {"success": False, "msg": "invalid point"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            game.save()
        serializer = GameObjectSerializer(game, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)



    @action(detail=True, methods=("post",))
    def set_state(self, request,  *args, **kwargs):
        """
        action to handler the state

        state: int 
            this value just can be   STATE_STARTED : 1 STATE_PAUSED:  2
        """
        serializer = GameStateSerializer(data=request.data)
        game = self.get_object()
        if serializer.is_valid(raise_exception=True):
            if game.state in [4, 5]:
                data = {"success": False, "msg": "the game is finish"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            state = serializer.validated_data['state']
            game.control_state(state)
            game.save()
        serializer = GameObjectSerializer(game, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)