from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
# Create your models here.


class MyUser(AbstractUser):
    displayname = models.CharField(max_length=50)
    # REQUIRED_FIELDS = ['displayname']


class Ticket(models.Model):
    title = models.CharField(max_length=50)
    add_time = models.DateTimeField(default=datetime.now)
    description = models.TextField()
    author = models.ForeignKey(MyUser, related_name='author', on_delete=models.CASCADE)

    NEW = 'New'
    INP = 'In_Progress'
    F = 'Finished'
    IN = 'Invalid'

    ticket_status_choices = [
        (NEW, 'New'),
        (INP, 'In_Progress'),
        (F, 'Finished'),
        (IN, 'Invalid'),
    ]
    ticket_status = models.CharField(max_length=30, choices=ticket_status_choices, default=NEW)
    ticket_person = models.ForeignKey(MyUser, null=True, related_name='ticketperson', on_delete=models.CASCADE)
    ticket_done_by = models.ForeignKey(MyUser, related_name='ticketdoneby', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
