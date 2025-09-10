from django.db import models
from django.contrib.auth.models import User

  
# --- v2.0 Models ---
class Problems(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField()
    solution = models.TextField()
    ai_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.AutoField(primary_key=True)
    recent_date = models.DateField(null=True, blank=True,auto_now_add = True)
    count = models.IntegerField(default=0)
    proficiency_rating = models.IntegerField(default=0,null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"Newsletter log and solution for {Problems.title} by  at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
        
#Temporary changes on the newsletter logs future if any error with newsletterlogs use this code
##   user = models.ForeignKey(User,on_delete = models.CASCADE)
    #problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True, blank=True)
    #newsletter_dates = models.JSONField(default = list,blank = True) 'if needed can add in future' 
  ## count = models.IntegerField(default=0)
    #proficiency_rating = models.IntegerField(default=0,null=True, blank=True)
    ##feedback = models.TextField(null=True, blank=True)
    #def __str__(self):
    #    return f"Newsletter log for {self.user.username} on {self.recent_date.strftime('%Y-%m-%d')}"
    #'''