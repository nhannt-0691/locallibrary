from django.shortcuts import render
from django.utils.translation import gettext_lazy as _  # Thêm dòng này
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import LoanStatus

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact=LoanStatus.AVAILABLE.value).count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        # Thêm các biến dịch vào context
        'books_label': _("Books"),
        'authors_label': _("Authors"),
        'copies_label': _("Copies"),
        'available_label': _("Available Now"),
        'library_stats_label': _("Library At A Glance"),
    }

    return render(request, 'index.html', context=context)

