from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Employer
from .forms import EmployerForm

@login_required
def employer_profile_create(request):
    if request.method == 'POST':
        form = EmployerForm(request.POST, request.FILES)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.user = request.user
            employer.save()
            return redirect('employer_profile_detail', pk=employer.pk)
    else:
        form = EmployerForm()
    return render(request, 'employers/employer_profile_create.html', {'form': form})

@login_required
def employer_profile_edit(request, pk):
    employer = get_object_or_404(Employer, pk=pk, user=request.user)
    if request.method == 'POST':
        form = EmployerForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            form.save()
            return redirect('employer_profile_detail', pk=employer.pk)
    else:
        form = EmployerForm(instance=employer)
    return render(request, 'employers/employer_profile_edit.html', {'form': form, 'employer': employer})

def employer_profile_detail(request, pk):
    employer = get_object_or_404(Employer, pk=pk)
    return render(request, 'employers/employer_profile_detail.html', {'employer': employer})
