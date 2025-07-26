from django.db import models

# Create your models here.
class Summary(models.Model):
    original_text = models.TextField()
    summary_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Summary created at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
