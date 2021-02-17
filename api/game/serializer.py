from rest_framework import serializers
from game.models import Game
import json


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'date_added'
            'title',
            'updated'
        ]


class GameObjectSerializer(serializers.ModelSerializer):
    board_view = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'date_added'
            'title',
            'updated',
            'board_view'

        ]


    def get_board_view(self, obj):
        view = []
        board = json.loads(obj.board)
        player_board = json.loads(obj.player_board)
        for i in range(len(board)):
            view_row = []
            for j in range(len(board[i])):
                if player_board[i][j] == 'v':
                    view_row.append(board[i][j])
                elif player_board[i][j] == 'h':
                    view_row.append(' ')
                else:
                    view_row.append(player_board[i][j])
            view.append(view_row)
        return view

class GameNewSerializer(serializers.Serializer):
    rows = serializers.IntegerField(min_value=9)
    columns = serializers.IntegerField(min_value=9)
    mines = serializers.IntegerField(min_value=1)
    title = serializers.CharField()


class GameParamSerializer(serializers.ModelSerializer):
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)


class GameStateSerializer (serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = [
            'state'
        ]

