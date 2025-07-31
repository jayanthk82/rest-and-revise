from django.contrib import admin
from .models import Summary
# This customizes how Summaries are displayed in the admin panel
class SummaryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'summary_text')
    list_filter = ('user',)
admin.site.register(Summary, SummaryAdmin)