from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.medicines.models import Medicine


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Medicine


@login_required
def medicine_manage(request):
    # Create Medicine
    if request.method == "POST":
        name = request.POST.get("name")
        type_ = request.POST.get("type")
        strength = request.POST.get("strength")
        brand = request.POST.get("brand")
        instructions = request.POST.get("instructions")

        if not name or not type_ or not strength:
            messages.error(request, "Name, Type and Strength are required.")
        else:
            Medicine.objects.create(
                name=name,
                type=type_,
                strength=strength,
                brand=brand,
                instructions=instructions,
            )
            messages.success(request, "Medicine added successfully.")
            return redirect("medicines:manage")

    # Search Medicine
    query = request.GET.get("q")
    medicines = Medicine.objects.all()

    if query:
        medicines = medicines.filter(
            Q(name__icontains=query) |
            Q(type__icontains=query) |
            Q(strength__icontains=query) |
            Q(brand__icontains=query)
        )

    medicines = medicines.order_by("name")

    return render(request, "medicines/manage.html", {
        "medicines": medicines,
        "query": query,
    })