# Jhatta Samachar - Backend

This is the backend project for the **Jhatta Samachar** application, developed using Django. Jhatta Samachar is a news summarization platform that would provide you with your preferred news's summary, using Transformers; a typical Neural Network Architecture. Also, it is a news aggregation platform that crawls and gathers news articles from various sources, such as Ekantipur, providing a personalized news feed for users based on their preferences (likes and dislikes). The backend system is responsible for managing user preferences, crawling news from different sources, and storing them in a structured database for easy access.

## Objectives

The primary objectives of this backend project are:

1. **Summarize News Articles**: Automatically generate summaries of news articles using State-of-the-art Transformer model.
2. **Crawl and Aggregate News**: Fetch news articles from sources like Ekantipur and store them in the database.
3. **User Preferences Management**: Enable users to like or dislike news categories, which helps in customizing the news feed based on individual preferences.

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.x
- Git
- Virtualenv (optional but recommended)
- others on `requirements.txt`

### Installation

1. **Clone the repository**:

```bash
git clone https://github.com/darpankattel/jhatta-samachar
cd jhatta-samachar
```

2. **Create and activate a virtual environment**:
For windows systems:

```bash
python -m venv venv
venv/Scripts/activate  # On linux: source venv\bin\activate
```

3. **Install required dependencies**:
```bash
pip install -r requirements.txt
```

4. **Apply migrations**:

```bash
python manage.py migrate
```


5. **Run the development server:**:

```bash
python manage.py runserver
```

6. **Access the application**:

    Open a browser and navigate to: `http://127.0.0.1:8000/`

### Environment Variables

Ensure you set up the required environment variables in your .env file for the Django settings, such as database configuration, secret keys, and any API credentials.

## API Reference

The API follows a RESTful fashion. Token authentication is required for endpoints that need authenticated user access. The token should be sent as an Authorization header in these requests.

### **Authorization**
- **API Key**  
  Key: `Authorization`  
  Value: `Token <your-token-value>`

---

### **Account Endpoints**

#### 1. **Google OAuth Authentication**
**POST** `/api/auth/google/`  
Authenticates the user using Google OAuth2.0. The frontend sends an ID token, which is verified via the Google API.

- **Request Example:**
  ```json
  {
      "id_token": "sample_id_token" // The ID token returned by Google Sign-In
  }

**Response**:
Creates a new user or updates an existing one, returning a Knox token for further authentication.

#### 2. **Hardcoded Login**
**POST** `/api/auth/hardcoded-login/`
Logs in a user with hardcoded credentials (username and password) and returns a Knox token.

**Response**:
Returns a Knox token to authenticate subsequent requests.


#### 3. **Logout**
**POST** `/api/auth/logout/`
Logs out the authenticated user by deleting their Knox token.

**Response**:
Successfully logs the user out.


#### 4. **Update Preferences**
**POST** `/api/auth/preferences/`
Updates the user's preferences, such as liked and disliked categories for news.

Expected JSON Input:
```json
{
    "likes": [12, 13],
    "dislikes": [14, 15]
}
```

**Response**:
Updates the user's preferences successfully.


#### 5. **User Profile**
**GET** `/api/auth/profile/`
Retrieves the authenticated user's profile information.


### News Endpoints
#### 1. **Get News Summary**
**GET** `/api/news/`
Lists news articles based on the user's preferences (liked and disliked categories). Only summaries are provided in the response.

#### 2. **Get News Category**
**GET** `/api/news/category/`
Lists all the available news categories with pagination support.

#### 3. **Generate News MP3**
**GET** `/api/news/mp3/`
Generates and returns an MP3 file containing a summary of the latest news articles.