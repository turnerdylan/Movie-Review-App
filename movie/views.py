from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required


#views is a set of functions that handles requests and typically renders out the corresponding html page

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(
        request, 
        'home.html',
        {
            'searchTerm':searchTerm, 
            'movies': movies
        })

def about(request):
    return HttpResponse('<h1>About page</h1>')

def signup(request):
    email = request.GET.get('email')
    return render(
        request,
        'signup.html',
        {'email': email})

def detail(request, movie_id):
    # get objects for the movie info and reviews so we can send them to the html file for display
    movie = get_object_or_404(Movie,pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(
        request, 
        'detail.html',
        {
            'movie':movie,
            'reviews':reviews,
        })

@login_required
def createreview(request, movie_id):
    #get movie obj from database
    movie = get_object_or_404(Movie,pk=movie_id) 
    if request.method == 'GET':
        return render(request, 'createreview.html', 
        {'form':ReviewForm(), 'movie':movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('detail', newReview.movie.id)
        except ValueError:
            return render(
                request, 
                'createreview.html', 
                {
                    'form':ReviewForm(),
                    'error':'bad data passed in'
                })

@login_required
def updatereview(request, review_id):
    #retrieve object with review id, supply current user as well
    review = get_object_or_404(
        Review,
        pk=review_id,
        user=request.user
    )
    #if directed to page
    if request.method == 'GET':
        #pass in current review obj so it populates the form
        form = ReviewForm(instance=review)
        return render(
            request,
            'updatereview.html',
            {
                'review':review,
                'form':form
            }
        )
    else:
        #update the current form
        try:
            #retrieve values from new form
            form = ReviewForm(
                request.POST,
                instance=review
                )
            #update the review
            form.save()
            return redirect('detail', review.movie.id)
        except ValueError:
            return render(request,
            'updatereview.html',
            {
                'review': review,
                'form': form,
                'error': 'Bad data in form'
            })

@login_required
def deletereview(request, review_id):
    review = get_object_or_404(
        Review,
        pk=review_id,
        user=request.user
    )
    review.delete()
    return redirect('detail', review.movie.id)