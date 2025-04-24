from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import PollingUnit, AnnouncedPUResult, LGA, Ward, Party, AnnouncedLGAResult
from django.db.models import Sum

# Question 1: Display results for a polling unit
def polling_unit_result(request, polling_unit_id):
    try:
        polling_unit = PollingUnit.objects.get(uniqueid=polling_unit_id)
        results = AnnouncedPUResult.objects.filter(polling_unit=polling_unit)
        context = {
            'polling_unit': polling_unit,
            'results': results
        }
        return render(request, 'polling_unit_result.html', context)
    except PollingUnit.DoesNotExist:
        return render(request, 'error.html', {'message': 'Polling unit not found'})

# Question 2: Summed total results for all polling units in an LGA
def lga_summed_results(request):
    lgas = LGA.objects.all()
    selected_lga_id = request.GET.get('lga_id')
    summed_results = None

    if selected_lga_id:
        selected_lga = get_object_or_404(LGA, lga_id=selected_lga_id)
        summed_results = (
            AnnouncedPUResult.objects
            .filter(polling_unit__lga=selected_lga)
            .values('party_abbreviation')
            .annotate(total_score=Sum('party_score'))
            .order_by('-total_score')
        )

    context = {
        'lgas': lgas,
        'selected_lga': selected_lga if selected_lga_id else None,
        'summed_results': summed_results
    }
    return render(request, 'lga_summed_results.html', context)

# Question 3: Store results for a new polling unit
def store_polling_unit_result(request):
    if request.method == 'POST':
        # Get form data
        polling_unit_id = request.POST.get('polling_unit_id')
        party_scores = request.POST.getlist('party_score')
        party_abbreviations = request.POST.getlist('party_abbreviation')
        
        try:
            polling_unit = PollingUnit.objects.get(uniqueid=polling_unit_id)
            
            # Save each party result
            for i in range(len(party_abbreviations)):
                AnnouncedPUResult.objects.create(
                    polling_unit=polling_unit,
                    party_abbreviation=party_abbreviations[i],
                    party_score=int(party_scores[i]),
                    entered_by_user=request.user.username if request.user.is_authenticated else 'Anonymous',
                    user_ip_address=request.META.get('REMOTE_ADDR', '')
                )
            
            return redirect('polling_unit_result', polling_unit_id=polling_unit_id)
        
        except PollingUnit.DoesNotExist:
            return render(request, 'error.html', {'message': 'Polling unit not found'})
    
    else:
        # For GET request, show the form
        lgas = LGA.objects.all()
        parties = Party.objects.all()
        context = {
            'lgas': lgas,
            'parties': parties
        }
        return render(request, 'store_polling_unit_result.html', context)

# AJAX view to get wards for a selected LGA
def get_wards(request):
    lga_id = request.GET.get('lga_id')
    wards = Ward.objects.filter(lga_id=lga_id).order_by('ward_name')
    return render(request, 'ward_dropdown.html', {'wards': wards})

# AJAX view to get polling units for a selected ward
def get_polling_units(request):
    ward_id = request.GET.get('ward_id')
    polling_units = PollingUnit.objects.filter(ward_id=ward_id).order_by('polling_unit_name')
    return render(request, 'polling_unit_dropdown.html', {'polling_units': polling_units})

def home(request):
    """Simple home page view"""
    return render(request, 'home.html')
