from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class MixinGenresCategories(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                            mixins.ListModelMixin, GenericViewSet):
    """Миксин для выполнения 3 методов."""
    pass
