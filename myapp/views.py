import datetime
import random

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Book, Member, Review
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SearchForm, OrderForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test


# Create your views here.
def index(request):
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = 'Your last login was more that one hour ago'
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist,'last_login':last_login})


def about(request):
    cookie_found = False
    if request.COOKIES.get('lucky_num'):
        myLuckyNum = request.COOKIES.get('lucky_num')
        cookie_found = True

    else:
        myLuckyNum = random.randint(1, 100)

    response = render(request, 'myapp/about.html', {'myLuckyNum': myLuckyNum})
    if not cookie_found:
        response.set_cookie('lucky_num', myLuckyNum, 300)
    return response


def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'myapp/detail.html', {'book': book})


def findbooks(request):
    CATEGORY_CHOICES = {
        'S': 'Science&Tech',
        'F': 'Fiction',
        'B': 'Biography',
        'T': 'Travel',
        'O': 'Other'
    }
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']
            if (category):
                booklist = Book.objects.filter(category=category, price__lte=max_price)
                return render(request, 'myapp/results.html',
                              {'booklist': booklist, 'name': name, 'category': CATEGORY_CHOICES[category],
                               'max_price': max_price})
            else:
                booklist = Book.objects.filter(price__lte=max_price)
                return render(request, 'myapp/results.html',
                              {'booklist': booklist, 'name': name, 'max_price': max_price})

        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            books = form.cleaned_data['books']
            # order = form.save(commit=False)
            member = order.member
            type = order.order_type
            order.save()
            form.save_m2m()
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)

            return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if rating <= 5 and rating >= 1:
                reviews = form.save(commit=False)
                books = reviews.book
                books.num_reviews += 1
                books.save()
                reviews.save()
                # return index(request)
                return redirect('myapp:index')
            else:
                RatingErr = "You must enter a rating between 1 and 5!"
                return render(request, 'myapp/review.html', {'form': form, 'RatingErr': RatingErr})
        else:
            # return HttpResponse('Please fill the form correctly')
            return render(request, 'myapp/review.html', {'form': form})

    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                dt = datetime.datetime.now()
                request.session['last_login'] = 'Last Login: ' + str(dt)
                request.session.set_expiry(3600)

                if 'next' in request.POST:
                    next_url= request.POST.get('next')
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))


@login_required
def chk_reviews(request, book_id):
    try:
        if Member.objects.get(id=request.user.id):
            count = 0
            rating = 0
            bookData = {}
            for r in Review.objects.filter(book__id=book_id):
                count += 1
                rating += r.rating
            if rating != 0:
                bookData['avgRating'] = round(rating / count, 2)
            else:
                bookData['avgRating'] = 'Book is not rated'

            bookData['title'] = Book.objects.get(id=book_id).title
            bookData['price'] = Book.objects.get(id=book_id).price

            return render(request, 'myapp/chk_reviews.html',
                          {'member': request.user.first_name, 'book': bookData})
    except Member.DoesNotExist:
        return render(request, 'myapp/chk_reviews.html')
    except Book.DoesNotExist:
        return render(request, 'myapp/chk_reviews.html', {'member': request.user.first_name})
