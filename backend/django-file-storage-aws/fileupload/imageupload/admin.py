from django.contrib import admin

from .models import Invoice
from .models import DropBox, UserProfile

admin.site.register(DropBox)
admin.site.register(UserProfile)


class InvoiceAdmin(admin.ModelAdmin):
    readonly_fields = ("pk", "generated_at")


admin.site.register(Invoice, InvoiceAdmin)
