import json

import requests
from dateutil.parser import parse
from django.shortcuts import render

from utils.settings import get_config
from .forms import SearchForm


def get_item_from_youtube(query, max_results=10, page_token=None):
    youtube_api_key = get_config()['youtube']['API_KEY']

    # 3. requests 라이브러리를 이용 (pip install requests), get요청으로 데이터를 받아온 후
    params = {
        'part': 'snippet',
        'q': query,
        'maxResults': max_results,
        'key': youtube_api_key,
        'type': 'video',
    }
    if page_token:
        params['pageToken'] = page_token

    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=params)
    result = r.text

    # 4. 해당 내용을 다시 파이썬 객체로 변환
    result_dict = json.loads(result)
    return result_dict


def get_context(result_dict):
    # 5. 이후 내부에 있는 검색결과를 적절히 루프하며 프린트 해주기
    items = result_dict['items']
    next_page_token = result_dict.get('nextPageToken')
    prev_page_token = result_dict.get('prevPageToken')
    video_list = []
    for index, item in enumerate(items):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        published_date = parse(item['snippet']['publishedAt'])
        thumbnail = item['snippet']['thumbnails']['default']['url']
        # defaults = {
        #     'title': title,
        #     'description': description
        # }
        # Video.objects.get_or_create(
        #     video_id=video_id,
        #     defaults=defaults
        # )
        video = {
            'video_id': video_id,
            'description': description,
            'title': title,
            'published_date': published_date,
            'thumbnail': thumbnail,
        }
        video_list.append(video)

    context = {
        'prev_page_token': prev_page_token,
        'next_page_token': next_page_token,
        'video_list': video_list

    }
    return context


def search(request):
    video_list = []
    context = {
        'video_list': video_list
    }

    if request.GET.get('query', '').strip() != '':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            max_results = form.cleaned_data['max_results']
            video_list = get_and_save_item_from_youtube(query, max_results)[0]

            context = {
                'video_list': video_list,
                'form': form
            }
            return render(request, 'video/search.html', context)

    # video_list = get_and_save_item_from_youtube(query, max_results)
    form = SearchForm()
    context = {

        'form': form
    }
    return render(request, 'video/search.html', context)


def prev_page_view(request):
    max_results = request.GET.get('max_result')
    query = request.GET.get('query')
    prev_page_token = get_and_save_item_from_youtube(query, max_results)[2]

    video_list = get_and_save_item_from_youtube(query, max_results, prev_page_token)[0]
    form = SearchForm()

    context = {
        'video_list': video_list,
        'form': form
    }
    return render(request, 'video/search.html', context)


def next_page_view(request):
    max_results = request.GET.get('max_result')
    query = request.GET.get('query')
    next_page_token = get_and_save_item_from_youtube(query, max_results)[1]

    video_list = get_and_save_item_from_youtube(query, max_results, next_page_token)[0]
    form = SearchForm()

    context = {
        'video_list': video_list,
        'form': form
    }
    return render(request, 'video/search.html', context)
