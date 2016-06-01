from django.shortcuts import render
import requests

def jan_analysis_summary(request):
    return analysis_summary(request, 'jan')


def felix_analysis_summary(request):
    return analysis_summary(request, 'felix')


def analysis_summary(request, ms_name):
    # get latest analysis. need runid and repository
    runid, repository = get_latest_analysis(ms_name)
    # get summary from github
    context = get_summary_context(runid, repository)

    return render(request, 'status/analysis_view.html', context)


def get_latest_analysis(ms_name):
    runid, repository = '',''
    return runid, repository


def get_summary_context(runid, repository, **kw):
    j = get_summary_json(runid, repository, **kw)
    return j


def get_summary_json(runid, repository,
                branch='master',
                organization='NMGRLData'):

    head, tail = runid[:3], runid[3:]
    p = '{}/{}/{}/{}/{}.json'.format(organization, repository,
                     branch, head, tail)
    url = 'https://raw.githubusercontent.com/{}'.format(p)
    r = requests.get(url)
    return r.json()