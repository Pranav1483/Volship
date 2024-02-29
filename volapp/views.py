from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from .services import *
import requests
import json
from hashlib import sha256
import logging

logger = logging.getLogger(__name__)


@api_view(['GET'])
def signup(request, email):
    # access_token = request.headers.get('Authorization').split(' ')[1]
    # response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", params={"access_token": access_token})
    # if not response.ok:
    #     logger.warn('Incorrect OAuth Token')
    #     return HttpResponse(status=401)
    # data = response.json()
    # hash_email = sha256(data['email'].encode()).hexdigest()
    hash_email = sha256(email.encode()).hexdigest()
    user, created = Users.objects.get_or_create(email=hash_email)
    user_data = UsersSerializer(user).data
    if created:
        response = JsonResponse(user_data, status=201)
        logger.info(f"OAuth User Created - {user_data['id']}")
        response['Access-Token'], response['Refresh-Token'] = create_token(user_data['email'])
        return response
    else:
        response = JsonResponse(user_data, status=200)
        logger.info(f"OAuth User Login - {user_data['id']}")
        response['Access-Token'], response['Refresh-Token'] = create_token(user_data['email'])
        return response

@api_view(['GET'])
def getUser(request):
    try:
        access_token, refresh_token = request.headers.get('Access-Token'), request.headers.get('Refresh-Token')
        res = verify_tokens(access_token, refresh_token)
        if not res:
            logger.warn('Incorrect JWT Token')
            return HttpResponse(status=401)
        else:
            user = Users.objects.get(email=res['email'])
            current_date = datetime.now(timezone(settings.TIME_ZONE)).date()
            if user.lastPostTime and user.lastPostTime.date() + timedelta(days=1) < current_date:
                user.streak = 0
                user.save()
            user_data = UsersSerializer(user).data
            response = JsonResponse(user_data, status=200)
            response['Access-Token'], response['Refresh-Token'] = res['access'], res['refresh']
            logger.info(f"User Accessed - {user_data['id']}")
            return response
    except Users.DoesNotExist:
        logger.error(f"JWT Token of unavailable User {res['email']}")
        return HttpResponse(status=404)

@api_view(['DELETE'])
def deleteUser(request, id):
    access_token, refresh_token = request.headers.get('Access-Token'), request.headers.get('Refresh-Token')
    res = verify_tokens(access_token, refresh_token)
    if not res:
        logger.warn('Incorrect JWT Token')
        return HttpResponse(status=401)
    else:
        users = Users.objects.filter(id=id)
        if not users.exists():
            logger.error(f"JWT Token of unavailable User {res['email']}")
            return HttpResponse(status=404)
        else:
            user = users.first()
            user.delete()
            logger.info(f"User Deleted - {user['id']}")
            return HttpResponse(status=204)

@api_view(['POST'])
def uploadPost(request):
    access_token, refresh_token = request.headers.get('Access-Token'), request.headers.get('Refresh-Token')
    res = verify_tokens(access_token, refresh_token)
    if not res:
        logger.warn('Incorrect JWT Token')
        return HttpResponse(status=401)
    else:
        users = Users.objects.filter(email=res['email'])
        if not users.exists():
            logger.error(f"JWT Token of unavailable User {res['email']}")
            return HttpResponse(status=404)
        else:
            try:
                user = users.first()
                current_date = datetime.now(timezone(settings.TIME_ZONE)).date()
                if user.lastPostTime and user.lastPostTime.date() + timedelta(days=1) < current_date:
                    user.streak = 0
                data = json.loads(request.body.decode('utf-8'))
                multimedia = data['url']
                description = data['description']
                emotions = {'emotions': data['emotions']}
                answers = {'answers': data['answers']}
                post = Posts(multimedia=multimedia, description=description, user=user, emotions=emotions, answers=answers)
                post.save()
                if not user.lastPostTime or user.lastPostTime.date() != current_date:
                    user.streak += 1
                    user.maxStreak = max(user.maxStreak, user.streak)
                user.lastPostTime = datetime.now(timezone(settings.TIME_ZONE))
                user.save()
                response = HttpResponse(status=204)
                response['Access-Token'], response['Refresh-Token'] = res['access'], res['refresh']
                logger.info(f"User {res['email']} posted content id: {post.id}")
                return response
            except Exception as e:
                logger.error(f"Error uploading post by User {res['email']}\n{e}")
                return HttpResponse(status=400)

@api_view(['PATCH'])
def editCaption(request, id):
    access_token, refresh_token = request.headers.get('Access-Token'), request.headers.get('Refresh-Token')
    res = verify_tokens(access_token, refresh_token)
    if not res:
        logger.warn('Incorrect JWT Token')
        return HttpResponse(status=401)
    else:
        posts = Posts.objects.filter(id=id)
        if not posts.exists():
            logger.warn(f"Patch request by User {res['email']}\nPost {id} does not exist")
            return HttpResponse(status=404)
        else:
            post = posts.first()
            if post.user.email != res['email']:
                logger.error(f"Post {post.id} does not match User {res['email']}")
                return HttpResponse(status=401)
            else:
                new_caption = json.loads(request.body.decode('utf-8'))['caption']
                post.description = new_caption
                post.save()
                response = HttpResponse(status=204)
                response['Access-Token'], response['Refresh-Token'] = res['access'], res['refresh']
                logger.info(f"Post {post.id} updated")
                return response

@api_view(['DELETE'])
def deletePost(request, id):
    access_token, refresh_token = request.headers.get('Access-Token'), request.headers.get('Refresh-Token')
    res = verify_tokens(access_token, refresh_token)
    if not res:
        logger.warn('Incorrect JWT Token')
        return HttpResponse(status=401)
    else:
        posts = Posts.objects.filter(id=id)
        if not posts.exists():
            logger.warn(f"Delete request by User {res['email']}\nPost {id} does not exist")
            return HttpResponse(status=404)
        else:
            post = posts.first()
            if post.user.email != res['email']:
                logger.error(f"Post {post.id} does not match User {res['email']}")
                return HttpResponse(status=401)
            else:
                try:
                    post.delete()
                    response = HttpResponse(status=204)
                    response['Access-Token'], response['Refresh-Token'] = res['access'], res['refresh']
                    logger.info(f"Post {post.id} deleted")
                    return response
                except Exception as e:
                    logger.error(f"Error deleting post by User {res['email']}\n{e}")
                    return HttpResponse(status=500)
        
@api_view(['GET'])
def getUserPosts(request):
    access_token, refresh_token = request.headers.get('Access-Token'), request.headers.get('Refresh-Token')
    res = verify_tokens(access_token, refresh_token)
    if not res:
        return HttpResponse(status=401)
    else:
        users = Users.objects.filter(email=res['email'])
        if not users.exists():
            return HttpResponse(status=404)
        else:
            user = users.first()
            postQuery = Posts.objects.filter(user=user).order_by('timestamp')
            posts = PostsSerializer(postQuery, many=True)
            response = JsonResponse(posts.data, status=200, safe=False)
            response['Access-Token'], response['Refresh-Token'] = res['access'], res['refresh']
            return response
        
@api_view(['GET'])
def getFeedPostsLatest(request):
    access_token, refresh_token = request.headers.get('Access-Token'), request.headers.get('Refresh-Token')
    res = verify_tokens(access_token, refresh_token)
    if not res:
        return HttpResponse(status=401)
    else:
        postQuery = Posts.objects.all().order_by('timestamp')[:20]
        posts = PostsSerializer(postQuery, many=True).data
        response = JsonResponse(posts, status=200, safe=False)
        response['Access-Token'], response['Refresh-Token'] = res['access'], res['refresh']
        return response

@api_view(['POST'])
def getFeedPostsNext(request):
    access_token, refresh_token = request.headers.get('Access-Token'), request.headers.get('Refresh-Token')
    res = verify_tokens(access_token, refresh_token)
    if not res:
        return HttpResponse(status=401)
    else:
        postData = json.loads(request.body.decode('utf-8'))
        postId, postDate = postData['id'], datetime.strptime(postData['timestamp'], '%Y-%m-%dT%H:%M:%S.%f%z')
        postsQuery = Posts.objects.filter(timestamp__lte=postDate, id__lt=postId)
        postsQuery = postsQuery.order_by('-timestamp', 'id')[:20]
        posts = PostsSerializer(postsQuery, many=True).data
        response = JsonResponse(posts, status=200, safe=False)
        response['Access-Token'], response['Refresh-Token'] = res['access'], res['refresh']
        return response
    
@api_view(['POST'])
def likePost(request):
    access_token, refresh_token = request.headers.get('Access-Token'), request.headers.get('Refresh-Token')
    res = verify_tokens(access_token, refresh_token)
    if not res:
        return HttpResponse(status=401)
    else:
        postData = json.loads(request.body.decode('utf-8'))
        postId, userEmail = postData['post'], postData['email']
        if res['email'] != postData['email']:
            return HttpResponse(status=403)
        else:
            post=Posts.objects.get(id=postId)
            post.total_likes += 1
            post.save()
            like, created = Likes.objects.get_or_create(user=Users.objects.get(email=userEmail), post=post)
            return HttpResponse(status=204)