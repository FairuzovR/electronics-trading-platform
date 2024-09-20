from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Network, Product, SupplierNode


@admin.action(description='Очистить задолженность')
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


class SupplierNodeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'country',
        'city',
        'street',
        'house_number',
        'supplier',
        'debt'
    )
    list_filter = ('city',)
    actions = [clear_debt]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('supplier')


class NetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_supplier_links')

    def get_supplier_links(self, obj):
        links = []
        for node in obj.nodes.all():
            url = reverse('admin:api_suppliernode_change', args=[node.id])
            links.append(format_html('<a href="{}">{}</a>', url, node.name))
        return format_html(', '.join(links))

    get_supplier_links.short_description = 'Поставщики'


admin.site.register(SupplierNode, SupplierNodeAdmin)
admin.site.register(Product)
admin.site.register(Network, NetworkAdmin)
