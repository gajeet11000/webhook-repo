# Techstax GitHub Actions API

This project provides a Flask-based API for tracking and displaying GitHub Actions events (pushes and pull requests) in real time. It is designed to be used with a frontend dashboard (such as the included HTML dashboard) and supports secure GitHub webhook integration.

## API Routes

### 1. `GET /api/actions`

Fetches recent GitHub actions from the database.

**Query Parameters:**

- `recent` (boolean, optional): If true, only fetches actions from the last `interval` seconds.
- `interval` (integer, optional): Time window in seconds for recent actions (default: 15).

**Example:**

```
GET http://localhost:8080/api/actions?recent=true&interval=15
```

**Response:**

- 200 OK: List of action objects (pushes, PRs, etc.)
- 400 Bad Request: Invalid query parameters

### 2. `POST /api/github-webhook`

Receives GitHub webhook events (push, pull_request, etc.).

**Body:**

- Raw JSON payload from GitHub webhook

**Response:**

- 200 OK: Data saved or message about PR closed but not merged
- 400/403/500: Error details

## Project Setup

### 1. Clone the Repository

```sh
git clone https://github.com/gajeet11000/webhook-repo.git
cd webhook-repo
```

### 2. Create and Configure Environment Variables

Create a `.env` file in the project root with the help of `.env.example` provided as sample

### 3. Install Python Dependencies
If you have uv(modern python package manger) installed you can skip this step

```sh
pip install -r requirements.txt
# or, if using pyproject.toml
pip install .
```

### 4. Run the Flask App

```
uv run main.py
```
or 
```sh
python main.py
```

The API will be available at `http://localhost:8080`.

## Setting Up GitHub Webhooks

- Go to your GitHub repository settings > Webhooks > Add webhook
- Payload URL: `http://<your-server>:8080/api/github-webhook`
- Content type: `application/json`
- Secret: Use the same value as `GITHUB_WEBHOOK_SECRET` in your `.env`
- Select events: Pushes and Pull requests (or all events)

## Dependencies

- Python 3.12+
- Flask
- Flask-CORS
- Flask-PyMongo
- Marshmallow
- python-dotenv
- gunicorn (for production)

---