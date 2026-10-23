from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ServiceForm
from .models import Service
from labor.models import LaborProfile


@login_required
def create_service(request):

    if request.user.role != 'LABOR':
        return redirect('/')

    labor_profile = LaborProfile.objects.filter(
        user=request.user
    ).first()

    if not labor_profile:
        return redirect('/labor/create-profile/')

    if request.method == 'POST':

        form = ServiceForm(request.POST)

        if form.is_valid():

            service_name = form.cleaned_data['name']

            existing_service = Service.objects.filter(
                labor=labor_profile,
                name__iexact=service_name
            ).first()

            if existing_service:
                form.add_error(
                    'name',
                    'You already have a service with this name.'
                )

            else:
                service = form.save(commit=False)
                service.labor = labor_profile
                service.save()

                return redirect('/services/list/')

    else:
        form = ServiceForm()

    return render(
        request,
        'services/create_service.html',
        {
            'form': form
        }
    )


@login_required
def service_list(request):

    if request.user.role != 'LABOR':
        return redirect('/')

    labor_profile = LaborProfile.objects.filter(
        user=request.user
    ).first()

    if not labor_profile:
        return redirect('/labor/create-profile/')

    services = Service.objects.filter(
        labor=labor_profile
    ).order_by('-id')

    return render(
        request,
        'services/service_list.html',
        {
            'services': services
        }
    )


@login_required
def edit_service(request, service_id):

    if request.user.role != 'LABOR':
        return redirect('/')

    labor_profile = LaborProfile.objects.filter(
        user=request.user
    ).first()

    if not labor_profile:
        return redirect('/labor/create-profile/')

    service = Service.objects.filter(
        id=service_id,
        labor=labor_profile
    ).first()

    if not service:
        return redirect('/services/list/')

    if request.method == 'POST':

        form = ServiceForm(
            request.POST,
            instance=service
        )

        if form.is_valid():

            service_name = form.cleaned_data['name']

            existing_service = Service.objects.filter(
                labor=labor_profile,
                name__iexact=service_name
            ).exclude(
                id=service.id
            ).first()

            if existing_service:

                form.add_error(
                    'name',
                    'You already have a service with this name.'
                )

            else:

                form.save()

                return redirect('/services/list/')

    else:

        form = ServiceForm(
            instance=service
        )

    return render(
        request,
        'services/edit_service.html',
        {
            'form': form,
            'service': service
        }
    )

@login_required
def delete_service(request, service_id):

    if request.user.role != 'LABOR':
        return redirect('/')

    labor_profile = LaborProfile.objects.filter(
        user=request.user
    ).first()

    if not labor_profile:
        return redirect('/labor/create-profile/')

    service = Service.objects.filter(
        id=service_id,
        labor=labor_profile
    ).first()

    if not service:
        return redirect('/services/list/')

    if request.method == 'POST':
        service.delete()
        return redirect('/services/list/')

    return render(
        request,
        'services/delete_service.html',
        {
            'service': service
        }
    )