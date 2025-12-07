from rest_framework import serializers

from .models import Payout


class PayoutSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payout.

    Выполняет валидацию суммы, валюты и реквизитов получателя.
    """

    class Meta:
        model = Payout
        fields = "__all__"
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_amount(self, value: float) -> float:
        """Проверяет, что сумма положительная."""
        if value <= 0:
            raise serializers.ValidationError(
                "Сумма должна быть положительной."
            )
        return value

    def validate_currency(self, value: str) -> str:
        """Проверяет, что валюта — трёхбуквенный код."""
        if not isinstance(value, str) or len(value.strip()) != 3:
            raise serializers.ValidationError(
                "Валюта должна быть в формате ISO (3 буквы)."
            )
        return value.strip().upper()

    def validate_recipient_details(self, value: str) -> str:
        """Проверяет корректность реквизитов получателя."""
        if not value:
            raise serializers.ValidationError(
                "Реквизиты получателя обязательны."
            )
        return value
