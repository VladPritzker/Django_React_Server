from django.db import models

class DailyActivityBase(models.Model):
    date = models.DateField()
    slept = models.TimeField(null=True)
    studied = models.BooleanField(null=True)
    wokeUp = models.TimeField(null=True)

    class Meta:
        abstract = True  # This model will not create any database table

def get_daily_activity_model(year, month):
    class_name = f'DailyActivity_{year}_{month:02d}'
    db_table_name = f'daily_activity_{year}_{str(month).zfill(2)}'

    class Meta:
        managed = False
        db_table = db_table_name

    # Dynamically create a model class
    return type(class_name, (DailyActivityBase,), {
        '__module__': 'myapp.models',
        'Meta': Meta,
    })
