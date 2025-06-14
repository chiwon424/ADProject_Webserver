from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from ..models import Question, Bookmark
from django.shortcuts import render
from django.core.paginator import Paginator



@login_required(login_url='common:login')
def toggle_bookmark(request, question_id):
    if request.method != 'POST':
        return HttpResponse("POST 요청만 허용됩니다.", status=405)

    question = get_object_or_404(Question, id=question_id)
    bookmark = Bookmark.objects.filter(user=request.user, question=question).first()

    if bookmark:
        bookmark.delete()
        return HttpResponse("북마크가 삭제되었습니다.", status=200)
    else:
        Bookmark.objects.create(user=request.user, question=question)
        return HttpResponse("북마크가 추가되었습니다.", status=201)

@login_required(login_url='common:login')
def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('question').order_by('-id')
    questions = [bookmark.question for bookmark in bookmarks]
    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page', 1)
    question_list = paginator.get_page(page_number)
    return render(request, 'pybo/bookmark_list.html', {
        'question_list': question_list,
        'sort': '',
    })