import logging
import time

from celery import shared_task
from django.db import transaction

from .models import Payout

logger = logging.getLogger("payouts")


@shared_task
def process_payout(payout_id: int):
    """
    Асинхронная задача обработки заявки.

    Этапы:
      1. Получает заявку по ID.
      2. Логирует факт обработки.
      3. Имитирует задержку выполнения.
      4. Устанавливает статус COMPLETED.

    Args:
        payout_id: ID созданной заявки.
    """
    try:
        payout = Payout.objects.get(id=payout_id)
    except Payout.DoesNotExist:
        logger.error(f"Payout {payout_id} does not exist")
        return

    logger.info(f"Processing payout {payout_id}")
    time.sleep(2)  # имитация обработки

    with transaction.atomic():
        payout.status = Payout.Status.COMPLETED
        payout.save(update_fields=["status", "updated_at"])

    logger.info(f"Payout {payout_id} completed")
