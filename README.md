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