from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

# TODO -- write tests for every view function / feature!

class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))
            self.assertIn(b'<p>High Score:', response.data)
            self.assertIn(b'Score:', response.data)
            self.assertIn(b'Seconds Left:', response.data)

    def test_valid_word(self):
        """Test if word is valid by modifying the board in the session"""

        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["H", "E", "L", "L", "O"], 
                                 ["W", "O", "R", "L", "D"], 
                                 ["F", "R", "I", "E", "N"], 
                                 ["D", "S", "H", "I", "P"], 
                                 ["G", "A", "M", "E", "S"]]
        response = self.client.get('/wordcheck?word=hello')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if word is in the dictionary"""

        self.client.get('/')
        response = self.client.get('/wordcheck?word=abcde')
        self.assertEqual(response.json['result'], 'not-on-board')

    def non_english_word(self):
        """Test if word is on the board"""

        self.client.get('/')
        response = self.client.get(
            '/wordcheck?word=zzz')
        self.assertEqual(response.json['result'], 'not-word')
