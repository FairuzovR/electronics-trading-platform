from rest_framework import viewsets

from .models import Product, SupplierNode
from .permissions import IsOwner, IsActive
from .serializers import ProductSerializer, SupplierSerializer
from rest_framework.exceptions import NotAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import SupplierNodeFilter


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = SupplierNode.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsActive]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SupplierNodeFilter

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permissions.append(IsOwner())
        return permissions

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            raise NotAuthenticated()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsActive]

    def get_permissions(self):
        permissions = super().get_permissions()
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            permissions.append(IsOwner())
        return permissions

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            raise NotAuthenticated()
