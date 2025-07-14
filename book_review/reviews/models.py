from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Author(models.Model):
    """
    Модель автора
    """

    name = models.CharField(max_length=100, verbose_name="Имя")
    bio = models.TextField(blank=True, verbose_name="Об авторе")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")

    def __str__(self):
        return f"Информация об авторе {self.name}"

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Book(models.Model):
    """
    Модель книги
    """

    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="books", verbose_name="Автор"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    published_date = models.DateField(
        null=True, blank=True, verbose_name="Дата публикации"
    )
    isbn = models.CharField(
        max_length=13,
        unique=True,
        blank=True,
        verbose_name="Уникальный международный идентификационный номер",
    )
    cover_image = models.ImageField(
        upload_to="covers/", null=True, blank=True, verbose_name="Обложка"
    )

    def __str__(self):
        return f"Информация о книге {self.title}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Review(models.Model):
    """
    Модель рецензии
    """

    text = models.TextField(verbose_name="Текст рецензии")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка (1-5)",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Пользователь",
    )
    book = models.ForeignKey(
        "Book", on_delete=models.CASCADE, related_name="reviews", verbose_name="Книга"
    )

    def __str__(self):
        return f"Рецензия от {self.user.username} на {self.book.title}"

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"
        ordering = ["-created_at"]
