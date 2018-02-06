from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class Note(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    owner = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE)

    def was_published_recently(self):
        now = timezone.now()
        return now - timezone.timedelta(days=1) <= self.pub_date <= now

    def __str__(self):
        return self.title

