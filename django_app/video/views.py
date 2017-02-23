import json

import requests
from dateutil.parser import parse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

from utils.settings import get_config
from video.models import Video, VideoBookmark


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


def get_context(result_dict, user):
    # 5. 이후 내부에 있는 검색결과를 적절히 루프하며 프린트 해주기
    items = result_dict['items']
    next_page_token = result_dict.get('nextPageToken', '')
    prev_page_token = result_dict.get('prevPageToken', '')
    total_results = result_dict['pageInfo'].get('totalResults')
    video_list = []
    for index, item in enumerate(items):
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        description = item['snippet']['description']
        published_date = parse(item['snippet']['publishedAt'])
        thumbnail = item['snippet']['thumbnails']['default']['url']
        video = {
            'video_id': video_id,
            'description': description,
            'title': title,
            'published_date': published_date,
            'thumbnail': thumbnail,
        }

        is_exist = VideoBookmark.objects.filter(user=user, video__youtube_video_id=video_id)
        # for video_bookmarked in video_bookmarked_list:
        #     video_bm = Video.objects.get(video_id=video_bookmarked.video.video_id)
        #     if video_bm.video_id == video_id:
        if is_exist:
            video['is_bookmarked'] = True
            # defaults = {
            # 'title': title,
            #     'description': description
            # }
            # Video.objects.get_or_create(
            #     video_id=video_id,
            #     defaults=defaults
            # )
        else:
            video['is_bookmarked'] = False
        video_list.append(video)

    context = {
        'prev_page_token': prev_page_token,
        'next_page_token': next_page_token,
        'video_list': video_list,
        'total_results': total_results,
    }
    return context


def search(request):
    video_list = []
    context = {
        'video_list': video_list
    }
    query = request.GET.get('query', '').strip()
    max_results = request.GET.get('max_results')
    page_token = request.GET.get('page_token')
    context['pageToken'] = page_token

    if query != '':
        context = get_context(get_item_from_youtube(query, max_results, page_token), user=request.user)
        context['query'] = query
        context['max_results'] = max_results
    # video_list = get_and_save_item_from_youtube(query, max_results)
    return render(request, 'video/search.html', context)


def bookmark_list(request):
    return render(request, 'video/bookmark.html')


def video_bookmark_toggle(request):
    video_id = request.POST.get('video_id')
    prev_path = request.POST['path']
    if VideoBookmark.objects.filter(video__youtube_video_id=video_id, user=request.user).exists():
        VideoBookmark.objects.get(video__youtube_video_id=video_id, user=request.user).delete()

    else:
        user = request.user
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_id = video_id
        video, _ = Video.objects.get_or_create(youtube_video_id=video_id, title=title, description=description,
                                               is_bookmarked=True)
        video.videobookmark_set.create(user=user)
    return redirect(prev_path)


def bookmark_list(request):
    if __name__ == '__main__':
        all_bookmarks = request.user.videobookmark_set.select_related('video')
        paginator = Paginator(all_bookmarks, 5)
        page = request.GET.get('page')
        try:
            bookmarks = paginator.page(page)
        except PageNotAnInteger:
            bookmarks = paginator.page(1)
        except EmptyPage:
            bookmarks = paginator.page(paginator.num_pages)
        return render(request, 'video/bookmark_list.html', {'bookmarks': bookmarks})
