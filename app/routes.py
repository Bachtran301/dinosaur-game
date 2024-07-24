from flask import Blueprint, render_template, jsonify, send_from_directory, request, current_app
from bson import ObjectId

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../static', path)

@main.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    new_score = {
        'player_name': data['player_name'],
        'score': data['score']
    }
    current_app.db.scores.insert_one(new_score)
    return jsonify({"message": "Nộp điểm thành công"}), 201

@main.route('/high_scores', methods=['GET'])
def get_high_scores():
    try:
        scores = list(current_app.db.scores.find().sort('score', -1).limit(5))
        for score in scores:
            score['_id'] = str(score['_id'])
        return jsonify(scores)
    except Exception as e:
        print(f"Lỗi khi lấy điểm cao: {e}")
        return jsonify({"error": "Không thể lấy điểm cao"}), 500

@main.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Không tìm thấy"}), 404

@main.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Lỗi máy chủ nội bộ"}), 500