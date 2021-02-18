import json
from django.test import TestCase
from accounts.models import User
from game.models import Game
from rest_framework import status
from rest_framework.test import (
    APIClient
)

class MineseeperTest(TestCase):
    """
    This are the test related to the Mineseeper
    """
    def setUp(self):
        self.client = APIClient()
        self.data_user = {
            'email': 'test@222.com',
            'password': 'andjadjaskjd',
        }
        self.player_b_lost = [
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"],
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"], 
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"], 
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"], 
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"], 
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"], 
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"], 
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"], 
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"], 
            ["h", "h", "h", "h", "h", "h", "h", "h", "h", "h"]
        ]
        self.board_lost =[
            ["x", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "1", "1", "1", "0", "0", "0", "0", "0", "0"], 
            ["0", "1", "x", "2", "1", "0", "0", "0", "0", "0"], 
            ["0", "1", "3", "x", "2", "0", "0", "0", "0", "0"],
            ["0", "0", "2", "x", "2", "0", "0", "0", "0", "0"],
            ["0", "0", "1", "1", "1", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]]

        self.player_b_win = [
            ["v", "v", "v", "v", "v", "v", "v", "v", "v", "v"],
            ["v", "h", "v", "v", "v", "v", "v", "v", "v", "v"], 
            ["v", "v", "h", "v", "v", "v", "v", "v", "v", "v"], 
            ["v", "v", "v", "h", "v", "v", "v", "v", "v", "v"], 
            ["v", "v", "v", "h", "v", "v", "v", "v", "v", "v"], 
            ["v", "v", "v", "v", "v", "v", "v", "v", "v", "v"], 
            ["v", "v", "v", "v", "v", "v", "v", "v", "v", "v"], 
            ["v", "v", "v", "v", "v", "v", "v", "v", "v", "v"], 
            ["v", "v", "v", "v", "v", "v", "v", "v", "v", "v"], 
            ["v", "v", "v", "v", "v", "v", "v", "v", "v", "v"]
        ]
        self.board_win =[
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "1", "1", "1", "0", "0", "0", "0", "0", "0"], 
            ["0", "1", "x", "2", "1", "0", "0", "0", "0", "0"], 
            ["0", "1", "3", "x", "2", "0", "0", "0", "0", "0"],
            ["0", "0", "2", "x", "2", "0", "0", "0", "0", "0"],
            ["0", "0", "1", "1", "1", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
            ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]]
        user = User()
        user.username = "roberto"
        user.email = self.data_user['email']
        user.set_password(self.data_user['password'])
        user.save()

        user2 = User()
        user2.username = "juanc"
        user2.email = 'test2@gmail.com'
        user2.set_password('iajd939udju39dj')
        user2.save()

        self.game = Game.create_game(10, 10, 3, 'title', user)
        self.url = '/api/v1/mineswepper/'
        self.url_new = '/api/v1/mineswepper/new/'
        self.url_login = '/api/v1/accounts/login/'
        self.url_get_game = '/api/v1/mineswepper/game/'+ str(self.game.id) + '/'
        self.url_click_game = '/api/v1/mineswepper/game/'+ str(self.game.id) + '/click_box/'



    def test_pull_board_ok(self):
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.get(self.url)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_pull_boards_fail(self):
        response = self.client.get(self.url)
        res_text = response.json().get('detail')
        self.assertEquals(res_text, 'Authentication credentials were not provided.')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_new_board_ok(self):
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        data_create = {
            'rows': 10,
            'columns': 10,
            'mines': 2,
            'title': 'test board'
        }
        resp = self.client.post(self.url_new, data=data_create)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data.get('title'), 'test board')
        self.assertEquals(resp.data.get('state'), Game.STATE_NEW)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)

    def test_new_boards_with_wrong_data(self):
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        data_create = {
            'rows': 8,
            'columns': 8,
            'mines': 0,
            'title': 'test board'
        }
        resp = self.client.post(self.url_new, data=data_create)
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        content = resp.json()
        self.assertEquals(content.get('rows')[0], 'Ensure this value is greater than or equal to 9.')
        self.assertEquals(content.get('columns')[0], 'Ensure this value is greater than or equal to 9.')
        self.assertEquals(content.get('mines')[0], 'Ensure this value is greater than or equal to 1.')

    def test_new_boards_without_data(self):
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_new)
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        content = resp.json()
        self.assertEquals(content.get('rows')[0], 'This field is required.')
        self.assertEquals(content.get('columns')[0], 'This field is required.')
        self.assertEquals(content.get('mines')[0], 'This field is required.')
        self.assertEquals(content.get('title')[0], 'This field is required.')

    def test_get_board_ok(self):
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.get(self.url_get_game)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data.get('id'), 1)
        self.assertEquals(resp.data.get('title'), 'title')

    def test_get_board_wrong_user(self):
        data_user2 = {
            'email': 'test2@gmail.com',
            'password': 'iajd939udju39dj'
        }
        response = self.client.post(self.url_login, data=data_user2)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.get(self.url_get_game)
        self.assertEquals(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def test_click_event_fail(self):
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_click_game, data={'click_type': 'jdjsj', 'x': 8, 'y':8})
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(resp.json().get('success'), False)
        self.assertEquals(resp.json().get('msg'), 'invalid data click type')

    def test_click_event_wrong_point(self):
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_click_game, data={'click_type': 'reveal', 'x': 12321, 'y':123123})
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(resp.json().get('success'), False)
        self.assertEquals(resp.json().get('msg'), 'invalid point')

    def test_click_event_mark_flag(self):
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_click_game, data={'click_type': 'flag', 'x': 0, 'y':0})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        game = Game.objects.last()
        self.assertEquals(json.loads(game.player_board)[0][0], '!')
        self.assertEquals(json.loads(game.player_board)[1][0], 'h')
        self.assertEquals(json.loads(game.player_board)[0][1], 'h')

    def test_click_event_mark_question(self):
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_click_game, data={'click_type': 'question', 'x': 0, 'y':0})
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        game = Game.objects.last()
        self.assertEquals(json.loads(game.player_board)[0][0], '?')
        self.assertEquals(json.loads(game.player_board)[1][0], 'h')
        self.assertEquals(json.loads(game.player_board)[0][1], 'h')

    def test_click_win_game(self):
        self.game.board = json.dumps(self.board_win)
        self.game.player_board = json.dumps(self.player_b_win)
        self.game.save()
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_click_game, data={'click_type': 'reveal', 'x': 1, 'y':1})
        game = Game.objects.last()
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(game.state, Game.STATE_WON)