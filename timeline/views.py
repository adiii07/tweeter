from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from timeline.forms import CreatePostForm, SignUpForm, ReplyForm
from timeline.models import *

# Create your views here.

@login_required
def index(request):
    current_user = request.user
    posts = []
    following = []
    # getting current user's following
    for i in current_user.following.all():
        following.append(i.following_user)
    #getting posts with author in following
    for post in Post.objects.all():
        if post.author in following or post.author == current_user:
            posts.append(post)
    posts = posts[::-1]
    return render(request, "timeline/index.html", 
    {'posts': posts,
     'current_user': current_user})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', 
    {'form': form})

@login_required
def like(request, pk):
    post = Post.objects.get(id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return redirect('post', post_id=pk)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            instance = Post(author=request.user, content=form.cleaned_data['content'])
            instance.save()
            return redirect("index")
    else:
        form = CreatePostForm()
    return render(request, "timeline/createpost.html", {'form': form, 'current_user': request.user})

@login_required
def accounts(request, username):
    user = User.objects.get(username=username)
    current_user = request.user
    # following = False

    try:
        UserFollowing.objects.get(user=current_user, following_user=user)
        following = True
    except:
        following = False

    if request.method == "POST" and following == False:
        UserFollowing.objects.create(user=current_user, following_user=user)
        return redirect("accounts", username=username)

    elif request.method == "POST" and following == True:
        UserFollowing.objects.filter(user=current_user, following_user=user).delete()
        return redirect("accounts", username=username)

    tweets = Post.objects.filter(author=current_user)


    return render(request, "registration/account.html", {
        "user": user,
        "current_user": current_user,
        "following": following,
        "tweets": tweets[::-1]
    })

@login_required
def following(request, username):
    following = []
    for i in User.objects.get(username=username).following.all():
        following.append(i.following_user)
    return render(request, "registration/following.html", {"following": following, "current_user":request.user})

@login_required
def followers(request, username):
    followers = []
    for i in User.objects.get(username=username).followers.all():
        followers.append(i.user)
    return render(request, "registration/followers.html", {"followers": followers, "current_user":request.user})

@login_required
def post(request, post_id):
    post = Post.objects.get(id=post_id)
    replies = Reply.objects.filter(post=post)
    likes = post.count_likes()
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    return render(request, "timeline/post.html", {
        "post": post,
        "replies": replies[::-1],
        "current_user": request.user,
        "total_likes": likes,
        "liked": liked,
    })

@login_required
def new_reply(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            instance = Reply(author=request.user, content=form.cleaned_data['content'], post=post)
            instance.save()
            return redirect("post", post_id=post_id)
    else:
        form = ReplyForm()
    return render(request, "timeline/newreply.html", {'form': form, "current_user":request.user})