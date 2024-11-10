from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from django.contrib.auth.models import User
from knox.models import AuthToken
from .models import CustomUser
from knox.views import LogoutView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer, CreatePreferenceSerializer

from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken


class UserLogoutView(LogoutView):
    """
    Logs out the user and deletes the Knox token.
    """
    pass


class GoogleAuthView(APIView):
    """
    Authenticates the user using Firebase OAuth2.0.

    The view receives an ID token from the frontend and verifies it using the Google API.

    If the token is valid, the view creates a new user or updates an existing one and generates a Knox token.
    """
    authentication_classes = []  # Disable authentication for this view

    def post(self, request):
        id_token_str = request.data.get('id_token')

        if not id_token_str:
            return Response({'error': 'ID token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # print(f"GOOGLE CLIENT ID: {settings.GOOGLE_CLIENT_ID}")
            idinfo = id_token.verify_firebase_token(
                id_token_str, google_requests.Request()
            )
            # settings.GOOGLE_CLIENT_ID
            google_id = idinfo['sub']
            email = idinfo.get('email')
            name = idinfo.get('name')
            picture = idinfo.get('picture')

            # print(google_id, email, name, picture)
            try:
                user = User.objects.get(username=email)
            except User.DoesNotExist:
                user = User(username=email, email=email)
                user.set_unusable_password()
                if name:
                    full_name = name.split(' ')
                    if len(full_name) > 1:
                        user.last_name = full_name[-1]
                        user.first_name = ' '.join(full_name[:-1])
                    else:
                        user.first_name = name
                user.save()

            # Update or create CustomUser
            custom_user, created = CustomUser.objects.get_or_create(user=user)
            custom_user.google_id = google_id
            custom_user.picture = picture
            custom_user.save()

            # Generate Knox Token
            _, token = AuthToken.objects.create(user)

            return Response({
                'token': token,
                "new_user": created
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            print(e)
            return Response({'error': 'Invalid ID token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    Returns the user's profile information.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        custom_user = CustomUser.objects.get(user=user)
        serializer = CustomUserSerializer(custom_user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PreferenceView(generics.CreateAPIView):
    """
    Updates the user's preferences.

    Expected input format:
    ```
    {
        "likes": [category_id1, category_id2, ...],
        "dislikes": [category_id1, category_id2, ...]
    }
    ```
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreatePreferenceSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        custom_user = CustomUser.objects.get(user=user)

        likes = request.data.get('likes', [])
        dislikes = request.data.get('dislikes', [])
        print(likes, dislikes)

        custom_user.likes.set(likes)

        custom_user.dislikes.set(dislikes)

        # custom_user.save()

        return Response({'message': 'Preferences updated'}, status=status.HTTP_200_OK)


class HardcodedLoginView(APIView):
    """
    Simple view that hardcodes a username and password, 
    authenticates the user and returns a Knox token.
    """
    authentication_classes = []  # Disable authentication for this view
    permission_classes = []  # Disable permission for this view

    def post(self, request, *args, **kwargs):
        hardcoded_username = "darpan"
        hardcoded_password = "darpan"

        user = authenticate(username=hardcoded_username,
                            password=hardcoded_password)

        if user is not None:
            _, token = AuthToken.objects.create(user)
            return Response({
                "token": token
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "error": "Invalid credentials"
            }, status=status.HTTP_401_UNAUTHORIZED)
