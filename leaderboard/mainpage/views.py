from django.shortcuts import render, redirect
from .forms import get_data
import asyncio
from .osm_api_wrapper import osm_get_score, get_changeset
from .mw_api_wrapper import get_response
# Create your views here.

def index(request):
    form = get_data
    error_message = ""
    if request.method == 'POST':
        form = get_data(request.POST)
        if form.is_valid():
            display_name = form.cleaned_data['display_name']
            osm_username = form.cleaned_data['osm_username']
            mw_username = form.cleaned_data['mw_username']
            email_address = form.cleaned_data['email']
            if osm_username.strip() != '':
                test_user = asyncio.run(get_changeset(osm_username))
                if test_user != 'Object not found':
                    pass
                else:
                    error_message = 'Invalid OSM Username'
                    render(request, 'mainpage/index.html',{'form':form,'error':error_message})
            if mw_username.strip() != '':
                test_user = asyncio.run(get_response(mw_username))
                try:
                    if test_user['query']['users'][0]['missing'] == '':
                        error_message += ' Invalid MediaWiki Username'
                        render(request, 'mainpage/index.html',{'form':form,'error':error_message})
                except:
                    pass
            # print(go)
            print(display_name, osm_username, mw_username, email_address)
    return render(request, 'mainpage/index.html', {'form':form,'error':error_message})

