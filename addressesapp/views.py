from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse

from .models import Person

import logging
import urllib
from ast import literal_eval

# Create your views here.
def main(request):
    context={}

    if request.method == 'POST':
        post_data = request.POST
        data = {}
        data['name'] = post_data.get('name', None)
        data['email'] = post_data.get('email', None)

        if data:
            return redirect('%s?%s' % (reverse('addressesmain'),
                urllib.parse.urlencode({'q': data})))
                # urllib.urlencode({'q': data})))

    elif request.method == 'GET':
        get_data = request.GET
        data= get_data.get('q',None)

        if not data:
            # return render_to_response('addressesapp/home.html', RequestContext(request,context))
            return render(request, 'addressesapp/home.html')
            
        data = literal_eval(get_data.get('q',None))
        print(data)

        if not data['name'] and not data['email']:
            return render(request, 'addressesapp/home.html')
        
        #add person to emails address book or update
        if Person.objects.filter(name=data['name']).exists():
            p = Person.objects.get(name=data['name'])
            p.mail=data['email']
            p.save()
        else:
            p = Person()
            p.name=data['name']
            p.mail=data['email']
            p.save()

        #restart page
        return render(request, 'addressesapp/home.html')


def get_contacts(request):
    logging.debug('here')

    if request.method == 'GET':
        get_data = request.GET
        data= get_data.get('term','')
        logging.debug('term')
        
        if data == '':
            return render(request, 'addressesapp/nopersonfound.html')
        else:
            return redirect('%s?%s' % (reverse('addressesbook'),
                urllib.parse.urlencode({'letter': data})))
                # urllib.urlencode({'letter': data})))

    return render(request, 'addressesapp/home.html')

def addressesbook(request):
    context = {}
    logging.debug('address book')
    get_data = request.GET
    letter = get_data.get('letter',None)
    
    if letter:
        contacts = Person.objects.filter(name__iregex=r"(^|\s)%s" % letter)
    else:
        contacts = Person.objects.all()

    #sorted alphabetically
    contacts = sort_lower(contacts,"name") # contacts.order_by("name")
    context['contacts']=contacts
    alphabetstring='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    context['alphabet']=[l for l in alphabetstring]

    return render(request, 'addressesapp/book.html', context)

def sort_lower(lst, key_name):
    return sorted(lst, key=lambda item: getattr(item, key_name).lower())            

def delete_person(request,name):
    if Person.objects.filter(name=name).exists():
        p = Person.objects.get(name=name)
        p.delete()

    context = {}
    contacts = Person.objects.all()

    #sorted alphabetically
    contacts = sort_lower(contacts,"name") #contacts.order_by("name")
    context['contacts']=contacts
    
    return render(request, 'addressesapp/book.html')

def notfound(request):
    context ={}
    return render(request, 'addressesapp/nopersonfound.html')