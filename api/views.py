# api/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from .models import Summary
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

load_dotenv()
@csrf_exempt # This decorator allows tools like Postman to send POST requests
@api_view(['POST']) # 1. Defines this is a POST-only API view
@permission_classes([IsAuthenticated]) # 2. Requires a valid token
def summarize_view(request):
    # We only want to allow POST requests
    if request.method != 'POST':
        return JsonResponse({"error": "POST method required."}, status=405)

    try:
        # Get the data the frontend sent
        data = json.loads(request.body)
        text_to_summarize = data.get('fileContent')

        # Check if the data is valid
        if not text_to_summarize:
            return JsonResponse({"error": "fileContent cannot be empty."}, status=400)

        # --- FAKE summarization logic ---
        # (We will replace this with the real AI call later)
        summary_text = api_call(text_to_summarize)
        word_count_original = len(text_to_summarize.split())
        word_count_summary = len(summary_text.split())
        
        Summary.objects.create(
            user=request.user,
            original_text=text_to_summarize,
            summary_text=summary_text
        )

        # Send back a successful response that matches our API Contract
        return JsonResponse({
            "summary": summary_text,
            "originalWordCount": word_count_original,
            "summaryWordCount": word_count_summary
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format in request body."}, status=400)

def api_call(content):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv('OPENROUTER_API_KEY')
    )
    completion = client.chat.completions.create(
        model="z-ai/glm-4.5-air:free",
        messages=[
            {
                "role": "user",
                "content": "Summarize the following content for revision newsletter.Note just five lines enough" +content
                }
        ]
    )
    r = completion.choices[0].message.content
    return r.strip()  # Ensure we return a clean string without extra spaces or newlines





# Add this new function to api/views.py
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_summaries_view(request):
    try:
        # 1. Get all summaries belonging to the currently authenticated user
        #    and order them by the newest first.
        summaries = Summary.objects.filter(user=request.user).order_by('-created_at')

        # 2. Prepare the data to be sent back as JSON.
        #    We manually create a list of dictionaries.
        results = [
            {
                "id": summary.id,
                "summary_text": summary.summary_text,
                "created_at": summary.created_at
            }
            for summary in summaries
        ]

        # 3. Send the list back as a response.
        return Response(results)

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)