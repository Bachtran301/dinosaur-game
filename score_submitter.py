import requests

API_URL = "http://localhost:5000"  # Thay đổi URL này khi triển khai lên server thật

def submit_score(player_name, score):
    url = f"{API_URL}/submit_score"
    data = {"player_name": player_name, "score": score}
    try:
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print("Score submitted successfully")
        else:
            print("Failed to submit score")
    except requests.RequestException as e:
        print(f"Error submitting score: {e}")

def get_high_scores():
    url = f"{API_URL}/high_scores"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to get high scores")
            return []
    except requests.RequestException as e:
        print(f"Error getting high scores: {e}")
        return []