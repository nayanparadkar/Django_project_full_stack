from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .forms import TweetForm
from .models import Tweet


# Create your views here.
def index(request):
    return redirect('tweet_list')


def health(request):
    from django.http import JsonResponse

    return JsonResponse({"status": "ok"})


def tweet_list(request):
    tweets_qs = Tweet.objects.all().order_by("-created_at")
    paginator = Paginator(tweets_qs, 10)
    page = request.GET.get("page")
    tweets = paginator.get_page(page)
    return render(request, "tweet_list.html", {"tweets": tweets})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("tweet_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def tweet_create(request):
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest" or request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            if is_ajax:
                html = render_to_string("tweet/_card.html", {"tweet": tweet}, request=request)
                return JsonResponse({"html": html}, status=201)
            return redirect("tweet_list")
        else:
            if is_ajax:
                return JsonResponse({"errors": form.errors}, status=400)
    else:
        form = TweetForm()
    return render(request, "tweet_create.html", {"form": form})


@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("tweet_list")
    else:
        form = TweetForm(instance=tweet)
    return render(request, "tweet_edit.html", {"form": form, "tweet": tweet})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id, user=request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect("tweet_list")
    return render(request, "tweet_delete.html", {"tweet": tweet})
