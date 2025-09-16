from celery import shared_task
from datetime import datetime
from .scheduler import NewsletterScheduler
from django.contrib.auth.models import User
import time
import redis,json
from django.conf import settings
import os
from celery.result import AsyncResult
from .email_utils import do_mail

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Initialize a connection to your Redis server.
redis_host = os.getenv('REDIS_HOST', '127.0.0.1')
redis_url = f"redis://{redis_host}:6379/0"
redis_client = redis.from_url(redis_url, decode_responses=True)


# --- Morning Newsletter Task (Refined Version) ---
@shared_task
def generate_newsletter():
    """
    Scheduled to run every morning.
    Generates personalized newsletter content for each active user
    and caches it in Redis for fast retrieval.
    """
    print(f"--- Running Morning Newsletter Generation at {datetime.now().strftime('%Y-%m-%d %H:%M')} ---")
    try:
        # 1. Get all *active* users to avoid processing disabled accounts.
        all_users = User.objects.filter(is_active=True)

        if not all_users.exists():
            print("No active users found. Task finished.")
            return {"message":"No active users to process."}

        # 2. Loop through each active user.
        for user in all_users:
            try:
                scheduler = NewsletterScheduler(user)
                content = scheduler.generate_newsletter_content()
                
                # 3. Use smarter logic to decide whether to cache the content.
                if content and "No topics due for review today!" not in content:
                    redis_key = f'newsletter_content_{user.id}'
                    data = {'email':user.email,"content":content}
                    redis_client.set(redis_key, json.dumps(data), ex=86400) # Expire after 24 hours
                    #print(content)
                    print(f"✅ Successfully generated and cached newsletter for user: {user.username}")
                else:
                    print(f"ℹ️ No topics for user: {user.username}. Nothing to cache.")

            except Exception as e:
                # This inner try-except ensures that one user's failure
                # doesn't stop the entire process.
                print(f"❌ Failed to process newsletter for {user.username}: {e}")

        # 4. Use the `all_users` variable we defined earlier.
        return {"message":"Newsletter generation and caching complete for users."}

    except Exception as e:
        print(f"A critical error occurred in the main task: {e}")
        return {"message":"Task failed due to a critical error."}

# --- Gentle Evening Reminder Task ---
# Adding this back as it aligns with your goal for daily relaxed moments.
@shared_task
def mailing():
    try:
        all_users = User.objects.filter(is_active=True)
        if not all_users.exists():
            print("No active users found. Task finished.")

        for user in all_users:
            redis_key = f"newsletter_content_{user.id}"
            data = redis_client.get(redis_key)
            if data:
                print(type(data))
                payload = json.loads(data)
                do_mail(payload["content"], payload["email"])
                print('mailsent')
            else:
                print(f"No newsletter found for user {user.id}")

        return {"message": "Mail sending finished"}  # ✅ return dict

    except Exception as e:
        print(f"Error in send_mail: {e}")
        return {"message":'error'}  # ✅ return plain string inside dict
