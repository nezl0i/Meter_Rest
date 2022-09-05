import datetime
import os

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from meters.models import Rating, Meter, Branches
from django.template.loader import render_to_string
from django.http import JsonResponse

MODULE_DIR = os.path.dirname(__file__)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required()
def rating(request, filters=None, exclude=None):
    last_date = Rating.date_pools()[0]['pool_date']
    query_last_date = Rating.objects\
        .select_related('branch')\
        .filter(pool_date=last_date)

    _last_rating = query_last_date\
        .order_by('-percent')\
        .exclude(branch_id=12)

    return _last_rating


@login_required()
def pre_rating(request):
    pre_date = Rating.date_pools()[1]['pool_date']
    query_pre_date = Rating.objects\
        .select_related('branch')\
        .filter(pool_date=pre_date)

    _pre_rating = query_pre_date\
        .order_by('-percent')\
        .exclude(branch_id=12)

    return _pre_rating


@login_required()
def index(request):
    context = {'segment': 'index', 'pool_date': Rating.date_pools(), 'pk': 1}

    last_date = Rating.date_pools()[0]['pool_date']
    pre_date = Rating.date_pools()[1]['pool_date']

    query_last_date = Rating.objects\
        .select_related('branch')\
        .filter(pool_date=last_date, meter_id=11)

    last_rating = query_last_date\
        .order_by('-percent')\
        .exclude(branch_id=12)

    query_pre_date = Rating.objects\
        .select_related('branch')\
        .filter(pool_date=pre_date, meter_id=11)

    pre_rating = query_pre_date\
        .order_by('-percent')\
        .exclude(branch_id=12)

    context['pre_rating'] = pre_rating

    if last_rating.exists():
        context['rating'] = enumerate(last_rating, 1)

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required()
def tables_rating(request):
    context = {'segment': 'index', 'pool_date': Rating.date_pools(), 'pk': 1}

    branches = Branches.objects.all().exclude(id=12)
    meters = Meter.objects.all().exclude(id=11)

    context['pre_rating'] = pre_rating(request)
    context['branches'] = branches
    context['meters'] = meters
    context['rating'] = rating(request)

    html_template = loader.get_template('home/meters.html')
    return HttpResponse(html_template.render(context, request))


@login_required()
def statistic(request, date):
    date_ = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    rating = None
    pre_rating = None
    index_ = 0

    date_pools = Rating.date_pools()

    for key, _ in enumerate(date_pools):
        if _['pool_date'] == date_:
            index_ = key

    pre_date = date_pools[index_ + 1]['pool_date']
    context = {'rating': rating, 'pre_rating': pre_rating}

    if is_ajax(request=request):
        rating = Rating.objects\
            .select_related('branch')\
            .filter(pool_date=date, meter_id=11) \
            .order_by('-percent') \
            .exclude(branch_id=12)

        pre_rating = Rating.objects\
            .select_related('branch')\
            .filter(pool_date=pre_date, meter_id=11) \
            .order_by('-percent') \
            .exclude(branch_id=12)

    if rating.exists():
        context['rating'] = enumerate(rating, 1)
        context['pre_rating'] = pre_rating
    print(rating.values())

    result = render_to_string('includes/rating.html', context)
    return JsonResponse({'result': result})


@login_required()
def meters(request, date):
    date_ = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    rating = None
    pre_rating = None
    index_ = 0

    branches = Branches.objects.all().exclude(id=12)
    meters = Meter.objects.all().exclude(id=11)

    date_pools = Rating.date_pools()

    for key, _ in enumerate(date_pools):
        if _['pool_date'] == date_:
            index_ = key

    pre_date = date_pools[index_ + 1]['pool_date']
    context = {'rating': rating, 'pre_rating': pre_rating}

    if is_ajax(request=request):
        rating = Rating.objects\
            .select_related('branch')\
            .filter(pool_date=date) \
            .order_by('-percent') \
            .exclude(branch_id=12)

        pre_rating = Rating.objects\
            .select_related('branch')\
            .filter(pool_date=pre_date) \
            .order_by('-percent') \
            .exclude(branch_id=12)

    if rating.exists():
        context['rating'] = rating
        context['pre_rating'] = pre_rating
        context['branches'] = branches
        context['meters'] = meters

    result_2 = render_to_string('includes/tablerating.html', context)
    return JsonResponse({'result': result_2})


@login_required()
def pages(request):
    context = {}
    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        print(e)
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
