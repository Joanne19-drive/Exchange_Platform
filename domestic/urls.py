from django.urls import path
from . import views

app_name = 'domestic'

urlpatterns = [
    path('', views.univ_list, name='univ_list'),

    path('<int:domestic_id>/wiki/', views.wiki, name='wiki'),
    path('<int:domestic_id>/wiki/<str:wiki_type>/',
         views.wiki_edit, name='wiki_edit'),


    path('<int:domestic_id>/qna/', views.question_list, name='question_list'),
    path('<int:domestic_id>/qna/create/',
         views.question_create, name='question_create'),
    path('<int:domestic_id>/qna/<int:pk>/',
         views.question_detail, name='question_detail'),
    path('<int:domestic_id>/qna/<int:pk>/edit/',
         views.question_edit, name='question_edit'),
    path('<int:domestic_id>/qna/<int:pk>/delete/',
         views.question_delete, name='question_delete'),
    path('<int:domestic_id>/qna/search/',
         views.question_search, name='question_search'),

    path('<int:domestic_id>/qna/<int:pk>/comment_create/',
         views.comment_create, name='comment_create'),
    path('<int:domestic_id>/qna/<int:pk>/comment_update/',
         views.comment_update, name='comment_update'),
    path('<int:domestic_id>/qna/<int:pk>/comment_delete/',
         views.comment_delete, name='comment_delete'),

    path('<int:domestic_id>/qna/<int:pk>/undercomment_create/',
         views.undercomment_create, name='undercomment_create'),
    path('<int:domestic_id>/qna/<int:pk>/undercomment_update/',
         views.undercomment_update, name='undercomment_update'),
    path('<int:domestic_id>/qna/<int:pk>/undercomment_delete/',
         views.undercomment_delete, name='undercomment_delete'),


    path('<int:domestic_id>/sister/', views.sister_list, name='sister_list'),
    path('<int:domestic_id>/sister/add', views.sister_add, name='sister_add'),


    path('<int:domestic_id>/credit/', views.credit_list, name='credit_list'),
    path('<int:domestic_id>/credit/create',
         views.credit_create, name='credit_create'),
    path('<int:domestic_id>/credit/search',
         views.credit_search, name='credit_search')
]
