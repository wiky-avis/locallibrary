from django.db import models
from django.urls import reverse # Используется для генерации URL, обратившись с узорами URL
import uuid # Требуется для уникальных экземпляров книг

class Genre(models.Model):
    """Модель, представляющая книжный жанр."""
    name = models.CharField(
        max_length=200,
        help_text='Введите жанр книги (например, научная фантастика)')

    def __str__(self):
        """Строка для представления объекта модели."""
        return self.name


class Language(models.Model):
    """
    Модель, представляющая язык (например, английский, французский, японский
    и т. Д.)
    """
    name = models.CharField(max_length=200,
                            help_text="Введите язык книги (например, "
                            "английский, французский, японский и т. Д.)")

    def __str__(self):
        """Строка для представления объекта модели"""
        return self.name


class Book(models.Model):
    """Модель, представляющая книгу (но не конкретная копия книги)."""
    title = models.CharField(max_length=200)

    # ForeignKey используется, потому что книга может иметь только один автор, 
    # но авторы могут иметь несколько книг
    # Автор как строка, а не объект, потому что он еще не объявлен в файле
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(
        max_length=1000,
        help_text='Введите краткое описание книги')
    isbn = models.CharField(
        'ISBN', max_length=13,
        unique=True,
        help_text='13 символов '
        '<a href="http://www.isbn-international.org/content/what-isbn">'
        ' номер ISBN</a>')

    # Manytomanyfield использует, потому что жанр может содержать много книг.
    # Книги могут охватывать много жанров.
    # Класс Genre уже был определен, поэтому мы можем указать объект выше.
    genre = models.ManyToManyField(
        Genre,
        help_text='Выберите жанр для этой книги')

    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        null=True)

    def __str__(self):
        """Строка для представления объекта модели."""
        return self.title

    def get_absolute_url(self):
        """Возвращает URL для доступа к детали записи для этой книги."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    """
    Модель, представляющая определенную копию книги (то есть, которая может 
    быть заимствована из библиотеки).
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Уникальный идентификатор для этой конкретной книги по всей'
        ' библиотеке')
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Обслуживание'),
        ('o', 'Кредит'),
        ('a', 'Доступна'),
        ('r', 'Зарезервированна'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Наличие книги',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """Строка для представления объекта модели."""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Модель, представляющая автора."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Дата смерти', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Возвращает URL для доступа к конкретному экземпляру автора."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Строка для представления объекта модели."""
        return f'{self.last_name}, {self.first_name}'
