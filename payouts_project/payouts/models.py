from django.db import models

class Payout(models.Model):
    '''
    Модель заявки на выплату.

    Статус заявки может изменяться в ходе
    асинхронной обработки Celery-задачей.
    '''

    class Status(models.TextChoices):
        CREATED = 'created', 'Создана'
        PROCESSING = 'processing', 'Обрабатывается'
        COMPLETED = 'completed', 'Выполнена'
        FAILED = 'failed', 'Ошибка'
        CANCELLED = 'cancelled', 'Отменена'

    amount: float = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Сумма выплаты',
        help_text='Положительная сумма выплаты в валюте платежа.'
    )

    currency: str = models.CharField(
        max_length=3,
        verbose_name='Валюта',
        help_text='Трёхбуквенный код валюты (ISO 4217), например USD.'
    )

    recipient_details: str = models.JSONField(
        verbose_name='Реквизиты получателя',
        help_text='Номер счёта, номер карты или иные данные получателя.'
    )

    status: str = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
        verbose_name='Статус заявки',
        help_text='Текущий статус обработки заявки.'
    )

    description: str | None = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
        help_text='Дополнительный комментарий к заявке.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def __str__(self):
        return (
            f'Payout #{self.id} - '
            f'{self.amount} {self.currency} ({self.status})'
        )
