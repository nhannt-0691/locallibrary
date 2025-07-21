import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.constants import (
    LoanStatus,
    BOOKS_PER_PAGE,
    DEFAULT_LOAN_PERIOD_WEEKS,
    LOAN_STATUS_ON_LOAN,
)
from catalog.models import Book, Author, BookInstance, Genre
from .forms import BorrowBookForm, RenewBookForm

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact=LoanStatus.AVAILABLE.value).count()
    num_authors = Author.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
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
    paginate_by = BOOKS_PER_PAGE
    context_object_name = 'author_list'
    template_name = 'catalog/author_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = BOOKS_PER_PAGE
    
    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status__exact=LoanStatus.ON_LOAN.value
        ).order_by('due_back')

# Thêm view mới
@login_required
def borrow_book(request, pk):
    """View function for borrowing a book."""
    book_instance = get_object_or_404(BookInstance, pk=pk, status=LoanStatus.AVAILABLE.value)
    
    if request.method == 'POST':
        form = BorrowBookForm(request.POST)
        if form.is_valid():
            book_instance.status = LOAN_STATUS_ON_LOAN
            book_instance.borrower = request.user
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            return HttpResponseRedirect(reverse('catalog:my-borrowed'))
    else:
        proposed_due_date = datetime.date.today() + datetime.timedelta(
            weeks=DEFAULT_LOAN_PERIOD_WEEKS['default']
        )
        form = BorrowBookForm(initial={'due_back': proposed_due_date})
    
    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/book_borrow.html', context)

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('catalog:my-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/book_renew_librarian.html', context)

# Thêm generic views cho Author
class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    success_url = reverse_lazy('catalog:authors')

class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    success_url = reverse_lazy('catalog:authors')

class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    success_url = reverse_lazy('catalog:authors')

