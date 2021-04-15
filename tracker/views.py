from django.shortcuts import render
from django.shortcuts import redirect
# Create your views here.
from .models import DailyData, Participant
from tracker.forms import UpdateForm
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from django.db.models import Sum

class DayListView(ListView):
    model = DailyData
    template_name = 'home.html'
    ordering = ['-date']
    
class UpdateFormView(FormView):
    template_name = 'form.html'
    form_class = UpdateForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.post_data()
        return super().form_valid(form)

class ParticipantView(ListView):
    model = Participant
    template_name = 'participants.html'


    def get_queryset(self, **kwargs):
        #primary key of base data
        pk = self.kwargs["pk"]
        #grabs date from dd primary key
        date = DailyData.objects.get(pk=pk).date

        return super().get_queryset().filter(date=date)
        
        
        #join participants with date of dailydata

class ATLeaderboardView(ListView):
    model = Participant
    template_name = 'leaderboard.html'
    queryset = Participant.objects.values('alias').annotate(total_cells=Sum('cells')).order_by('-total_cells')
