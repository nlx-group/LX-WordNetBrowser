from __future__ import unicode_literals
from django.db import models


# Create your models here.

class Search(models.Model):
	search_term = models.CharField(max_length=512)

	def __str__(self):
		return self.search_term