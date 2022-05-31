from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Rent
from .forms import RentForm

from django.core.paginator import Paginator

# Create your views here.
def rent_list(request):
    rents_list = Rent.objects.order_by('-pk')

    page = request.GET.get('page',1)
    paginator = Paginator(rents_list, 6)
    rents = paginator.get_page(page)

    context = {
        'rents': rents,
    }
    return render(request, 'rents/list.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def rent_write(request):
    if request.method=="POST":
        form = RentForm(request.POST)
        if form.is_valid():
            rent = form.save(commit=False)
            rent.user = request.user
            rent.save()
            return redirect('rents:')
    form = RentForm()
    context = {
        'form': form,
    }
    return render(request, 'rents/write.html', context)


@require_http_methods(['GET'])
def rent_content(request, rent_id):
    rent = get_object_or_404(Rent, pk=rent_id)
    context = {
        'rent': rent,
    }
    return render(request, 'rents/detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def rent_edit(request, rent_id):
    rent = get_object_or_404(Rent, pk=rent_id)
    if request.user == rent.user:
        if request.method=="POST":
            print(request.POST)
            form = RentForm(request.POST, instance=rent)
            if form.is_valid():
                form.save()
                return redirect('rents:content', rent.id)  
    else:
        return redirect('rents:content', rent.id)
    form = RentForm(instance=rent)
    context = {
        'form': form,
        'rent': rent,
    }    
    return render(request, 'rents/edit.html', context)


@login_required
@require_http_methods(['POST'])
def rent_remove(request, rent_id):
    rent = get_object_or_404(Rent, pk=rent_id)
    if request.user == rent.user:
        rent.delete()
    return redirect('rents:')  



