from django.shortcuts import render
from .models import Leaderboard

# Create your views here.
def leaderboard(request):
    data = Leaderboard.objects.all().order_by('-total_score')
    return render(request, 'view_leaderboard/leaderboard.html',{'datas':data})