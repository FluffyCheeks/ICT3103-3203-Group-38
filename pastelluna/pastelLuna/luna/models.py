from django.db import models

# Database schemas.
# note all id is created as pk

class Roles(models.Model):
    permissions = models.CharField(max_length=20)
    role_desc = models.CharField(max_length=20)
