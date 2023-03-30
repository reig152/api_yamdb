from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class MixinGenresCategories(CreateModelMixin, DestroyModelMixin,
                            ListModelMixin, GenericViewSet):
    """Миксин для выполнения 3 методов."""
    pass
