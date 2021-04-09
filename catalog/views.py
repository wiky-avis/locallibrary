from django.shortcuts import render
from django.views import generic

from catalog.models import Book, Author, BookInstance, Genre

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

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre
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
