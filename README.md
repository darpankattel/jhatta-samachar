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

This API generates and streams an MP3 file containing a summary of the latest news articles based on the user’s preferences.

**Paginated response is supported via the #1 endpoint for news summary.**

**Response**:
Content Type: *audio/mp3*
Streaming: *The response streams the MP3 file directly.*

#### Example usecase in Flutter
To handle the MP3 file streaming in a Flutter app, we can use the `http` package along with the `audioplayers` package to stream or download the MP3 file.

1. Add the necessary packages to your `pubspec.yaml` file:

```yaml
  dependencies:
  http: ^0.13.3
  audioplayers: ^0.20.1
```

2. Stream the MP3 file in Flutter using http and play it using audioplayers:

```dart
import 'package:http/http.dart' as http;
import 'package:audioplayers/audioplayers.dart';

Future<void> playNewsSummary(String token) async {
  final url = '/api/news/mp3/';
  final headers = {'Authorization': 'Token $token'};

  try {
    final response = await http.get(Uri.parse(url), headers: headers);

    if (response.statusCode == 200) {
      // Initialize audio player
      AudioPlayer audioPlayer = AudioPlayer();
      // Play the streamed MP3 file
      await audioPlayer.play(BytesSource(response.bodyBytes));
    } else {
      print('Failed to load MP3. Status code: ${response.statusCode}');
    }
  } catch (e) {
    print('Error: $e');
  }
}

```

#### Example usecase in React/Next.js
To handle MP3 streaming in React or Next.js, we can use the axios library to fetch the streaming MP3 data, and then the Audio tag or an audio player library like react-audio-player to play it.

1. Install Axios (if not already installed):
```bash
npm install axios
```

2. React code to stream and play the MP3 file:

```jsx
import axios from 'axios';
import { useEffect, useState } from 'react';

const NewsSummaryPlayer = () => {
  const [audioSrc, setAudioSrc] = useState(null);

  useEffect(() => {
    const fetchMP3 = async () => {
      const token = 'YOUR_AUTH_TOKEN';  // Replace with your token
      try {
        const response = await axios.get('/api/news/mp3/', {
          headers: { Authorization: `Token ${token}` },
          responseType: 'blob',  // Ensure the response is treated as a file
        });
        
        // Create a URL for the MP3 file and set it as the audio source
        const url = window.URL.createObjectURL(new Blob([response.data], { type: 'audio/mp3' }));
        setAudioSrc(url);
      } catch (error) {
        console.error('Error fetching the MP3 file:', error);
      }
    };

    fetchMP3();
  }, []);

  return (
    <div>
      {audioSrc ? (
        <audio controls>
          <source src={audioSrc} type="audio/mp3" />
          Your browser does not support the audio tag.
        </audio>
      ) : (
        <p>Loading news summary...</p>
      )}
    </div>
  );
};

export default NewsSummaryPlayer;

```