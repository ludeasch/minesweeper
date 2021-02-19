from rest_framework import serializers
from game.models import Game
import json


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            'id',
            'date_added',
            'title',
            'updated',
            'state',
            'duration_seconds',
            'total_duration_seconds'
        ]


class GameObjectSerializer(serializers.ModelSerializer):
    board_view = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = [
            'id',
            'date_added',
            'title',
            'updated',
            'board_view',
            'state',
            'duration_seconds',
            'total_duration_seconds'

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


class GameParamSerializer(serializers.Serializer):
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)
    click_type = serializers.CharField()


class GameStateSerializer(serializers.Serializer):
    state = serializers.IntegerField(min_value=1, max_value=2)
