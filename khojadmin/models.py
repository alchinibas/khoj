from django.db import models
import django
class PendingUrl(models.Model):
    requestDate = models.DateTimeField(default=django.utils.timezone.now)
    url=models.CharField(max_length = 255)

    def __str__(self):
        return self.url

class Feedback(models.Model):
    email=models.EmailField()
    message = models.TextField()
    messageDate = models.DateTimeField(default = django.utils.timezone.now)

    def __str__(self):
        if(len(self.message)>100):
            return self.message[:100]+"..."
        else:
            return self.message
