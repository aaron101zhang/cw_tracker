from django.db import models
import datetime

# Create your models here.
                         
class PlayDate(models.Model):
    date = models.DateField(primary_key=True)

def get_default_date():
    return PlayDate.objects.get(date=datetime.datetime(1970, 1, 1))

class AuthorizedUser(models.Model):
    name = models.CharField(max_length=20, primary_key = True)

    def __str__(self):
        return self.name

def get_default_user():
    return AuthorizedUser.objects.get(name="")

class DailyData(models.Model):
    date = models.ForeignKey(PlayDate, default=get_default_date, on_delete=models.CASCADE)
    link = models.CharField(max_length=50)
    duration = models.DurationField()
    def __str__(self):
        return self.link

def get_default_daily_data():
    return DailyData.objects.get(date=datetime.datetime(1970, 1, 1),
                                    link = "",
                                    duration = datetime.timedelta())

class Participant(models.Model):
    alias = models.ForeignKey(AuthorizedUser, default=get_default_user, on_delete=models.CASCADE)
    cells = models.PositiveIntegerField()
    date = models.ForeignKey(PlayDate, default=get_default_date, on_delete=models.CASCADE)
