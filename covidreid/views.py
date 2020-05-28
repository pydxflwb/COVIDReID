from django.http import HttpResponse, Http404
from django.shortcuts import render
import datetime
from django.utils import timezone


# Index
def index(request):
    # Waiting for the functions
    return render(request, 'index.html')


def welcome(request):
    content = {}
    video_name = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6',]
    all_video = []
    for i in range(len(video_name)):
        video_dir = 'source/videos/'+video_name[i]+".mp4"
        one_video = {}
        one_video['name'] = video_name[i]
        one_video['dir'] = video_dir
        all_video.append(one_video)
    content["num"] = len(video_name)
    content["all_video"] = all_video
    return render(request, "welcome.html", content)


def video(request):
    return render(request, "video.html")


def manual(request):
    return render(request, "manual.html")


def about(request):
    return render(request, "about.html")


# def welcome(request):
#     return render(request, "welcome.html")

# def fourOfour(request):
#     return render(request, "error.html")
