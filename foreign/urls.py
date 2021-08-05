from django.urls import path
from . import views

app_name = 'foreign'

urlpatterns = [
    path('univ_list', views.univ_list, name='univ_list'),
    path('wiki/<int:pk>', views.wiki, name='wiki'),
    path('wiki/edit/<int:pk>', views.wiki_edit_apply, name='wiki_edit_apply'),
    path('wiki/edit_language_score/<int:pk>',
         views.wiki_edit_language_score, name='wiki_edit_language_score'),
    path('wiki/edit_course_enroll/<int:pk>',
         views.wiki_edit_course_enroll, name='wiki_edit_course_enroll'),
    path('wiki/edit_accomodation/<int:pk>',
         views.wiki_edit_accommodation, name='wiki_edit_accommodation'),
    path('wiki/edit_atmosphere/<int:pk>',
         views.wiki_edit_atmosphere, name='wiki_edit_atmosphere'),
    path('wiki/edit_club/<int:pk>', views.wiki_edit_club, name='wiki_edit_club'),
    path('wiki/edit_away_scholarship/<int:pk>',
         views.wiki_edit_away_scholarship, name='wiki_edit_away_scholarship'),
    path('<int:foreign_id>/review/list', views.review_list, name="review_list"),
    path('<int:foreign_id>/review/create',
         views.review_create, name="review_create"),
    path('<int:foreign_id>/review/delete/<int:pk>/',
         views.review_delete, name="review_delete"),
    path('<int:foreign_id>/review/detail/<int:pk>/',
         views.review_detail, name="review_detail"),
    path('<int:foreign_id>/review/update/<int:pk>/',
         views.review_update, name="review_update"),

    path('<int:foreign_id>/question/', views.question_list, name='question_list'),
    path('<int:foreign_id>/question/<int:pk>/',
         views.question_detail, name='question_detail'),
    path('<int:foreign_id>/question/create/',
         views.question_create, name='question_create'),
    path('<int:foreign_id>/question/<int:pk>/edit/',
         views.question_edit, name='question_edit'),
    path('<int:foreign_id>/question/<int:pk>/delete/',
         views.question_delete, name='question_delete'),

    path('<int:foreign_id>/review/detail/<int:pk>/comment_create/',
         views.comment_create, name="comment_create"),
    path('<int:foreign_id>/review/<int:pk>/comment_delete/',
         views.comment_delete, name="comment_delete"),
]
