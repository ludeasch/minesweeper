import json
import time
from django.utils import timezone
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
        self.url_set_state = '/api/v1/mineswepper/game/'+ str(self.game.id) + '/set_state/'



    def test_pull_board_ok(self):
        """
        Test try to pull  boards success
        """
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.get(self.url)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(len(resp.json()), 1)
        self.assertEquals(resp.json()[0].get('title'), 'title')
        

    def test_pull_boards_fail(self):
        """
        Test try to pull  boards without credencials
        """
        response = self.client.get(self.url)
        res_text = response.json().get('detail')
        self.assertEquals(res_text, 'Authentication credentials were not provided.')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_new_board_ok(self):
        """
        Test try to create a new board success
        """
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
        self.assertEquals(Game.objects.all().count(), 2)
        self.assertTrue(Game.objects.filter(user__email=self.data_user['email']).exists())

    def test_new_boards_with_wrong_data(self):
        """
        Test try to create a new board with invalid data
        """
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
        """
        Test try to create a new board without data
        """
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
        """
        Test try to get a objects game success
        """
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.get(self.url_get_game)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data.get('id'), 1)
        self.assertEquals(resp.data.get('title'), 'title')

    def test_get_board_wrong_user(self):
        """
        Test when try to get a objects game from another user
        """
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
        """
        Test when the action click box get wrong params
        """
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_click_game, data={'click_type': 'jdjsj', 'x': 8, 'y':8})
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(resp.json().get('success'), False)
        self.assertEquals(resp.json().get('msg'), 'invalid data click type')

    def test_click_event_wrong_point(self):
        """
        Test when you try to revel a wrong point
        """
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_click_game, data={'click_type': 'reveal', 'x': 12321, 'y':123123})
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(resp.json().get('success'), False)
        self.assertEquals(resp.json().get('msg'), 'invalid point')

    def test_click_event_mark_flag(self):
        """
        Test when you try to mark a point as a flag
        """
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
        """
        Test when you try to mark a point as a question
        """
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
        """

        Test when  win the game after to reveal the last point
        """

        self.game.board = json.dumps(self.board_win)
        self.game.player_board = json.dumps(self.player_b_win)
        self.game.date_start_game = timezone.now()
        self.game.save()
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_click_game, data={'click_type': 'reveal', 'x': 1, 'y':1})
        game = Game.objects.last()
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(game.state, Game.STATE_WON)

    def test_click_lose_game(self):
        """

        Test when lost the game after to reveal the last point
        """

        self.game.board = json.dumps(self.board_lost)
        self.game.player_board = json.dumps(self.player_b_lost)
        self.game.date_start_game = timezone.now()
        self.game.save()
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_click_game, data={'click_type': 'reveal', 'x': 0, 'y':0})
        game = Game.objects.last()
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(game.state, Game.STATE_LOST)


    def test_set_state_wrong_data(self):
        """
        Test when try to set state with wrong params
        """
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp = self.client.post(self.url_set_state, data={'state': 7})
        self.assertEquals(resp.status_code, status.HTTP_400_BAD_REQUEST)
        content = resp.json()
        self.assertEquals(content.get('state')[0], 'Ensure this value is less than or equal to 2.')

    def test_set_state_with_game_finish(self):
        """
        Test when try to set state with game lost
        """
        self.game.board = json.dumps(self.board_lost)
        self.game.player_board = json.dumps(self.player_b_lost)
        self.game.date_start_game = timezone.now()
        self.game.save()
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        # set game lost
        resp = self.client.post(self.url_click_game, data={'click_type': 'reveal', 'x': 0, 'y':0})
        game = Game.objects.last()
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(game.state, Game.STATE_LOST)
        # set state
        resp_state = self.client.post(self.url_set_state, data={'state': 1})
        self.assertEquals(resp_state.status_code, status.HTTP_400_BAD_REQUEST)
        content = resp_state.json()
        self.assertEquals(content.get('success'), False)
        self.assertEquals(content.get('msg'), 'the game is finish')
        

    def test_set_state_start(self):
        """
        Test when try to start a game
        """

        
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp_state = self.client.post(self.url_set_state, data={'state': 1})
        self.assertEquals(resp_state.status_code, status.HTTP_200_OK)
        content = resp_state.json()
        self.assertEquals(content.get('state'), Game.STATE_STARTED)


    def test_set_state_pause(self):
        """
        Test when try to pause a game started
        """
        # set game start
        self.game.state = Game.STATE_STARTED
        self.game.date_start_game = timezone.now()
        self.game.save()
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp_state = self.client.post(self.url_set_state, data={'state': 2})
        self.assertEquals(resp_state.status_code, status.HTTP_200_OK)
        content = resp_state.json()
        self.assertEquals(content.get('state'), Game.STATE_PAUSED)
        self.assertIsNotNone(content.get('total_duration_seconds'))
        self.assertIsNotNone(content.get('duration_seconds'))
        self.assertEquals(content.get('total_duration_seconds'), content.get('duration_seconds'))


    def test_set_state_start_to_pause_game(self):
        """
        Test when try to start a game paused
        """
        # set game start
        self.game.state = Game.STATE_PAUSED
        self.game.total_duration_seconds = 3
        self.game.duration_seconds = 3
        self.game.date_start_game = timezone.now()
        self.game.save()
        time.sleep(2)
        response = self.client.post(self.url_login, data=self.data_user)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        key = response.json().get('key')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + key)
        resp_state = self.client.post(self.url_set_state, data={'state': 1})
        self.assertEquals(resp_state.status_code, status.HTTP_200_OK)
        content = resp_state.json()
        
        self.assertEquals(content.get('state'), Game.STATE_STARTED)
        self.assertEquals(content.get('total_duration_seconds'), 5)
        self.assertEquals(content.get('duration_seconds'), 3)



