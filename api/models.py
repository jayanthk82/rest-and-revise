from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# --- v1.0 Model ---
class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_text = models.TextField()
    summary_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Summary for {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
# --- v2.0 Models ---
class Problem(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    weblink = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.title
class Solution(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solution_programming_languaage = models.CharField(max_length = 30)
    solution = models.TextField()
    ai_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"solution for {self.problem.title} by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
class Newsletterslog(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    newsletter_date = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0,null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Newsletter log for {self.user.username} on {self.newsletter_date.strftime('%Y-%m-%d')}"