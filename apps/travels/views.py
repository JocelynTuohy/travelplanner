# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from ..login.models import User
from .models import Plan

# Create your views here.
def index(request):
    print '!'*100
    userid = request.session['id']
    context = {
        'user': User.objects.filter(id=userid),
        'mytrips': Plan.objects.myAdventures(userid),
        'othertrips': Plan.objects.otherAdventures(userid),
    }
    print context['user'][0].name
    return render(request, 'travels/index.html', context)

def destination(request, id):
    print '@'*100
    print User.objects.get(id=request.session['id']).adventures
    print User.objects.get(id=request.session['id']).created
    try:
        this_plan = Plan.objects.get(id=id)
        context = {
            'plan': this_plan,
            'others': Plan.objects.otherAdventurers(id)
        }
        return render(request, 'travels/destination.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('travels:index'))

def addpage(request):
    print '#'*100
    return render(request, 'travels/addpage.html')

def join(request, id):
    print '$'*100
    Plan.objects.joinAdventure(id, request.session['id'])
    return redirect(reverse('travels:index'))

def addthis(request):
    print '%'*100
    if request.method == 'POST':
        errors = Plan.objects.validAdventure(request.POST)
        if errors:
            for each in errors:
                messages.error(request, each)
            return redirect(reverse('travels:addpage'))
        else:
            Plan.objects.createAdventure(request.POST, request.session['id'])
            return redirect(reverse('travels:index'))
    return redirect(reverse('travels:addpage'))
