from celery import shared_task
import time

@shared_task
def add(x, y):
    time.sleep(5)  # simulate long task
    return x + y


'''
from celery import shared_task
from .models import User, Problems
from .scheduler import NewsletterScheduler
from .email_utils import send_newsletter_email  #Need to setup emailservice  
from django.conf import settings
import redis # 1. Import the redis library
import json  # 2. Import json to handle data formatting

# 3. Create a Redis client instance
# This connects to the same Redis server your Celery broker uses.
redis_client = redis.from_url(settings.CELERY_BROKER_URL)

@shared_task
def select_daily_topics_for_all_users():
    """
    TASK 1: Runs every night. For each user, it calculates their topics
    and saves the list of IDs directly to Redis.
    """
    print("CELERY BEAT: Starting nightly topic selection for all users...")
    all_users = User.objects.filter(is_active=True)
    for user in all_users:
        scheduler = NewsletterScheduler(user)
        newsletter_content = scheduler.generate_newsletter_content()

        if newsletter_content:
            
            # 4. Store the topic IDs in Redis as a JSON string
            # The key is unique for each user. It expires in 12 hours.
            redis_client.set(
                f'newsletter_topics_{user.id}',
                json.dumps(topic_ids),
                ex=60*60*12
            )
            print(f"Selected topics for {user.username}: {topic_ids}")

    return "Nightly topic selection complete."

@shared_task
def send_daily_newsletter_for_all_users():
    """
    TASK 2: Runs every morning. For each user, it fetches their
    pre-selected topics directly from Redis and sends the email.
    """
    print("CELERY BEAT: Starting morning newsletter dispatch...")
    all_users = User.objects.filter(is_active=True)
    for user in all_users:
        # 5. Fetch the list of topic IDs directly from Redis
        topic_ids_json = redis_client.get(f'newsletter_topics_{user.id}')
        
        if topic_ids_json:
            # 6. Convert the JSON string back into a Python list
            topic_ids = json.loads(topic_ids_json)
            
            topics = Problem.objects.filter(id__in=topic_ids)
            send_newsletter_email(user, topics)
            
            # 7. Clean up the key from Redis after sending
            redis_client.delete(f'newsletter_topics_{user.id}')
            
    return "Morning newsletter dispatch complete."'''