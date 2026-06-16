from fastapi import FastAPI
import requests

app = FastAPI(title="PulseBoard API Playground")

# =====================================================
# HOME
# =====================================================
@app.get("/")
def home():
    return {
        "message": "PulseBoard API Running",
        "endpoints": {
            "github_user": "/github/user/octocat",
            "posts": "/posts",
            "create_post": "/posts/create",
            "update_post": "/posts/update",
            "patch_post": "/posts/patch",
            "delete_post": "/posts/delete",
            "weather": "/weather/London"
        }
    }


# =====================================================
# 1. GITHUB API (REAL PUBLIC API)
# =====================================================
@app.get("/github/user/{username}")
def github_user(username: str):

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    return {
        "status_code": response.status_code,
        "data": response.json()
    }


# =====================================================
# 2. JSONPLACEHOLDER - GET POSTS
# =====================================================
@app.get("/posts")
def get_posts():

    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)

    return {
        "status_code": response.status_code,
        "data": response.json()[:5]
    }


# =====================================================
# 3. JSONPLACEHOLDER - CREATE POST (POST)
# =====================================================
@app.post("/posts/create")
def create_post():

    url = "https://jsonplaceholder.typicode.com/posts"

    payload = {
        "title": "AI Internship Task",
        "body": "Learning HTTP + REST + FastAPI",
        "userId": 1
    }

    response = requests.post(url, json=payload)

    return {
        "status_code": response.status_code,
        "created": response.json()
    }


# =====================================================
# 4. JSONPLACEHOLDER - UPDATE (PUT)
# =====================================================
@app.put("/posts/update")
def update_post():

    url = "https://jsonplaceholder.typicode.com/posts/1"

    payload = {
        "id": 1,
        "title": "Updated Title",
        "body": "Updated using PUT",
        "userId": 1
    }

    response = requests.put(url, json=payload)

    return {
        "status_code": response.status_code,
        "updated": response.json()
    }


# =====================================================
# 5. JSONPLACEHOLDER - PATCH
# =====================================================
@app.patch("/posts/patch")
def patch_post():

    url = "https://jsonplaceholder.typicode.com/posts/1"

    payload = {
        "title": "Only title updated via PATCH"
    }

    response = requests.patch(url, json=payload)

    return {
        "status_code": response.status_code,
        "patched": response.json()
    }


# =====================================================
# 6. JSONPLACEHOLDER - DELETE
# =====================================================
@app.delete("/posts/delete")
def delete_post():

    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.delete(url)

    return {
        "status_code": response.status_code,
        "message": "Fake delete (JSONPlaceholder does not actually delete)",
        "response": response.text
    }


# =====================================================
# 7. OPENWEATHER API 
# =====================================================
@app.get("/weather/{city}")
def get_weather(city: str):

    API_KEY = "a06ae94b7714ec0bf0fc1496b9191b50"

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    return {
        "status_code": response.status_code,
        "city": city,
        "data": response.json()
    }