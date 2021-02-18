import json
import random
from django.db import models
from accounts.models import User


class Game(models.Model):
    STATE_NEW = 0
    STATE_STARTED = 1
    STATE_PAUSED = 2
    STATE_TIMEOUT = 3
    STATE_WON = 4
    STATE_LOST = 5
    STATE_CHOICES = (
        (STATE_NEW, 'new'),
        (STATE_STARTED, 'started'),
        (STATE_PAUSED, 'paused'),
        (STATE_TIMEOUT, 'timeout'),
        (STATE_WON, 'won'),
        (STATE_LOST, 'lost'),
    )

    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, blank=True, default='Game')

    board = models.TextField(blank=True, default='', help_text='Board as a JSON matrix. (0-9: adjacent mines, x: mine)')
    player_board = models.TextField(blank=True, default='',
                                    help_text='Board as a JSON matrix. (v: visible, h: hidden, ?: question mark, !: exclamation mark.')
    state = models.IntegerField(choices=STATE_CHOICES, default=STATE_NEW)
    user = models.ForeignKey(User, related_name='games', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        ordering = ('date_added',)

    def __unicode__(self):
        return self.title


    @classmethod
    def create_game(cls, rows, cols, mines, title, user):
        # function to create a new game
        game = Game()
        game.title = title
        board, player_board = cls.new_boards(rows, cols, mines)
        game.board = board
        game.player_board = player_board
        game.user = user
        game.save()
        return game

    @classmethod
    def _inside_board(cls, rows, cols, point):
        # function to check if the point if inside on the board
        y, x = point
        return (x >= 0 and x < cols) and (y >= 0 and y < rows)

    @classmethod
    def _adjacent_points(cls, rows, cols, x, y):
        # function to get adjacent_points
        up = (y - 1, x)
        down = (y + 1, x)
        left = (y, x - 1)
        right = (y, x + 1)
        upper_right = (y - 1, x + 1)
        upper_left = (y - 1, x - 1)
        lower_right = (y + 1, x + 1)
        lower_left = (y + 1, x - 1)
        points = [up, down, left, right, upper_left, upper_right, lower_left, lower_right]
        return [p for p in points if Game._inside_board(rows, cols, p)]

    @classmethod
    def _fill_adjacent(cls, board, rows, cols, x, y):
        # function to fill adjacent
        if board[y][x] != 'x':
            return
        for p in Game._adjacent_points(rows, cols, x, y):
            py, px = p
            if board[py][px] != 'x':
                board[py][px] = str(int(board[py][px]) + 1)

    @classmethod
    def new_boards(cls, rows, cols, mines):
        # function to create a new board
        assert mines < (rows * cols)

        board = [['0' for j in range(cols)] for i in range(rows)]
        player_board = [['h' for j in range(cols)] for i in range(rows)]
        for i in range(mines):
            mine_set = False
            while not mine_set:
                x = random.randint(0, cols - 1)
                y = random.randint(0, rows - 1)
                if board[y][x] != 'x':
                    board[y][x] = 'x'
                    mine_set = True
        for i in range(rows):
            for j in range(cols):
                Game._fill_adjacent(board, rows, cols, j, i)
        return json.dumps(board), json.dumps(player_board)

    def reveal_at(self, x, y):
        # function to reveal the point 
        pboard = json.loads(self.player_board)
        if pboard[y][x] == 'v':
            return
        pboard[y][x] = 'v'
        self.player_board = json.dumps(pboard)
        board = json.loads(self.board)
        rows, cols = len(board), len(board[0])
        if board[y][x] == '0':
            for p in Game._adjacent_points(rows, cols, x, y):
                py, px = p
                self.reveal_at(px, py)

    def is_mine_at(self, x, y):
        # function to check if the point is a mine
        board = json.loads(self.board)
        return (board[y][x] == 'x')

    def is_all_revealed(self):
        # function to check if all the point was revealed
        board = json.loads(self.board)
        pboard = json.loads(self.player_board)
        rows, cols = len(board), len(board[0])
        for i in range(rows):
            for j in range(cols):
                if board[i][j] != 'x' and pboard[i][j] != 'v':
                    return False
        return True

    def mark_flag_at(self, x, y):
        # function to mark a flag 
        board = json.loads(self.player_board)
        board[y][x] = '!'
        self.player_board = json.dumps(board)

    def mark_question_at(self, x, y):
        # function to mark a question 
        board = json.loads(self.player_board)
        board[y][x] = '?'
        self.player_board = json.dumps(board)

    def make_click(self, x, y):
        # function to handler a click
        self.reveal_at(x, y)
        if self.is_mine_at(x, y):
            self.state = self.STATE_LOST
        elif self.is_all_revealed():
            self.state = self.STATE_WON
