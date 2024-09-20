from rest_framework import serializers

from .models import Product, SupplierNode


class SupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierNode
        fields = ('name', 'email', 'country', 'city', 'street', 'house_number')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('owner',)


class SupplierSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """Кастомизируем вывод"""
        representation = super().to_representation(instance)
        representation['products'] = ProductSerializer(
            instance.products.all(),
            many=True
        ).data
        representation['supplier'] = SupplierListSerializer(
            instance.supplier
        ).data if instance.supplier else None
        return representation

    def validate_supplier(self, value):
        """Проверяем глубину иерархии."""
        if value and value.get_hierarchy_level() >= 2:
            raise serializers.ValidationError(
                'Нельзя указать поставщика, если уровень глубины больше 3.'
            )
        return value

    class Meta:
        model = SupplierNode
        fields = '__all__'
        read_only_fields = ('debt', 'owner')
