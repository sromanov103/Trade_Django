from django.db import models
from django.contrib.auth.models import User


class Ad(models.Model):
    """Модель объявления"""
    CONDITION_CHOICES = [
        ('new', 'Новый'),
        ('used', 'Б/У'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads',
                            verbose_name='Пользователь')
    title = models.CharField('Заголовок', max_length=200)
    description = models.TextField('Описание')
    image_url = models.ImageField('Изображение', upload_to='ads/', blank=True, null=True)
    category = models.CharField('Категория', max_length=100)
    condition = models.CharField('Состояние', max_length=4, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    """Модель предложения обмена"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('accepted', 'Принято'),
        ('rejected', 'Отклонено'),
    ]

    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='sent_proposals',
                                 verbose_name='Отправитель')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='received_proposals',
                                  verbose_name='Получатель')
    comment = models.TextField('Комментарий')
    status = models.CharField('Статус', max_length=8, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
        ordering = ['-created_at']

    def __str__(self):
        return f'Обмен {self.ad_sender} на {self.ad_receiver}'
