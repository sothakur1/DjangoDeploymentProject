#we will write the unit test cases for all the API end points in views.py file
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Tweet

from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def _create_user(username='testuser', password='password'):
        return User.objects.create_user(username=username, password=password)
    return _create_user

@pytest.fixture
def create_tweet(create_user):
    user = create_user()
    #add mock image to get rid of following issue: The 'photo' attribute has no file associated with it.
    
    def _create_tweet(text='Test tweet', photo=None):
        if photo is None:
            photo = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        return Tweet.objects.create(user=user, text=text, photo=photo)
    return _create_tweet

def test_index_view(api_client):
    url = reverse('index')  
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

def test_tweet_list_view(api_client, create_tweet):
    create_tweet(text='Tweet 1')
    create_tweet(text='Tweet 2')

    url = reverse('tweet_list')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.context['tweets']) == 2
    
def test_tweet_create_view(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)

    url = reverse('tweet_create')
    data = {
        'text': 'Some New tweet for test',
        'photo': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'), 
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_302_FOUND
    assert Tweet.objects.count() == 1
    assert Tweet.objects.first().text == 'Some New tweet for test'
    
#adding new test cases
def test_tweet_create_view(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user=user)

    url = reverse('tweet_create')
    data = {
        'text': 'New tweet',
        'photo': '',  # Add path to a valid image file if needed
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_302_FOUND
    assert Tweet.objects.count() == 1
    assert Tweet.objects.first().text == 'New tweet'

def test_tweet_edit_view(api_client, create_user, create_tweet):
    user = create_user()
    tweet = create_tweet(text='Original tweet')
    api_client.force_authenticate(user=user)

    url = reverse('tweet_edit', kwargs={'tweet_id': tweet.id})
    data = {
        'text': 'Updated tweet',
        'photo': tweet.photo,
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_302_FOUND
    tweet.refresh_from_db()
    assert tweet.text == 'Updated tweet'

def test_tweet_delete_view(api_client, create_user, create_tweet):
    user = create_user()
    tweet = create_tweet(text='Tweet to delete')
    api_client.force_authenticate(user=user)

    url = reverse('tweet_delete', kwargs={'tweet_id': tweet.id})
    response = api_client.post(url)

    assert response.status_code == status.HTTP_302_FOUND
    assert Tweet.objects.count() == 0

def test_register_view(api_client):
    url = reverse('register')
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password1': 'newpassword',
        'password2': 'newpassword',
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_302_FOUND
    assert User.objects.count() == 1
    assert User.objects.first().username == 'newuser'