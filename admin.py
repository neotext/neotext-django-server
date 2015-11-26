from django.contrib import admin

# Register your models here.
from .models import Quote

class QuoteAdmin(admin.ModelAdmin):
   list_display = ('citing_url', 'citing_quote', 'cited_url')


admin.site.register(Quote, QuoteAdmin)
