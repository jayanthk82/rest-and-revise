# api/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from .models import Problems,User
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from rest_framework.response import Response
from rest_framework.authtoken.models import Token # 1. Import the Token model

load_dotenv()

'''Use this function to make a query for a LLM(You also add base64 url for images to get response based on the images)'''
def LLM_API_CALL(query):
    return query
    '''
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv('OPENROUTER_API_KEY')
    )
    completion = client.chat.completions.create(
        model="nvidia/nemotron-nano-9b-v2:free",
        messages=[
            {
                "role": "user",
                #"content": [{"type": "text","text":query}]
                "content": query
                }
        ]
    )
    res = completion.choices[0].message.content
    return res.strip()  # Ensure we return a clean string without extra spaces or newlines'''
    

'''Use this function to upload new problem for revision. This funtion verifies where the user sending this requesting has an account or not. If yes proceeds and stores required info into the database'''
@csrf_exempt        #This decorator allows tools like Postman to send POST requests
@api_view(['POST']) # 1. Defines this is a POST-only API view
@permission_classes([IsAuthenticated]) # 2. Requires a valid token
def upload_problem(request):
    try:
        # Get the data the frontend sent
        data = json.loads(request.body)
        problem = data.get('problem')
        user_solution = data.get('solution')

        # Check if the data is valid
        if not (problem or user_solution):
            return JsonResponse({"error": "Problem or Solution cannot be empty."}, status=400)
        query = f"Analyze the  problem and solution and return the information that helps for better revision. Include comments on the approach along with suggestions to improve if needed etcc., You have the freedom to describe and return any type of analysis for better and smart Revision. Problem: {problem}, solution :{user_solution}"
        LLM_response = LLM_API_CALL(query)
        Problems.objects.create(
            user=request.user,
            title = problem[:10],
            description = problem,
            solution = user_solution,
            ai_description = LLM_response
        )
    
        # 2. CALL THE BACKGROUND TASK
        # .delay() tells Celery to run this in the background
        #send_summary_email.delay(request.user.id)
        # Send back a successful response that matches our API Contract
        return JsonResponse({
            "problem": problem,
            "user_solution": user_solution,
            "ai_analysis": LLM_response
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format in request body."}, status=400)

# Add this new function to api/views.py
'''Use this view to retrieve complete info of an user. Before returning the data it validates user. '''
@csrf_exempt        #This decorator allows tools like Postman to send POST requests
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_data(request):
    try:
        # 1. Get all summaries belonging to the currently authenticated user
        #    and order them by the newest first.
        problems = Problems.objects.filter(user=request.user)
        # 2. Prepare the data to be sent back as JSON.
        #    We manually create a list of dictionaries.
        results = [
            {
                "id": problem.id,
                "problem":problem.description,
                "user_solution": problem.solution,
                "ai_analysis_report":problem.ai_description,
                "created_at": problem.created_at,
                "proficiency_rating" : problem.proficiency_rating,
                'User_Note':problem.note,
                "newsletter_info":problem.recent_date

            }
            for problem in problems
        ]

        # 3. Send the list back as a response.
        return Response(results)

    except Exception as e:
        return ResponIsAuthenticatedse({"error": f"An error occurred: {str(e)}"}, status=500)


'''Use this view to get all the topics of an user to find the next day topics'''
def get_user_log(request_user):

    try:
        problems = Problems.objects.filter(user=request_user)
        print(problems)
        results = [
            {
                "id": problem.id,
                "problem":problem.description,
                "user_solution": problem.solution,
                "ai_analysis_report":problem.ai_description,
                "recent_date" : problem.recent_date,
                "proficiency_rating" : problem.proficiency_rating,
                "count" : problem.count
            }
            for problem in problems
        ]
        return results
    except Exception as e:
        # **THE FIX IS HERE**
        # Instead of returning an error string, we return an empty list.
        # This is safe for the scheduler to process.
        print(f"Error fetching user log for {request_user.username}: {e}")
        return []
    
'''Use this function to create a new user by giving username,email-id and login password'''
@csrf_exempt        #This decorator allows tools like Postman to send POST requests
@api_view(['POST'])
@permission_classes([AllowAny])  # This makes the view public and solves the error
def sign_up(request):
    info = json.loads(request.body)
    try: 
        user = User.objects.create_user(
            username = info["username"],
            email = info["email"],
            password = info["password"],
            is_active = True,
        )
        user.save()
        return Response(f"{info["username"]} created\n")
        
    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)
    


@csrf_exempt        #This decorator allows tools like Postman to send POST requests
@api_view(['GET'])
#@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_resume(request):
    info = json.loads(request.body)
    logs =None
    token_key = (request.headers.get('Authorization').split('Token '))[1]
    try:
       token = Token.objects.get(key=token_key)
       print(token.user)
       logs = get_user_log(token.user)
    except Exception as e:
        print(str(e))
    try:
        '''Extract user skills using AN LLM'''
        topics = []
        count = 1
        for log in logs:
            topics.append(str(f'{count}:{log['ai_analysis_report']}'))
            count+=1
        topics = ' '.join(topics)
        
        query = f'Extract the skills that are suitable for the job {info['job_description']} from the following user knowing topics. User known topics {topics} '
        skills = LLM_API_CALL(query)
        '''Create resume for the above extracted skills'''
        #print(skills)
        print(skills)
        query = f'Create ATS friendly resume with the following skills and job description. Skills: {skills}, job description; {info['job_description']}. Note follow the following instructions to tune proper resume. Instructions:f{info['instructions']}'
        resume = LLM_API_CALL(query)
        response = {"resume":resume}
        return Response(response)
    except Exception as e:
        response = {'error':str(e)}
        return Response(response)
