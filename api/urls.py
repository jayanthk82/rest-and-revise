from django.urls import path
from .views import summarize_view

urlpatterns = [
    # This says: match 'v1/summarize' and call 'summarize_view'
    path('v1/summarize', summarize_view, name='summarize'),
]