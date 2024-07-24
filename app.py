from flask import Flask, render_template, jsonify, send_from_directory, request
from flask_cors import CORS
from bson import ObjectId
from config import config
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='.')

CORS(app)

# Thay đổi URI kết nối để sử dụng MongoDB
env = os.environ.get('FLASK_ENV', 'default')
app.config.from_object(config[env])

# Kiểm tra xem MONGO_URI có được tải đúng không
mongo_uri = os.environ.get('MONGO_URI')
if not mongo_uri:
    raise ValueError("Biến môi trường MONGO_URI không được thiết lập")

print(f"MONGO_URI: {mongo_uri}")  # In ra để kiểm tra

client = MongoClient(mongo_uri)
try:
    client.admin.command('ismaster')
    print("Kết nối MongoDB thành công")
    db = client["dinosaur-game"]
except ConnectionFailure:
    print("Kết nối MongoDB thất bại")
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/submit_score', methods=['POST'])
def submit_score():
    data = request.json
    new_score = {
        'player_name': data['player_name'],
        'score': data['score']
    }
    db.scores.insert_one(new_score)
    return jsonify({"message": "Nộp điểm thành công"}), 201

@app.route('/high_scores', methods=['GET'])
def get_high_scores():
    try:
        scores = list(db.scores.find().sort('score', -1).limit(5))
        for score in scores:
            score['_id'] = str(score['_id'])
        return jsonify(scores)
    except Exception as e:
        print(f"Lỗi khi lấy điểm cao: {e}")
        return jsonify({"error": "Không thể lấy điểm cao"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Không tìm thấy"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Lỗi máy chủ nội bộ"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
