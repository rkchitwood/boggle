from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """setup before every test"""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_base_route(self):
        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)
            self.assertIn('play_count', session)
            #self.assertEqual(session['high_score'], 0)
            self.assertEqual(session['play_count'], 1)
            self.assertIsNone(session.get('high_score'))
            #a couple tests for HTML
            self.assertIn("<div id='scoretracker'>Your Score: </div>", html)

    def test_word_check(self):
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['B','E','A','R','S'],
                                           ['B','E','A','R','S'],
                                           ['B','E','A','R','S'],
                                           ['B','E','A','R','S'],
                                           ['B','E','A','R','S']]
            response = client.get('/word-check?guess=bear')
            self.assertEqual(response.json, 'ok')
            response = client.get('/word-check?guess=pear')
            self.assertEqual(response.json, 'not-on-board')
            response = client.get('/word-check?guess=qwertyuioplkjhgfdsazxcvbnm')
            self.assertEqual(response.json, 'not-word')

    def test_high_score(self):
        with self.client as client:
            client.get('/high-score?score=12')
            response = client.get('/high-score?score=10')
            self.assertEqual(session['high_score'], 12)
            self.assertEqual(response.status_code, 200)
            response = client.get('high-score?score=13')
            self.assertEqual(session['high_score'], 13)
            self.assertEqual(response.status_code, 200)

    def test_get_high_score(self):
        with self.client as client:
            client.get('/high-score?score=20')        
            response = client.get('/get-high-score')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['high_score'], 20)
                


    # TODO -- write tests for every view function / feature!

