import os,sys
import django
from django.core.mail import send_mail
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Step 1: Load Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# Step 2: Send test 
def do_mail(Message,receiver):
    try: 
        send_mail(
            subject="Hello from Django (File Test)",
            message= Message,
            from_email="jayanthkonanki82@gmail.com",
            recipient_list=[receiver],
            fail_silently=False,)
        return 
    except Exception as e:
        print(e)
        return 