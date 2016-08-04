from django.db import models

class custom_commands(models.Model):
    USERLEVELS = (('m', 'mod'),
                  ('s', 'subscriber'),
                  ('e', 'everyone'))
    command = models.CharField(max_length=200, primary_key=True, unique=True)
    command_type = models.CharField(max_length=512)
    message = models.CharField(max_length=512)
    userlevel = models.CharField(max_length=15, choices=USERLEVELS)


