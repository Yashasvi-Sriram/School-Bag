import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse
from paper.models import Book, Page


def ls(request):
    if request.method == 'GET':
        try:
            book_name = request.GET['book_name']
            answer = {'pages': [], 'books': []}

            # list out all books and loose pages
            if book_name == '':
                all_books = Book.objects.all()
                for book in all_books:
                    answer['books'].append(book.name)
                loose_pages = Page.objects.filter(book=None)
                for loose_page in loose_pages:
                    answer['pages'].append(loose_page.name)

            # list out all pages in that book
            else:
                book = Book.objects.get(name=book_name)
                for page in book.pages.all():
                    answer['pages'].append(page.name)

            return HttpResponse(json.dumps({'status': 0, 'body': answer}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid data'}))
        except (ValueError, TypeError):
            return HttpResponse(json.dumps({'status': -1, 'message': 'Improper data'}))
    else:
        return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid request'}))


def book_exists(request):
    if request.method == 'GET':
        try:
            book_name = request.GET['book_name']
            Book.objects.get(name=book_name)
            return HttpResponse(json.dumps({'status': 0}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'status': -1, 'message': 'Book doesn\'t exist'}))
        except (ValueError, TypeError):
            return HttpResponse(json.dumps({'status': -1, 'message': 'Improper data'}))
    else:
        return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid request'}))


def book_jsonize(book):
    jsoned_book = {
        'id': book.id,
        'name': book.name,
    }
    return jsoned_book


def book_create(request):
    if request.method == 'POST':
        try:
            name = request.POST['name']
            new_book = Book(name=name)
            new_book.save()
            return HttpResponse(json.dumps({'status': 0, 'body': book_jsonize(new_book)}))
        except IntegrityError:
            return HttpResponse(json.dumps({'status': -1, 'message': 'Constraints not met'}))
        except (ValueError, TypeError):
            return HttpResponse(json.dumps({'status': -1, 'message': 'Improper data'}))
    else:
        return HttpResponse(json.dumps({'status': -1, 'message': 'Invalid request'}))


def book_update_name(request):
    return None


def book_delete(request):
    return None