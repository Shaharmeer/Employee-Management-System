from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Chat(models.Model):
    message = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.message
