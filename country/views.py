import json
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from jamo import h2j, j2hcj
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .forms import *
from datetime import datetime

URL_LOGIN = '/login/'


def country_list(request):
    countries = Country.objects.values().order_by('country_name')
    countries_dict = alpha_group(countries, 'country_name')

    # print(countries_dict)

    return render(request, 'country/country_list.html', {'countries_dict': countries_dict})


def alpha_group(things, type):
    things_dict = {}
    last_alpha = 'ㄱ'
    things_dict[last_alpha] = []

    for thing in things:
        this_thing = thing.country_name
        this_alpha = j2hcj(h2j(this_thing[0]))[0]
        if last_alpha != this_alpha:     # 직전 초성과 다른 초성
            things_dict[this_alpha] = []
            things_dict[this_alpha].append(thing)
            last_alpha = this_alpha
        else:                           # 같은 초성
            things_dict[this_alpha].append(thing)
    g_cho = 'ㄱ'
    if len(things_dict[g_cho]) == 0:
        del(things_dict[g_cho])
    return things_dict


'''
 위키
'''


def country_wiki(request, pk):
    country = get_object_or_404(Country, pk=pk)
    return render(request, 'country/country_wiki.html', {
        'country': country
    })


@login_required(login_url=URL_LOGIN)
def wiki_edit(request, pk, wiki_type):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            country = form.save()
            return redirect('country:country_wiki', country.pk)
    else:
        form = CountryForm(instance=country)
    return render(request, 'country/wiki_edit.html', {
        'form': form,
        'country': country,
        'type': wiki_type,
    })


'''
 대학 목록
'''


def country_univ(request, pk):
    country = get_object_or_404(Country, pk=pk)
    unives = country.country_univs.all().order_by('away_name')

    univ_dict = alpha_group(unives)

    return render(request, 'country/country_univ.html', {
        'country': country,
        'univ_dict': univ_dict,
    })


'''
 질문
'''


def question_list(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    questions = CQuestion.objects.filter(country=country)
    questions = questions.order_by('-pk')
    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ctx = {
        'page_obj': page_obj,
        'country_id': country_id,
        'country': country,
    }
    return render(request, 'country/question_list.html', context=ctx)


def question_search(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    questions = country.cquestion_set.order_by('-pk')

    q = request.POST.get('q', "")
    searched = questions.filter(question_title__icontains=q)

    paginator = Paginator(searched, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    ctx = {
        'country': country,
        'country_id': country_id,
        'page_obj': page_obj,
        'q': q
    }
    return render(request, template_name='country/question_search.html', context=ctx)


def question_detail(request, country_id, pk):
    country = get_object_or_404(Country, pk=country_id)
    question = CQuestion.objects.get(id=pk)
    comments = question.ccomment_set.all()
    undercomments = CUnderComment.objects.all()
    now = datetime.now()
    ctx = {
        'question': question,
        'comments': comments,
        'country': country,
        'is_authenticated': request.user.is_authenticated,
        'undercomments': undercomments,
        'now': now
    }
    return render(request, template_name='country/question_detail.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def question_create(request, country_id):
    country = get_object_or_404(Country, pk=country_id)
    if request.method == 'POST':
        form = CQuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.country = country
            post.save()
            return redirect('country:question_detail', country_id, post.pk)
    else:
        form = CQuestionForm()
        ctx = {
            'form': form,
            'country': country,
            'is_authenticated': request.user.is_authenticated,
        }
        return render(request, template_name='country/question_form.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def question_edit(request, country_id, pk):
    country = get_object_or_404(Country, pk=country_id)
    question = get_object_or_404(CQuestion, id=pk)
    if request.method == 'POST':
        form = CQuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('country:question_detail', country_id, pk)
    else:
        form = CQuestionForm(instance=question)
        ctx = {
            'form': form,
            'country': country,
            'question': question,
        }
        return render(request, template_name='country/question_form.html', context=ctx)


def question_delete(request, country_id, pk):
    if request.method == 'POST':
        question = CQuestion.objects.get(id=pk)
        question.delete()

    return redirect('country:question_list', country_id)


'''
 댓글
'''


@csrf_exempt
def comment_create(request, country_id, pk):
    req = json.loads(request.body)
    question_id = req['question_id']
    new_comment_content = req['comment_content']

    new_comment = CComment.objects.create(
        question=CQuestion.objects.get(id=question_id),
        comment_content=new_comment_content,
        comment_author=request.user
    )
    new_comment.save()

    return JsonResponse({'question_id': question_id, 'comment_id': new_comment.id, 'comment_content': new_comment_content})


@csrf_exempt
def comment_update(request, country_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    edit_comment_content = req['comment_content']

    edit_comment = CComment.objects.get(id=comment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'comment_content': edit_comment_content, 'nickname': request.user.nickname})


@csrf_exempt
def comment_delete(request, country_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    delete_comment = CComment.objects.get(id=comment_id)
    delete_comment.delete()

    return JsonResponse({'comment_id': comment_id})


@csrf_exempt
def undercomment_create(request, country_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    new_comment_content = req['comment_content']

    new_undercomment = CUnderComment.objects.create(
        comment=CComment.objects.get(id=comment_id),
        comment_author=request.user,
        comment_content=new_comment_content
    )
    new_undercomment.save()

    return JsonResponse({'comment_id': comment_id, 'undercomment_id': new_undercomment.id, 'undercomment_author': request.user.nickname, 'undercomment_content': new_comment_content})


@csrf_exempt
def undercomment_update(request, country_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    undercomment_id = req['undercomment_id']
    edit_comment_content = req['comment_content']

    edit_comment = CUnderComment.objects.get(id=undercomment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'undercomment_id': undercomment_id, 'undercomment_author': edit_comment.comment_author.nickname, 'undercomment_content': edit_comment_content})


@csrf_exempt
def undercomment_delete(request, country_id, pk):
    req = json.loads(request.body)
    undercomment_id = req['undercomment_id']
    delete_comment = CUnderComment.objects.get(id=undercomment_id)
    delete_comment.delete()

    return JsonResponse({'undercomment_id': undercomment_id})
