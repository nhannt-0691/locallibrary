from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import LoanStatus
from catalog.constants import BOOKS_PER_PAGE 

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
        'books_label': _("Books"),
        'authors_label': _("Authors"),
        'copies_label': _("Copies"),
        'available_label': _("Available Now"),
        'library_stats_label': _("Library At A Glance"),
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = BOOKS_PER_PAGE
    context_object_name = 'book_list'
    template_name = 'catalog/book_list.html'

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_instances'] = self.object.bookinstance_set.all()
        context['LOAN_STATUS_AVAILABLE'] = LoanStatus.AVAILABLE.value
        context['LOAN_STATUS_MAINTENANCE'] = LoanStatus.MAINTENANCE.value
        return context
    
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'

