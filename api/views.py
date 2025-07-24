# api/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
@csrf_exempt # This decorator allows tools like Postman to send POST requests
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
        model="google/gemma-3n-e2b-it:free",
        messages=[
            {
                "role": "user",
                "content": "Summarize the following content for revision newsletter.Note just five lines enough" +content
                }
        ]
    )
    r = completion.choices[0].message.content
    return r.strip()  # Ensure we return a clean string without extra spaces or newlines
