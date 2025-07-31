from django.urls import path
from .views import summarize_view,my_summaries_view
from rest_framework.authtoken.views import obtain_auth_token # Import this

urlpatterns = [
    # This says: match 'v1/summarize' and call 'summarize_view'
    path('v1/summarize', summarize_view, name='summarize'),
    path('get-token/', obtain_auth_token, name='get_token'), # Add this line
    path('v1/my-summaries/',my_summaries_view,name='my_summaries')
]