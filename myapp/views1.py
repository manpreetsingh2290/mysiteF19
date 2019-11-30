# Import necessary classes
from django.http import HttpResponse
from .models import Publisher, Book, Member, Order
from django.shortcuts import render


# Create your views here.

def index(request):
    response = HttpResponse()

    booklist = Book.objects.all().order_by('-title')[:10]
    print(booklist)
    heading1 = '<h1>' + 'List of available books: ' + '</h1>'
    response.write(heading1)
    for book in booklist:
        para = '<p>' + str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    response.write('Book not found')

    publisherlist = Publisher.objects.all().order_by('-city')[:10]
    heading2 = '<h1>' + 'List of available Publishers: ' + '</h1>'
    response.write(heading2)
    for publisher in publisherlist:
        para2 = '<p>' + str(publisher.name) + ': ' + str(publisher.city) + '</p>'
        response.write(para2)

    return response


def order(request):
    response = HttpResponse()
    orderlist = Order.objects.all().order_by('id')[:10]
    print(orderlist)
    heading1 = '<p>' + 'List of available Orders: ' + '</p>'
    response.write(heading1)
    for odr in orderlist:
        para = '<p>' + str(odr.id) + ': Total Books in Order:' + str(odr.total_items()) + '</p>'
        response.write(para)

    return response

'''
def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'booklist': booklist})
'''


def about(request):
    response = HttpResponse()
    response.write('<h1>This is an eBook APP</h1>')
    return response


'''
def about(request):
    return render(request, 'myapp/about0.html', {})
'''


def detail(request, book_id):
    response = HttpResponse()
    try:
        book = Book.objects.get(id=book_id)
        response.write('<h3>Title of Book: ' + str(book.title).upper() + '</h3>')
        response.write('<h3>Price: $' + str(book.price) + '</h3>')
        response.write('<h3>Publisher: ' + str(book.publisher.name) + '</h3>')
    except Book.DoesNotExist:
        response.write('<h1>Book not found</h1>')
    return response
