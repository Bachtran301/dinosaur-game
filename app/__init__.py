from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import config
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    
    CORS(app)

    env = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[env])

    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        raise ValueError("Biến môi trường MONGO_URI không được thiết lập")

    print(f"MONGO_URI: {mongo_uri}")  # In ra để kiểm tra

    client = MongoClient(mongo_uri)
    try:
        client.admin.command('ismaster')
        print("Kết nối MongoDB thành công")
        app.db = client["dinosaur-game"]  # Chỉ định cơ sở dữ liệu ở đây
    except ConnectionFailure:
        print("Kết nối MongoDB thất bại")
        raise

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app