import logging
from rest_framework import generics

from .models import Payout
from .serializers import PayoutSerializer
from .tasks import process_payout

logger = logging.getLogger('payouts')

class PayoutListCreateView(generics.ListCreateAPIView):
    '''
    Обработчик для:
      - получения списка заявок;
      - создания новой заявки.

    При создании автоматически запускается Celery-задача обработки.
    '''
    queryset = Payout.objects.all().order_by('-created_at')
    serializer_class = PayoutSerializer

    def perform_create(self, serializer):
        '''Создаёт заявку и запускает асинхронную обработку.'''
        payout = serializer.save()
        logger.info(f'Created payout {payout.id}')
        process_payout.delay(payout.id)


class PayoutDetailView(generics.RetrieveUpdateDestroyAPIView):
    '''
    Обработчик для:
      - получения заявки по ID;
      - обновления полей (PATCH/PUT);
      - удаления заявки.
    '''
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
