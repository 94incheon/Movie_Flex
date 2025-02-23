from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from .models import Movie, Review, Comment, Genre
from .forms import ReviewForm, CommentForm
from . import tests


# Movie
@require_http_methods(['GET'])
def index(request):
    movies = Movie.objects.all().order_by('-release_date')
    paginator = Paginator(movies, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'movies/index.html', context)

from rest_framework.decorators import api_view
@api_view(['GET'])
def get_recommend(request):

    code = request.GET.get('code') # 0: 위치정보 X, 1: 위치정보 O
    if (code == "1"):
        params = {
            'lat': request.GET.get('lat'),
            'lon': request.GET.get('lon'),
            'code': True,
        }
    else:
        params = {
            'code': False,
        }

    genre_list, IMG_URL, loc_name = tests.recommend_movie(params)

    rgs = []
    for i in range(5):
        if i < len(genre_list):
            rgs.append(get_object_or_404(Genre, name=genre_list[i]))
        else:
            rgs.append(get_object_or_404(Genre, name=genre_list[0]))
    # 평점순 5개 추천
    reco_movies = Movie.objects.filter(Q(genre=rgs[0]) | Q(genre=rgs[1]) | Q(genre=rgs[2]) | Q(genre=rgs[3]) | Q(genre=rgs[4])).order_by('-vote_average')[:5]

    from .serializers import MovieCarouselSerializer
    serializer = MovieCarouselSerializer(reco_movies, many=True)

    data = {
        'IMG_URL': IMG_URL,
        'loc_name': loc_name,
        'genre_list': genre_list,
        'reco_movies': serializer.data, # id, poster_path
    }
    from rest_framework.response import Response
    return Response(data)

@require_http_methods(['GET'])
def detail(request, movie_pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_pk)
        reviews = movie.reviews.all().order_by('-pk')
        genres = movie.genre.all()
        context = {
            'movie': movie,
            'reviews': reviews,
            'genres': genres,
        }
        return render(request, 'movies/detail.html', context)

def search(request):
    text = request.GET.get('q')
    movies = Movie.objects.filter(Q(title__icontains=text)|Q(title_en__icontains=text))
    context = {
        'movies': movies,
        'text': text,
    }
    return render(request, 'movies/search.html', context)

# Review
def review_create(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=movie_pk)
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                review.movie = movie
                review.save()
            return redirect('movies:detail', movie.pk)
        else:
            form = ReviewForm()
        context = {
            'form': form
        }
        return render(request, 'movies/review_form.html', context)
    else:
        messages.warning(request, '리뷰 작성을 위해서는 로그인이 필요합니다.')
        return redirect('accounts:login')


def review_detail(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    comments = Comment.objects.filter(review=review).order_by('-pk')
    form = CommentForm()

    context = {
        'movie': movie,
        'review': review,
        'comments': comments,
        'form': form,
    }
    return render(request, 'movies/review_detail.html', context)

@login_required
def review_update(request, movie_pk, review_pk):
    review = get_object_or_404(Review, id=review_pk)
    if request.user == review.user:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.save()
                return redirect('movies:review_detail', movie_pk, review_pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form
        }
        return render(request, 'movies/review_form.html', context)
    else:
        messages.warning(request, '리뷰작성자만 수정/삭제 가능합니다.')
        return redirect('movies:index')

@require_POST
@login_required
def review_delete(request, movie_pk, review_pk):
    review = get_object_or_404(Review, id=review_pk)
    if request.user == review.user:
        review.delete()
        messages.warning(request, '리뷰가 삭제 되었습니다.')
    return redirect('movies:detail', movie_pk)

@require_POST
@login_required
def comment_create(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect('movies:review_detail', movie_pk, review_pk)
    else:
        messages.warning(request, '댓글 작성을 위해서는 로그인이 필요합니다.')
        return redirect('accounts:login')

@require_POST
@login_required
def comment_create_api(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    comments = Comment.objects.filter(review=review)

    if request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
        data = {
            'comments': comments
        }
        return JsonResponse(data)
    else:
        messages.warning(request, '댓글 작성을 위해서는 로그인이 필요합니다.')
        return redirect('accounts:login')


@require_POST
@login_required
def comment_delete(request, movie_pk, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user.is_authenticated:
        if comment.user == request.user:
            comment.delete()
            messages.warning(request, '댓글이 삭제되었습니다.')
            return redirect('movies:review_detail', movie_pk, review_pk)
        else:
            messages.warning(request, '본인 댓글만 삭제 가능합니다.')
            return redirect('movies:review_detail', movie_pk, review_pk)

# Like
# 무비라이크 새로고침 렌더버전
@login_required
def movie_like(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
    else:
        movie.like_users.add(request.user)
    return redirect('movies:detail', movie_pk)


def movie_like_api(request, movie_pk):
    if not request.user.is_authenticated:
        return JsonResponse({'is_like_movie': -1})

    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.like_users.filter(pk=request.user.pk).exists():
        movie.like_users.remove(request.user)
        is_like_movie = False
    else:
        movie.like_users.add(request.user)
        is_like_movie = True

    data = {
        'is_like_movie': is_like_movie,
        'count': movie.like_users.count()
    }
    return JsonResponse(data)

@login_required
def review_like(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
    else:
        review.like_users.add(request.user)
    return redirect('movies:review_detail', review.movie.pk, review_pk)

@login_required
def review_like_api(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if review.like_users.filter(pk=request.user.pk).exists():
        review.like_users.remove(request.user)
        is_review_like = False
    else:
        review.like_users.add(request.user)
        is_review_like = True

    data = {
        'is_review_like': is_review_like,
        'review_like_count': review.like_users.count()
    }
    return JsonResponse(data)
