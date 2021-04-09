from django.shortcuts import render
from django.views import generic

from catalog.models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import RenewBookForm
from .models import Author, Book

from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def index(request):
    """Просмотр функции для домашней страницы сайта."""

    # Генерировать количество некоторых из основных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Доступные книги (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # 'all()' подразумевается по умолчанию.
    num_authors = Author.objects.count()

    num_genre = Genre.objects.all().count()

    # Количество посещений
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_visits': num_visits,
    }

    # Визуализация HTML-шаблона index.html с данными в переменных контекста
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    #context_object_name = 'my_book_list'   # Ваше собственное имя для списка как переменная шаблона
    #queryset = Book.objects.filter(title__icontains='Война')[:5] # Получите 5 книг, содержащие в тайтле "война"
    #template_name = 'book_list.html'  # Укажите свой собственный шаблон имя / местоположение

    # def get_context_data(self, **kwargs):
    #     # Сначала позвоните в базовую реализацию, чтобы получить контекст
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Создайте любые данные и добавьте его в контекст
    #     context['some_data'] = 'This is just some data'
    #     return context

    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5] # Получите 5 книг, содержащие титульную войну


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Общий доступ на основе классов в списке книг в долг к текущему пользователю."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Общий вид на основе класса, перечисляющий все книги в долг.Видимо только пользователям с разрешения Can_mark_returned."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Если это запрос на POST, обработайте данные формы
    if request.method == 'POST':

        # Создайте экземпляр формы и заполните его с помощью данных из запроса:
        form = RenewBookForm(request.POST)

        # Проверьте, действительна ли форма:
        if form.is_valid():
            # Обработайте данные в форме.
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # Перенаправить на новый URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # Если это GET (или любой другой метод) создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(LoginRequiredMixin,CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}

class AuthorUpdate(LoginRequiredMixin,UpdateView):
    model = Author
    fields = '__all__' # Не рекомендуется (потенциальная проблема безопасности, если добавлено больше полей)

class AuthorDelete(LoginRequiredMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('authors')



class BookCreate(LoginRequiredMixin,CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(LoginRequiredMixin,UpdateView):
    model = Book
    fields = '__all__' # Не рекомендуется (потенциальная проблема безопасности, если добавлено больше полей)

class BookDelete(LoginRequiredMixin,DeleteView):
    model = Book
    success_url = reverse_lazy('books')
