from django.shortcuts import render
from .forms import get_data
import asyncio
from .osm_api_wrapper import osm_get_score, get_changeset
# Create your views here.

def index(request):
    form = get_data
    if request.method == 'POST':
        form = get_data(request.POST)
        if form.is_valid():
            display_name = form.cleaned_data['display_name']
            osm_username = form.cleaned_data['osm_username']
            mw_username = form.cleaned_data['mw_username']
            email_address = form.cleaned_data['email']
            go = asyncio.run(get_changeset(osm_username))
            print(go)
            print(display_name, osm_username, mw_username, email_address)
    return render(request, 'mainpage/index.html', {'form':form})

