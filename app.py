from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', template_folder='.')

CORS(app)
SCORE_FILE_PATH = 'high_scores.txt'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scores.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    new_score = Score(player_name=data['player_name'], score=data['score'])
    db.session.add(new_score)
    db.session.commit()
    return jsonify({"message": "Score submitted successfully"}), 201

@app.route('/high_scores', methods=['GET'])
def get_high_scores():
    scores = Score.query.order_by(Score.score.desc()).limit(5).all()
    return jsonify([{"player_name": score.player_name, "score": score.score} for score in scores])

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)