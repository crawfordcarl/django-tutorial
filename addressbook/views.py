from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from django.views import generic

from addressbook.models import Record, Title, City, County

def index(request):
   # latest_record_list = Record.objects.order_by('surname')
    latest_record_list = Record.objects.all().extra(select={'lower_name':'lower(surname)'}).order_by('lower_name')
    context = {'latest_record_list':latest_record_list }
    return render(request, 'addressbook/index.html', context)

"""
class IndexView(generic.ListView):
    template_name = 'addressbook/index.html'
    context_object_name = 'latest_record_list'
    def get_queryset(self):
        return Record.objects.order_by('-surname')
"""

"""
def detail(request, record_id):
    record = get_object_or_404(Record, pk=record_id)
    return render(request, 'addressbook/detail.html', {'record':record})
"""

class DetailView(generic.DetailView):
    model = Record
    template_name = 'addressbook/detail.html'

"""
DetailView requires a pk, which we dont have yet (could get one, but why when the view below works)
class AddrecordView(generic.DetailView):
    model = Record
    template_name = 'addressbook/addrecord.html'
"""

def addrecord(request):
    ## objects come from database, so for busy apps, populating elements with such objects may not be wise (not noticeable slower but database could crash)
    titles = Title.objects.all()
    cities = City.objects.all()
    counties = County.objects.all()
    context = { 'titles': titles, 'cities': cities, 'counties': counties }
    return render(request, 'addressbook/addrecord.html', context)

def submitrecord(request):
    #create new record
    r = Record()

    ## get drop down menu objects
    t = get_object_or_404(Title, pk=request.POST['title'])
    ci = get_object_or_404(City, pk=request.POST['city'])
    co = get_object_or_404(County, pk=request.POST['county'])
    
    ##set values to new record
    r.title = t
    r.firstname = request.POST['forename']
    r.surname = request.POST['surname']
    r.address_line_1 = request.POST['address_line_1']
    r.address_line_2 = request.POST['address_line_2']
    r.address_line_3 = request.POST['address_line_3']
    r.city = ci
    r.county = co
    r.postcode = request.POST['postcode']

    r.save()
    return HttpResponseRedirect(reverse('addressbook:index'))

            
