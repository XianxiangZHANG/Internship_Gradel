from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

from web import models
import django_filters

class R_and_DFilter(django_filters.FilterSet):

    class Meta:
        model = models.R_and_D
        fields = {
            'program': ['icontains'], 
            'projectNr': ['icontains'],
            'ERMDS': ['icontains'],
            'fiber': ['exact'],
            'resin': ['exact'],
        }

def r_and_d_list(request):
    """ list of r_and_d """

    r_and_d_filter = R_and_DFilter(request.GET, queryset=models.R_and_D.objects.all())
    return render(request, 'r_and_d/r_and_d_list.html', {'filter': r_and_d_filter})

# def r_and_d_detail(request, ermds_id):
#     randd = get_object_or_404(models.R_and_D, ERMDS=ermds_id)
#     comments = models.RDComment.objects.filter(ERMDS=randd)
#     return render(request, 'r_and_d_list.html', {'randd': randd, 'comments': comments})

def r_and_d_input(request):
    """ list of r_and_d """

    # [obj,]
    queryset = models.R_and_D.objects.all().order_by("id")
    # for row in queryset:
    #     print(row.username, row.password, row.gender, row.get_gender_display(), row.depart_id, row.depart.title)
    
    return render(request, 'r_and_d/r_and_d_input.html', {"queryset": queryset})


class R_and_DModelForm(forms.ModelForm):
    class Meta:
        model = models.R_and_D
        fields = ['program', 'projectNr',
                'ERMDS', 'lastUpdate', 'verifiedBy', 'approvedBy',
                'fiber', 'numberOfBobbins', 'resin', 
                'endEffector', 'impregnationBath', 'entryNozzleDiam', 'exitNozzleDiam',
                'roomTemperature', 'roomhumidity',
                'brakeForcebobin', 'windingSpeedRange',
                'FVR', 'compositeDensity', 'porosity', 'theoreticalSampleSection', 'experimentalSampleSection', 'aged', 'temperatureOfTests',
                'numberOfSamples', 'configurarion', 'sampleLength', 'numberOfCycles', 'sleeve',
                'thermalExpansionCoefficient', 'thermalConductivity',
                'tensileYoungModulus', 'tensileUltimateStress', 'tensileUltimateStressMA', 'tensileUltimateStressMB',
                'tensileUltimateLoad', 'tensileYieldStress', 'tensileYieldStressMA', 'tensileYieldStressMB', 'tensileYieldLoad',
                'compressionYoungModulus', 'compressionUltimateStress', 'compressionUltimateStressMA', 'compressionUltimateStressMB',
                'compressionUltimateLoad', 'compressionYieldStress', 'compressionYieldStressMA', 'compressionYieldStressMB', 'compressionYieldLoad', 'poissonRatio',
                'flexuralModulusILSS', 'ultimateShearForce', 'ultimateShearStress', 'ultimateShearStressMA', 'ultimateShearStressMB',
                'flexuralModulusF', 'flexuralUltimateStrength', 'flexuralUltimateStrengthMA', 'flexuralUltimateStrengthMB', 'strainUltimateStrength', 'flexuralUltimateForce',
                'yieldTorque', 'maxiTorque', 'yieldAngle', 'maxiTwistedAngle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


class RDCommentModelForm(forms.ModelForm):
    class Meta:
        model = models.RDComment
        fields = [
                'fiber', 'numberOfBobbins', 'resin', 
                'endEffector', 'impregnationBath', 'entryNozzleDiam', 'exitNozzleDiam',
                'roomTemperature', 'roomhumidity',
                'brakeForcebobin', 'windingSpeedRange',
                'FVR', 'compositeDensity', 'porosity', 'theoreticalSampleSection', 'experimentalSampleSection', 'aged', 'temperatureOfTests',
                'numberOfSamples', 'configurarion', 'sampleLength', 'numberOfCycles', 'sleeve',
                'thermalExpansionCoefficient', 'thermalConductivity',
                'tensileYoungModulus', 'tensileUltimateStress', 'tensileUltimateStressMA', 'tensileUltimateStressMB',
                'tensileUltimateLoad', 'tensileYieldStress', 'tensileYieldStressMA', 'tensileYieldStressMB', 'tensileYieldLoad',
                'compressionYoungModulus', 'compressionUltimateStress', 'compressionUltimateStressMA', 'compressionUltimateStressMB',
                'compressionUltimateLoad', 'compressionYieldStress', 'compressionYieldStressMA', 'compressionYieldStressMB', 'compressionYieldLoad', 'poissonRatio',
                'flexuralModulusILSS', 'ultimateShearForce', 'ultimateShearStress', 'ultimateShearStressMA', 'ultimateShearStressMB',
                'flexuralModulusF', 'flexuralUltimateStrength', 'flexuralUltimateStrengthMA', 'flexuralUltimateStrengthMB', 'strainUltimateStrength', 'flexuralUltimateForce',
                'yieldTorque', 'maxiTorque', 'yieldAngle', 'maxiTwistedAngle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


class R_and_DForm(forms.ModelForm):
    class Meta:
        model = models.R_and_D
        fields = ['program', 'projectNr',
                'ERMDS', 'lastUpdate', 'verifiedBy', 'approvedBy',
                'fiber', 'numberOfBobbins', 'resin', 
                'endEffector', 'impregnationBath', 'entryNozzleDiam', 'exitNozzleDiam',
                'roomTemperature', 'roomhumidity',
                'brakeForcebobin', 'windingSpeedRange',
                'FVR', 'compositeDensity', 'porosity', 'theoreticalSampleSection', 'experimentalSampleSection', 'aged', 'temperatureOfTests',
                'numberOfSamples', 'configurarion', 'sampleLength', 'numberOfCycles', 'sleeve',
                'thermalExpansionCoefficient', 'thermalConductivity',
                'tensileYoungModulus', 'tensileUltimateStress', 'tensileUltimateStressMA', 'tensileUltimateStressMB',
                'tensileUltimateLoad', 'tensileYieldStress', 'tensileYieldStressMA', 'tensileYieldStressMB', 'tensileYieldLoad',
                'compressionYoungModulus', 'compressionUltimateStress', 'compressionUltimateStressMA', 'compressionUltimateStressMB',
                'compressionUltimateLoad', 'compressionYieldStress', 'compressionYieldStressMA', 'compressionYieldStressMB', 'compressionYieldLoad', 'poissonRatio',
                'flexuralModulusILSS', 'ultimateShearForce', 'ultimateShearStress', 'ultimateShearStressMA', 'ultimateShearStressMB',
                'flexuralModulusF', 'flexuralUltimateStrength', 'flexuralUltimateStrengthMA', 'flexuralUltimateStrengthMB', 'strainUltimateStrength', 'flexuralUltimateForce',
                'yieldTorque', 'maxiTorque', 'yieldAngle', 'maxiTwistedAngle']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


R_and_DFormSet = modelformset_factory(
    models.R_and_D,
    form=R_and_DModelForm,
    extra=1  # The number of additional forms added during initialization
)
RDCommentFormSet = modelformset_factory(
    models.RDComment,
    form=RDCommentModelForm,
    extra=1  # The number of additional forms added during initialization
)

R_and_DMultFormSet = modelformset_factory(
    models.R_and_D,
    form=R_and_DForm,
    extra=1  # The number of additional forms added during initialization
)

def r_and_d_add_multiple(request):
    formset = R_and_DFormSet(queryset=models.R_and_D.objects.none())
    formsetC = RDCommentFormSet(queryset=models.RDComment.objects.none())
    # r_and_dError = None

    if request.method == 'POST':
        formset = R_and_DFormSet(request.POST)
        formsetC = RDCommentFormSet(request.POST)
       
        # r_and_dName = request.POST.get('r_and_dName')
        # if not r_and_dName:
        #     r_and_dError = "Required"
        if formset.is_valid() and formsetC.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.save()
            instancesC = formsetC.save(commit=False)
            for instanceC in instancesC:
                instanceC.save()
            return redirect('/r_and_d/list/')  # Replace with your redirect URL

    return render(request, 'r_and_d/r_and_d_add_multiple.html', {
        'formset': formset,
        'formset': formsetC,
    })


def r_and_d_modify_multiple(request):
    # Get filtered data
    r_and_d_filter = R_and_DFilter(request.GET, queryset=models.R_and_D.objects.all())
    
    # Define form set
    R_and_DFormSet = modelformset_factory(models.R_and_D, form=R_and_DModelForm, extra=0)
    
    if request.method == 'POST':
        formset = R_and_DFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/r_and_d/list/')
    else:
        formset = R_and_DFormSet(queryset=r_and_d_filter.qs)

    return render(request, 'r_and_d/r_and_d_modify_multiple.html', {
        'filter': r_and_d_filter,
        'formset': formset,
    })


def r_and_d_add(request):
    if request.method == "GET":
        form = R_and_DModelForm()
        return render(request, 'r_and_d/r_and_d_form.html', {"form": form})

    form = R_and_DModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'r_and_d/r_and_d_form.html', {"form": form})

    form.save()
    return redirect('/r_and_d/list/')


class R_and_DEditModelForm(forms.ModelForm):
    class Meta:
        model = models.R_and_D
        fields = ['program', 'projectNr',
                'ERMDS', 'lastUpdate', 'verifiedBy', 'approvedBy',
                'fiber', 'numberOfBobbins', 'resin',
                'endEffector', 'impregnationBath', 'entryNozzleDiam', 'exitNozzleDiam',
                'roomTemperature', 'roomhumidity',
                'brakeForcebobin', 'windingSpeedRange',
                'FVR', 'compositeDensity', 'porosity', 'theoreticalSampleSection', 'experimentalSampleSection', 'aged', 'temperatureOfTests',
                'numberOfSamples', 'configurarion', 'sampleLength', 'numberOfCycles', 'sleeve',
                'thermalExpansionCoefficient', 'thermalConductivity',
                'tensileYoungModulus', 'tensileUltimateStress', 'tensileUltimateStressMA', 'tensileUltimateStressMB',
                'tensileUltimateLoad', 'tensileYieldStress', 'tensileYieldStressMA', 'tensileYieldStressMB', 'tensileYieldLoad',
                'compressionYoungModulus', 'compressionUltimateStress', 'compressionUltimateStressMA', 'compressionUltimateStressMB',
                'compressionUltimateLoad', 'compressionYieldStress', 'compressionYieldStressMA', 'compressionYieldStressMB', 'compressionYieldLoad', 'poissonRatio',
                'flexuralModulusILSS', 'ultimateShearForce', 'ultimateShearStress', 'ultimateShearStressMA', 'ultimateShearStressMB',
                'flexuralModulusF', 'flexuralUltimateStrength', 'flexuralUltimateStrengthMA', 'flexuralUltimateStrengthMB', 'strainUltimateStrength', 'flexuralUltimateForce',
                'yieldTorque', 'maxiTorque', 'yieldAngle', 'maxiTwistedAngle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def r_and_d_edit(request, aid):
    r_and_d_object = models.R_and_D.objects.filter(id=aid).first()

    if request.method == "GET":
        form = R_and_DEditModelForm(instance=r_and_d_object)
        return render(request, 'r_and_d/r_and_d_form.html', {"form": form})

    form = R_and_DEditModelForm(instance=r_and_d_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'r_and_d/r_and_d_form.html', {"form": form})

    form.save()

    return redirect('/r_and_d/list/')


def r_and_d_delete(request):
    aid = request.GET.get("aid")
    models.R_and_D.objects.filter(id=aid).delete()

    return JsonResponse({"status": True})

def r_and_d_delete_mult(request):
    aid = request.GET.get("aid")
    if not aid:
        return JsonResponse({"status": False, "error": "ID cannot be empty"})

    try:
        r_and_d = models.R_and_D.objects.get(id=aid)
        r_and_d.delete()
        return JsonResponse({"status": True})
    except models.R_and_D.DoesNotExist:
        return JsonResponse({"status": False, "error": "R_and_D not found"})