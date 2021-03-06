import json
import re
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import json
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .forms import *
from config.functions import *
from django.core.paginator import Paginator
from datetime import datetime


URL_LOGIN = '/login/'


def univ_list(request):
    unives = Foreign.objects.all().order_by('away_name')
    univ_dict = order_foreign(unives)
    alphaList = [chr(c) for c in range(ord('A'), ord('Z')+1)]
    return render(request, 'foreign/univ_list.html', {
        'univ_dict': univ_dict,
        'alphaList': alphaList,
    })

# 해외 대학 추가


@login_required(login_url=URL_LOGIN)
def univ_search(request):
    if request.method == 'POST':  # newforeign폼 입력시
        form = NewForeignForm(request.POST)
        if form.is_valid():
            univ = form.save()
            return redirect('foreign:univ_list')
        else:
            ctx = {'message': "이미 등록된 대학입니다.", 'form': form, }
    else:
        form = NewForeignForm()
        ctx = {'form': form, }

    return render(request, 'foreign/univ_search.html', context=ctx)


# 해외 대학 추가 폼
@login_required(login_url=URL_LOGIN)
def univ_create(request, univ_name):
    if request.method == 'POST':
        form = NewForeignForm(request.POST)
        if form.is_valid():
            univ = form.save(commit=False)
            univ.save()
            univs = Foreign.objects.filter()
            return redirect('foreign:univ_list')
    else:
        form = NewForeignForm()
        ctx = {
            'form': form,
            'univ_name': univ_name,
        }
        return render(request, template_name='foreign/univ_create.html', context=ctx)


# 자매대학


def sister(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    sisters = foreign.sisters.all().order_by('home_name')
    sisters_dict = order_domestic(sisters)
    ctx = {
        'sisters_dict': sisters_dict,
        'univ': foreign,
    }
    return render(request, 'foreign/sister.html', ctx)

# 자매대학 추가


@login_required(login_url=URL_LOGIN)
def create_sister(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    if request.method == 'POST':
        sister_name = request.POST['sister']
        sister = get_object_or_404(Domestic, home_name=sister_name)
        foreign.sisters.add(sister.id)

        return redirect("foreign:sister", foreign_id)
    else:
        univs = Domestic.objects.all()
    return render(request, 'foreign/create_sister.html', {
        'domestic_univs': univs,
        'univ': foreign
    })

# wiki


def wiki(request, pk):
    univ = Foreign.objects.get(pk=pk)
    ctx = {
        'univ': univ,
    }
    return render(request, 'foreign/wiki.html', ctx)


@login_required(login_url=URL_LOGIN)
def wiki_edit(request, pk, wiki_type):
    foreign = get_object_or_404(Foreign, pk=pk)
    if request.method == 'POST':
        form = ForeignForm(request.POST, request.FILES, instance=foreign)
        if form.is_valid():
            foreign = form.save()
            return redirect('foreign:wiki', foreign.pk)
    else:
        form = ForeignForm(instance=foreign)
    return render(request, 'foreign/wiki_edit.html', {
        'form': form,
        'univ': foreign,
        'type': wiki_type,
    })

# review


def review_list(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    all_review = foreign.reviews.order_by('-pk')
    paginator = Paginator(all_review, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_review = all_review.count()
    ctx = {
        'univ': foreign,
        'page_obj': page_obj,
        'total_review': total_review,
    }
    return render(request, 'foreign/review_list.html', ctx)


def review_detail(request, pk, foreign_id):
    review = get_object_or_404(Post, pk=pk)
    all_comment = review.post_comment.all()
    recomments = FReComment.objects.all()
    foreign = get_object_or_404(
        Foreign, pk=foreign_id)  # 외국 대학과 국가 넘겨주기위해 받음
    if request.user == review.post_author:
        IsReviewAuthor = True
    else:
        IsReviewAuthor = False
    now = datetime.now()
    ctx = {
        'review': review,
        'univ': foreign,
        'all_comment': all_comment,
        'IsReviewAuthor': IsReviewAuthor,
        'recomments': recomments,
        'now': now,
    }
    return render(request, 'foreign/review_detail.html', ctx)


@login_required(login_url=URL_LOGIN)
def review_create(request, foreign_id, post=None):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    IsReviewAuthor = True
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=post)
        form.author_post = request.user
        if form.is_valid():
            review = form.save(commit=False)  # db에 바로 저장되지 않도록
            review.post_author = request.user
            review.foreign = get_object_or_404(Foreign, id=foreign_id)
            review.save()
            return redirect('foreign:review_detail', foreign_id, review.pk)
    else:
        if post != None:                # 수정할 때
            if request.user != post.post_author:
                IsReviewAuthor = False
            post.save()
            type = 'update'
        else:                           # 새로 생성할 때
            type = 'create'
        form = ReviewForm(instance=post)

    return render(request, 'foreign/review_create.html', {
        'form': form,
        'review': post,
        'type': type,
        'univ': foreign,
        'IsReviewAuthor': IsReviewAuthor,
    })


def review_delete(request, pk, foreign_id):
    review = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        review.delete()
    return redirect('foreign:review_list', foreign_id)


@login_required(login_url=URL_LOGIN)
def review_update(request, pk, foreign_id):
    post = get_object_or_404(Post, pk=pk)
    return review_create(request, foreign_id, post)


# Q&A


def question_list(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    questions = FQuestion.objects.filter(away_university=foreign)
    questions = questions.order_by('-pk')
    total_question = questions.count()
    paginator = Paginator(questions, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    ctx = {
        'page_obj': page_obj,
        'total_question': total_question,
        'univ': foreign,
    }
    return render(request, 'foreign/question_list.html', context=ctx)


def question_detail(request, foreign_id, pk):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    question = FQuestion.objects.get(id=pk)
    comments = question.fcomment_set.all()
    undercomments = FUnderComment.objects.all()
    now = datetime.now()
    ctx = {
        'question': question,
        'comments': comments,
        'univ': foreign,
        'is_authenticated': request.user.is_authenticated,
        'undercomments': undercomments,
        'now': now
    }
    return render(request, 'foreign/question_detail.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def question_create(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        form.author_fquestion = request.user
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.away_university = foreign
            post.save()
            return redirect('foreign:question_detail', foreign_id, post.pk)
    else:
        form = QuestionForm()
        ctx = {
            'form': form,
            'univ': foreign,
        }
        return render(request, template_name='foreign/question_form.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def question_edit(request, foreign_id, pk):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    question = get_object_or_404(FQuestion, id=pk)
    IsQuestionAuthor = True
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save()
            return redirect('foreign:question_detail', foreign_id, pk)
    else:
        if question != None:                # 수정할 때
            if request.user != question.author:
                IsQuestionAuthor = False
            type = 'update'
        else:                           # 새로 생성할 때
            type = 'create'
        form = QuestionForm(instance=question)
        ctx = {
            'form': form,
            'univ': foreign,
            'IsQuestionAuthor': IsQuestionAuthor,
            'type': type,
            'question': question,
        }
        return render(request, template_name='foreign/question_form.html', context=ctx)


def question_delete(request, foreign_id, pk):
    question = get_object_or_404(FQuestion, id=pk)
    if request.method == 'POST':
        question.delete()
    return redirect('foreign:question_list', foreign_id)


def question_search(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    questions = foreign.fquestion_set.order_by('-pk')

    q = request.POST.get('q', "")
    searched = questions.filter(question_title__icontains=q)
    total_question = searched.count()

    paginator = Paginator(searched, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user = request.user
    is_enrolled = 'False'
    if user.is_authenticated:
        if user.university == foreign.away_name:
            is_enrolled = 'True'

    ctx = {
        'univ': foreign,
        'page_obj': page_obj,
        'total_question': total_question,
        'is_authenticated': user.is_authenticated,
        'is_enrolled': is_enrolled,
        'q': q
    }
    return render(request, template_name='foreign/question_search.html', context=ctx)

# qna 댓글


@csrf_exempt
@login_required(login_url=URL_LOGIN)
def q_comment_create(request, foreign_id, pk):
    req = json.loads(request.body)
    question_id = req['question_id']
    new_comment_content = req['comment_content']
    is_secret = req['is_secret']

    new_comment = FComment.objects.create(
        question=FQuestion.objects.get(id=question_id),
        comment_content=new_comment_content,
        comment_author=request.user
    )

    new_comment.secret = is_secret
    new_comment.save()

    return JsonResponse({'question_id': question_id, 'comment_id': new_comment.id, 'comment_content': new_comment_content, 'secret': new_comment.secret})


@csrf_exempt
@login_required(login_url=URL_LOGIN)
def q_comment_edit(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    edit_comment_content = req['comment_content']
    edit_comment_secret = req['secret']

    edit_comment = FComment.objects.get(id=comment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.secret = edit_comment_secret
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'comment_content': edit_comment_content, 'nickname': request.user.nickname, 'secret': edit_comment.secret})


@csrf_exempt
def q_comment_delete(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    delete_comment = FComment.objects.get(id=comment_id)
    delete_comment.delete()

    return JsonResponse({'comment_id': comment_id})


# qna 대댓글
@csrf_exempt
def undercomment_create(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    new_comment_content = req['comment_content']

    new_undercomment = FUnderComment.objects.create(
        comment=FComment.objects.get(id=comment_id),
        comment_author=request.user,
        comment_content=new_comment_content
    )
    new_undercomment.save()

    return JsonResponse({'comment_id': comment_id, 'undercomment_id': new_undercomment.id, 'undercomment_author': request.user.nickname, 'undercomment_content': new_comment_content})


@csrf_exempt
def undercomment_update(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    undercomment_id = req['undercomment_id']
    edit_comment_content = req['comment_content']

    edit_comment = FUnderComment.objects.get(id=undercomment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'undercomment_id': undercomment_id, 'undercomment_author': edit_comment.comment_author.nickname, 'undercomment_content': edit_comment_content})


@csrf_exempt
def undercomment_delete(request, foreign_id, pk):
    req = json.loads(request.body)
    undercomment_id = req['undercomment_id']
    delete_comment = FUnderComment.objects.get(id=undercomment_id)
    delete_comment.delete()

    return JsonResponse({'undercomment_id': undercomment_id})


# 댓글달기

@method_decorator(csrf_exempt, name="dispatch")
def comment_create(request, foreign_id, pk):
    req = json.loads(request.body)
    Post_id = req['post_id']
    post = Post.objects.get(id=Post_id)
    content = req['comment_content']
    new_comment = Comment.objects.create(
        comment_author=request.user, comment_content=content, post=post)
    new_comment.save()
    return JsonResponse({'post_id': Post_id, 'comment_content': content, 'comment_id': new_comment.id})


@method_decorator(csrf_exempt, name="dispatch")
def comment_update(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    comment = Comment.objects.get(id=comment_id)
    content = req['comment_content']
    comment.comment_content = content
    comment.save()
    nickname = comment.comment_author.nickname
    return JsonResponse({'comment_id': comment_id, 'comment_content': content, 'nickname': nickname, })


@method_decorator(csrf_exempt, name="dispatch")
def comment_delete(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return JsonResponse({'comment_id': comment_id})


# review 대댓글
@csrf_exempt
def Rrecomment_create(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    new_comment_content = req['comment_content']

    new_recomment = FReComment.objects.create(
        comment=Comment.objects.get(id=comment_id),
        comment_author=request.user,
        comment_content=new_comment_content
    )
    new_recomment.save()

    return JsonResponse({'comment_id': comment_id, 'recomment_id': new_recomment.id, 'recomment_author': request.user.nickname, 'recomment_content': new_comment_content})


@csrf_exempt
def Rrecomment_update(request, foreign_id, pk):
    req = json.loads(request.body)
    comment_id = req['comment_id']
    recomment_id = req['recomment_id']
    edit_comment_content = req['comment_content']

    edit_comment = FReComment.objects.get(id=recomment_id)
    edit_comment.comment_content = edit_comment_content
    edit_comment.save()

    return JsonResponse({'comment_id': comment_id, 'recomment_id': recomment_id, 'recomment_author': edit_comment.comment_author.nickname, 'recomment_content': edit_comment_content})


@csrf_exempt
def Rrecomment_delete(request, foreign_id, pk):
    req = json.loads(request.body)
    recomment_id = req['recomment_id']
    delete_comment = FReComment.objects.get(id=recomment_id)
    delete_comment.delete()

    return JsonResponse({'recomment_id': recomment_id})


# 친구찾기

def friend_list(request, foreign_id):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    all_friend = foreign.find_friend.order_by('-pk')
    paginator = Paginator(all_friend, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_friend = all_friend.count()
    ctx = {
        'univ': foreign,
        'page_obj': page_obj,
        'total_friend': total_friend,
    }
    return render(request, 'foreign/friend_list.html', ctx)


def friend_detail(request, foreign_id, pk):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    friend = FFriend.objects.get(id=pk)
    comments = friend.friendcomment_set.all()
    undercomments = FriendUnderComment.objects.all()
    now = datetime.now()
    ctx = {
        'friend': friend,
        'comments': comments,
        'univ': foreign,
        'is_authenticated': request.user.is_authenticated,
        'undercomments': undercomments,
        'now': now
    }
    return render(request, 'foreign/friend_detail.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def friend_create(request, foreign_id):
    foreign_univ = get_object_or_404(Foreign, pk=foreign_id)
    if request.method == 'POST':
        form = FriendForm(request.POST)
        form.friend_author = request.user
        print(form)
        if form.is_valid():
            post = form.save(commit=False)
            post.friend_author = request.user
            post.foreign = foreign_univ
            post.save()
            return redirect('foreign:friend_detail', foreign_id, post.pk)
    else:
        form = FriendForm()
        ctx = {
            'form': form,
            'univ': foreign_univ,
        }
        return render(request, template_name='foreign/friend_form.html', context=ctx)


@login_required(login_url=URL_LOGIN)
def friend_edit(request, foreign_id, pk):
    foreign = get_object_or_404(Foreign, pk=foreign_id)
    friend = get_object_or_404(FFriend, id=pk)
    IsFriendAuthor = True
    if request.method == 'POST':
        form = FriendForm(request.POST, instance=friend)
        if form.is_valid():
            friend = form.save()
            return redirect('foreign:friend_detail', foreign_id, pk)
    else:
        if friend != None:                # 수정할 때
            if request.user != friend.friend_author:
                IsFriendAuthor = False
            type = 'update'
        else:                           # 새로 생성할 때
            type = 'create'
        form = FriendForm(instance=friend)
        ctx = {
            'form': form,
            'univ': foreign,
            'IsFriendAuthor': IsFriendAuthor,
            'type': type,
            'friend': friend,
        }
        return render(request, template_name='foreign/friend_form.html', context=ctx)


def friend_delete(request, foreign_id, pk):
    friend = get_object_or_404(FFriend, id=pk)
    if request.method == 'POST':
        friend.delete()
    return redirect('foreign:friend_list', foreign_id)
