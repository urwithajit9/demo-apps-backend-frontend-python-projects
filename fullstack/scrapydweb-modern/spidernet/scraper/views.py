import requests
from django.http import JsonResponse

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

SCRAPYD_URL = 'http://localhost:6800'

def schedule_spider(request, spider_name):
    project_name = 'spiders_automation_demo'
    response = requests.post(f'{SCRAPYD_URL}/schedule.json', data={
        'project': project_name,
        'spider': spider_name,
    })
    return JsonResponse(response.json())

def list_jobs(request):
    project_name = 'spiders_automation_demo'
    response = requests.get(f'{SCRAPYD_URL}/listjobs.json?project={project_name}')
    return JsonResponse(response.json())
