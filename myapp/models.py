from django.db import models

class DailyActivity(models.Model):
    date = models.DateField()
    slept = models.TimeField(null=True)
    studied = models.BooleanField(null=True)
    wokeUp = models.TimeField(null=True)



    class Meta:
        managed = True  # Django won't create or modify tables
        db_table = 'daily_activity_2024_01'  # Change xx to the specific month as needed
