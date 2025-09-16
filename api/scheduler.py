# api/scheduler.py
import math
from datetime import date
from .models import User, Problems
import heapq
# We will create this as a separate utility later
from .views import LLM_API_CALL,get_user_log
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


class NewsletterScheduler:
    """
    Encapsulates all the logic for a single user's spaced repetition schedule.
    This is a refactored, more robust version.
    """
    def __init__(self, user: User):
        # FIX: The __init__ method should only set up the object's initial state.
        # It should not perform actions or return values.
        self.user = user
        self.today = date.today()
        self.alpha = 0.5
        self.beta = 0.4
        self.gamma = 0.1
        
    def _calculate_topic_score(self,log) -> float:
        """Calculates the urgency score for a single topic."""
        ''' 
        The following variables are not useful in this function
        problem = log['problem']
        user_solution = log['user_solution']
        ai_analysis_report = log['ai_analysis_report']
        '''
        recent_date = log['recent_date']
        proficiency_rating = log['proficiency_rating']
        count = log['count']
        d_i = (self.today - recent_date).days
        n_i = count
        # Make the proficiency calculation safer in case the rating is None
        p_i = (proficiency_rating or 0) / 5.0
        time_factor = d_i / math.log(1 + n_i + 1)
        proficiency_factor = 1 - p_i
        recap_bias = 1 / (1 + p_i)
        score = (self.alpha * time_factor) + (self.beta * proficiency_factor) + (self.gamma * recap_bias)
        return score

    def select_topics_for_newsletter(self, num_topics=3) -> list:
        """
        Calculates scores for all of a user's topics and returns the top N.
        """

        user_logs = get_user_log(self.user)
        # FIX: Initialize a heap as an empty list
        heap = []
        for log in user_logs:
            try:
                score = self._calculate_topic_score(log)
                # Use a min-heap with a negated score to find the topics with the highest scores
                if len(heap)<num_topics:
                    heapq.heappush(heap, (score,log))
                    continue
                if heap[0][0]<score:
                    heapq.heapreplace(heap, (score,log))

            except (TypeError, KeyError, ValueError) as e:
                # If a log exists but a solution doesn't, just skip it.
                print(f"Could not calculate score for a log item for user {self.user.username}: {e}")
                continue
        return heap

    def generate_newsletter_content(self):
        topics = self.select_topics_for_newsletter()
        # FIX: This is now a proper method of the class and takes `self`.
        if not topics:
            return "No topics due for review today!"

        base_query = 'Create engaging newsletter content for the following topics to get a full-pledged revision by explaining the topics along with solution for the following topics and solutions ai_analysis:'
        
        topic_queries = []
        i=1
        for score, log in topics:
            problem = log['problem']
            user_solution = log['user_solution']
            ai_analysis_report = log['ai_analysis_report']
            proficiency_rating = log['proficiency_rating']
            # topic[0] is description, topic[1] is solution, topic[2] is analysis
            s = f"\n--- Topic {i} ---\nProblem Description: {problem}\nUser Solution: {user_solution}\n AI Analysis Report: {ai_analysis_report}\n User Proficiency level on this topics {proficiency_rating}"
            i+=1
            topic_queries.append(s)
        
        full_query = base_query + ' '.join(topic_queries)
        
        print("---- GENERATING NEWSLETTER WITH THIS QUERY ----")
        #print(full_query)
        # to-do: Replace this with a real LLM call utility
        content = LLM_API_CALL(full_query)
        #content = 'This is wonderFull-Exactly working what you need'
        # For now, we'll return a placeholder
        return content
    

#Use below code snippet for querying thorugh postman
@csrf_exempt        #This decorator allows tools like Postman to send POST requests
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # 2. Requires a valid token
def NewsletterScheduler_request(request=None,user=None):
    if request:
       obj = NewsletterScheduler(request.user)
    else:
       obj = NewsletterScheduler(user)
    obj.generate_newsletter_content()
    return Response("Great")
    #return Response(obj.generate_newsletter_content())