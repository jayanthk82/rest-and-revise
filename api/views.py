# api/views.py
import requests
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
from .job_api_utils import fetch_job_listings
from django.http import HttpResponse
from weasyprint import HTML
from .gemini_utils import generate_resume_html # 1. Import our new Gemini function
import base64


load_dotenv()

'''Use this function to make a query for a LLM(You also add base64 url for images to get response based on the images)'''
def LLM_API_CALL(query):
    return query
    '''client = OpenAI(
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
        return Response({"error": f"An error occurred: {str(e)}"}, status=500)


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


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def job_suggestions_view(request):
    """
    An endpoint to provide job suggestions based on multiple keywords.
    """
    # Create a list of skills or job titles
    skills = ['writer']
    
    jobs = fetch_job_listings(search_terms=skills)
    print(type(jobs[0]))
    return Response(jobs)

'''
@csrf_exempt        #This decorator allows tools like Postman to send POST requests
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_resume_pdf_view(request):
    """
    An endpoint that takes user data and a job description,
    generates a resume using the Gemini API, and returns it as a PDF.
    """
    try:
        # 2. Get the data from the frontend's request body
        user_data = request.data.get('userData')
        job_description = request.data.get('jobDescription')

        if not user_data or not job_description:
            return Response({"error": "User data and job description are required."}, status=400)

        # 3. Call our Gemini utility to get the resume as an HTML string
        resume_html = generate_resume_html(user_data, job_description)

        # 4. Use WeasyPrint to convert the HTML string into a PDF in memory
        pdf_file = HTML(string=resume_html).write_pdf()

        # 5. Return the PDF file directly as the HTTP response
        response = HttpResponse(pdf_file, content_type='application/pdf')
        # This header tells the browser to display the PDF inline
        response['Content-Disposition'] = 'inline; filename="resume.pdf"'
        
        return response

    except Exception as e:
        print(f"An error occurred during PDF generation: {e}")
        return Response({"error": "Failed to generate resume PDF."}, status=500)

'''


@csrf_exempt        #This decorator allows tools like Postman to send POST requests
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_resume_pdf_view(request):
    """
    An endpoint that takes user data and a job description,
    generates a resume using the Gemini API, and returns it as a PDF.
    """
    user_data = request.data.get('userData')
    job_description = request.data.get('jobDescription')
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
        
        query = f'Extract the skills that are suitable for the job {job_description} from the following user knowing topics. User known topics {topics} '
        skills = LLM_API_CALL(query)
        '''Create resume for the above extracted skills'''
        #print(skills)
        # 2. Get the data from the frontend's request body
        #user_data +=skills

        if not user_data or not job_description:
            return Response({"error": "User data and job description are required."}, status=400)

        # 3. Call our Gemini utility to get the resume as an HTML string
        resume_html = generate_resume_html(user_data, job_description)

        # 4. Use WeasyPrint to convert the HTML string into a PDF in memory
        pdf_file = HTML(string=resume_html).write_pdf()
        pdf_base64 = base64.b64encode(pdf_file).decode('utf-8')

        # 2. Get the size of the PDF in bytes
        pdf_size_bytes = len(pdf_file)

        # 3. Build the exact JSON object Retool is expecting
        retool_file_object = {
            'name': 'generated_resume.pdf',
            'type': 'application/pdf',
            'sizeBytes': pdf_size_bytes,
            'base64Data': pdf_base64
        }
        
        # 4. Return this complete object as the JSON response
        return JsonResponse(retool_file_object)
        '''
        # 5. Return the PDF file directly as the HTTP response
        response = HttpResponse(pdf_file, content_type='application/pdf')
        # This header tells the browser to display the PDF inline
        response['Content-Disposition'] = 'inline; filename="resume.pdf"'
        
        return response'''

    except Exception as e:
        print(f"An error occurred during PDF generation: {e}")
        return Response({"error": "Failed to generate resume PDF."}, status=500)
