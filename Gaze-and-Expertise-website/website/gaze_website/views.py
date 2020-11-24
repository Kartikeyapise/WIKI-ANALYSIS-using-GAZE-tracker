import time
from django.shortcuts import render
import requests
from django.http import StreamingHttpResponse
from GazeTracking.tracker import Tracker

WIKI_API_URL = "https://en.wikipedia.org/w/api.php"

PARAMS = {
    "action": "opensearch",
    "namespace": "0",
    "limit": "10",
    "format": "json"
}


def index(request):
    context = {}
    query = ""
    results = []
    if request.GET:
        query = request.GET['search']
        query = query.strip()
        context['query'] = str(query)
        if query != '':
            params = PARAMS
            params['search'] = query
            json_response = requests.get(
                url=WIKI_API_URL, params=params).json()
            for i in range(len(json_response[1])):
                results.append({
                    'title': json_response[1][i],
                    'description': json_response[2][i],
                    'link': json_response[3][i],
                })
        context['results'] = results
    return render(request, 'index.html', context)


def gen(cam):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


cams = {}
def current_milli_time(): return int(round(time.time() * 1000))


def track(request):
    if request.GET:
        cam_key = request.GET['cam']
        if cam_key:
            cam_key = int(cam_key)
        cam = cams[cam_key]
        cam.stop()

        return render(request, 'processing.html')
    context = {}
    now = current_milli_time()
    new_tracker = Tracker()
    cams[now] = new_tracker
    context['cam'] = now
    return render(request, 'track.html', context)


def tracker_feed(request):
    try:
        cam_key = request.GET['cam']
        if cam_key:
            cam_key = int(cam_key)
        else:
            now = current_milli_time()
            new_tracker = Tracker()
            cams[now] = new_tracker
            cam_key = now

        return StreamingHttpResponse(gen(cams[cam_key]), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
