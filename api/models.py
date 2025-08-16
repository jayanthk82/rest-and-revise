from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_text = models.TextField()
    summary_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Summary created at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

class UserNote(models.Model):
    # This creates a link to Django's built-in User model.
    # on_delete=models.CASCADE means if a User is deleted,
    # all of their notes will be deleted too.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    original_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"'{self.title}' by {self.user.username}"
    