from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

from django.contrib import messages
from pybo.utils import validate_uploaded_files
from pybo.exceptions import FileTooLargeException

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                validate_uploaded_files(request.FILES)

                question = form.save(commit=False)
                question.author = request.user
                question.create_date = timezone.now()
                question.save()
                return redirect('pybo:index')

            except FileTooLargeException as e:
                messages.error(request, str(e))
                return render(request, 'pybo/question_form.html', {'form': form})
    else:
        form = QuestionForm()
    return render(request, 'pybo/question_form.html', {'form': form})

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            try:
                validate_uploaded_files(request.FILES)

                question = form.save(commit=False)
                question.author = request.user
                question.modify_date = timezone.now()
                question.save()
                return redirect('pybo:detail', question_id=question.id)

            except FileTooLargeException as e:
                messages.error(request, str(e))
                return render(request, 'pybo/question_form.html', {'form': form})

    else:
        form = QuestionForm(instance=question)

    return render(request, 'pybo/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')




