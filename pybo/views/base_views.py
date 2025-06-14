from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from ..models import Question, Bookmark
import os


def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')
    auto = request.GET.get('auto', 'off')  # 추천 필터용

    # 기본 queryset: 추천 필터 적용
    if auto == 'on':
        question_list = Question.get_recommended_auto()
    else:
        question_list = Question.objects.all()

    # 정렬 적용
    if so == 'recommend':
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # 최신순
        question_list = question_list.order_by('-create_date')

    # 검색 적용
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(author__profile__nickname__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    # 페이징
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)

    context = {
        'question_list': page_obj,
        'page': page,
        'kw': kw,
        'so': so,
        'auto': auto,  # 템플릿에 넘겨서 추천필터 활성화 상태 유지
    }
    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    filename = os.path.basename(question.file.name) if question.file else ''
    is_image = question.file.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')) if question.file else False
    if request.user.is_authenticated :
        is_bookmarked = Bookmark.objects.filter(user=request.user, question=question).exists()
    else:
        is_bookmarked = False

    context = {
        'question': question,
        'filename': filename,
        'is_image': is_image,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'pybo/question_detail.html', context)
