from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    # Movie
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),

    # Review
    path('<int:movie_pk>/review_create/', views.review_create, name='review_create'),
    path('<int:movie_pk>/review_detail/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:movie_pk>/review_update/<int:review_pk>/', views.review_update, name='review_update'),
    path('<int:movie_pk>/review_delete/<int:review_pk>/', views.review_delete, name='review_delete'),

    # Comment
    path('<int:movie_pk>/review/<int:review_pk>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:movie_pk>/review/<int:review_pk>/comment_delete/<int:comment_pk>/', views.comment_delete, name='comment_delete'),

    # Like
    path('<int:movie_pk>/movie_like/', views.movie_like, name='movie_like'),
    path('<int:movie_pk>/movie_like_api/', views.movie_like_api, name='movie_like_api'),
    path('<int:review_pk>/review_like/', views.review_like, name='review_like'),
]
