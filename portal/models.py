from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Client(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    full_name = models.CharField(max_length=150, verbose_name='ФИО')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'На рассмотрении'),
        ('in_progress', 'В обработке'),
        ('confirmed', 'Подтверждено'),
        ('rejected', 'Отклонено')
    ]

    PAYMENT_ACQUISITIONS = [
        ('rent', 'Аренда'),
        ('purchase', 'Покупка')
    ]

    BUILDING_CHOICES = [
        ('home', 'Дом'),
        ('shop', 'Магазин'),
        ('factory', 'Завод'),
        ('other', 'Другое')
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name='Клиент'
    )

    plot_size = models.PositiveIntegerField(verbose_name='Площадь участка (м²)')
    passport_data = models.CharField(max_length=100, verbose_name='Паспортные данные')
    cadastral_number = models.CharField(max_length=50, verbose_name='Кадастровый номер')

    address = models.CharField(max_length=255, verbose_name='Адрес участка')

    payment_acquisitions = models.CharField(
        max_length=20,
        choices=PAYMENT_ACQUISITIONS,
        verbose_name='Вид приобретения'
    )

    building = models.CharField(
        max_length=25,
        choices=BUILDING_CHOICES,
        verbose_name='Тип строения'
    )

    comment = models.TextField(blank=True, verbose_name='Комментарий')

    document = models.FileField(
        upload_to='documents/',
        blank=True,
        null=True,
        verbose_name='Документы'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        verbose_name='Статус'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return f'Заявка #{self.id} - {self.client.full_name}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']