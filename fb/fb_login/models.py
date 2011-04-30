from django.db import models
from django.contrib.auth.models import User


class FacebookUser(models.Model):
	id = models.CharField(primary_key = True, max_length = 100)
	user = models.ForeignKey(User)
