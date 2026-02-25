from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.medicines.models import Medicine


@login_required
def medicine_list(request):
    medicines = Medicine.objects.all().order_by('name')
    return render(request, 'medicines/list.html', {'medicines': medicines})


@login_required
def medicine_create(request):
    if request.method == 'POST':
        Medicine.objects.create(
            name=request.POST.get('name'),
            type=request.POST.get('type'),
            strength=request.POST.get('strength'),
            brand=request.POST.get('brand'),
            instructions=request.POST.get('instructions'),
        )
        return redirect('medicines:list')

    return render(request, 'medicines/create.html')
