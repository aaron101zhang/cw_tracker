from django import forms
from .scraper import scrapeData
from .models import AuthorizedUser, DailyData, Participant, PlayDate

class UpdateForm(forms.Form):
    crossword_URL = forms.CharField()

    def post_data(self):
        # post crossword data for the day using the self.cleaned_data dictionary
        url = self.cleaned_data["crossword_URL"]
        if("https://downforacross.com" not in url):
            raise ValidationError(
                        _('Invalid link: %(value)s'),
                        params={'value': url},
                    )
        auth_users = (list(AuthorizedUser.objects.all().values_list('name',flat=True)))
        #try
        data = scrapeData(url, auth_users)

        playerContributions = data[0]
        date = data[1]
        time = data[2]
        #print(playerContributions)

        dat = PlayDate(date=date)
        dat.save()
        #insert DailyData
        d = DailyData(date = dat, link = url, duration = time)
        d.save()

        #insert Participant
        for k,v in playerContributions.items():
            entry = AuthorizedUser.objects.get(name = k)
            if entry in AuthorizedUser.objects.all():
                p = Participant(alias=entry, cells=v, date=dat)
                p.save()

            

        pass