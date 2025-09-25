from django.urls import path
from .views import upload_problem,my_data,sign_up,create_resume,job_suggestions_view,generate_resume_pdf_view
from rest_framework.authtoken.views import obtain_auth_token # Import this
from .scheduler import NewsletterScheduler_request
from .tasks import newsletter_mailing
urlpatterns = [
    # This says: match 'v1/summarize' and call 'summarize_view'
    path('user/SignUp',sign_up,name = 'UserSignUp'),
    path('get-token/', obtain_auth_token, name='get_token'), # Add this line
    path('v2/MyData',my_data,name='Fetch_My_Data'),  #VERIFIED THE CODE LOGICALLY, NEED TO TEST BY RUNNING THE APPLICATION
    path('v2/NewProblem', upload_problem, name='upload_new_problem'),
    path('user/newsletter',NewsletterScheduler_request,name = 'newsletter_content'),
    path('v2/send_email',newsletter_mailing,name = "send_mail"),
    #NEW PATHS TO MATCH RETOOL QUERIES.
    path('topics',my_data,name='Fetch_My_Data'),
    path('resume',create_resume,name = 'Create Resume'),
    path('getJobs',job_suggestions_view,name = 'get jobs'),
    path('generate-resume', generate_resume_pdf_view, name='generate_resume')


]