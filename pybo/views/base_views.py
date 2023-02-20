from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from ..models import Question
from django.db.models import Q

def index(request):
    page = request.GET.get('page', '1') # 페이지
    kw = request.GET.get('kw', '') # 검색어
    what =request.GET.get('what', '')
    searchW = request.GET.get('searchW', '')
    question_list = Question.objects.order_by('-create_date')
    if kw:
        if searchW:
            if searchW == 'question_subject':
                question_list = question_list.filter(subject__icontains=kw)
            elif searchW =='question_content':
                question_list = question_list.filter(content__icontains=kw)
            elif searchW =='question_author':
                question_list = question_list.filter(author__username__icontains=kw)
            elif searchW =='answer_content':
                question_list = question_list.filter(answer__content__icontains=kw).distinct()
            elif searchW =='answer_author':
                question_list = question_list.filter(answer__author__username__icontains=kw).distinct()
        else:
            question_list = question_list.filter(
                Q(subject__icontains=kw) |
                Q(content__icontains=kw) |
                Q(answer__content__icontains=kw) |
                Q(author__username__icontains=kw) |
                Q(answer__author__username__icontains=kw)
            ).distinct()
    if what:
        question_list = question_list.filter(
            category__subject=what
        )
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {
        'question_list':page_obj,
        'page': page,
        'kw': kw,
        'searchW': searchW,
    }
    return render(request, 'pybo/index.html', context)

def detail(request, question_id):
    page = request.GET.get('page', '1')

    question = get_object_or_404(Question, pk=question_id)
    answer_list = question.answer_set.order_by('-voter')
    paginator = Paginator(answer_list, 5)
    page_obj = paginator.get_page(page)
    context = {
        'question': question,
        'answer_list': page_obj,
    }
    return render(request, 'pybo/detail.html', context)
