from boggle import Boggle

boggle_game = Boggle()

from flask import Flask, request, render_template, flash, redirect, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
app=Flask(__name__)
app.config['SECRET_KEY']='super secret key'
app.config['TESTING']=True
debug=DebugToolbarExtension(app)

@app.route('/')
def display_board():
    """base route which displays the board to the user UI"""
    board_data = boggle_game.make_board()
    session['board'] = board_data
    games_played = session.get('play_count', 0)
    games_played += 1
    session['play_count'] = games_played
    return render_template('board.html', board_data=board_data)

@app.route('/word-check')
def word_check():
    """checks if user's guess sent via JS is a valid word in the dictionary 
    and/or the board and responds with JSON"""
    guess = request.args['guess']
    board_data=session['board']
    result = boggle_game.check_valid_word(board_data, guess.lower())
    return jsonify(result)

@app.route('/high-score')
def high_score_check():
    """checks if the score is the high score, if so, saves high score"""
    score = int(request.args['score'])
    high_score = session.get('high_score', 0)
    if score > high_score:
        high_score = score
        session['high_score'] = high_score
        data = {'high_score': score, 'score': score}
        return jsonify(data)
    data = {'high_score': high_score, 'score': score}
    return jsonify(data)

@app.route('/get-high-score')
def get_high_score():
    high_score = session.get('high_score', 0)
    data = {'high_score': high_score}
    return jsonify(data)