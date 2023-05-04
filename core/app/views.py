from django.shortcuts import render
from .models import Contact, Product
from  django.contrib import messages
from math import ceil

# Create your views here.


def index(request):
    allProds = []
    catProds = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catProds}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
        print([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, "index.html", params)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get('email')
        desc = request.POST.get('desc')
        pnumber=request.POST.get('pnumber')
        myquery = Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
        myquery.save()
        return render(request, "index.html")

    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")
