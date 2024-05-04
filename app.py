from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "secrettboggle"

boggle_logic = Boggle()

# homepage
@app.route("/")
def gamepage():
    
    # show game board
    board = boggle_logic.make_board()
    session['board'] = board
    # score
    highscore = session.get("highscore", 0)
    attempts = session.get("attempts", 0) 
    
    return render_template("bogglegame.html", board=board,
                           highscore=highscore,
                           attempts=attempts)
    
@app.route("/wordcheck")
def word_check():
    
        #once player inputs word, check to see if it is in dictionary list
        word = request.args["word"]
        board = session["board"]
        
        # returns word if in list
        response = boggle_logic.check_valid_word(board, word) 
        return jsonify({'result': response})
    
@app.route("/final-score", methods=["POST"])
def final_score(): 
    
    # get the user's score 
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    attempts = session.get("attempts", 0) 
    
    # Update the attemps counter, and highscore if there
    session['attempts'] = attempts + 1
    session['highscore'] = max(score, highscore)
    
    # Show highscore if player beat previous score
    return jsonify(brokeRecord=score > highscore)
    

    
    



