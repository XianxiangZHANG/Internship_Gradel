from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory

from web import models
import django_filters

class R_and_DFilter(django_filters.FilterSet):
    program = django_filters.CharFilter(field_name='program', lookup_expr='icontains')
    projectNr = django_filters.CharFilter(field_name='projectNr', lookup_expr='icontains')
    ERMDS = django_filters.CharFilter(field_name='ERMDS', lookup_expr='icontains')
    fiber = django_filters.ModelChoiceFilter(queryset=models.Fiber.objects.all())
    resin = django_filters.ModelChoiceFilter(queryset=models.Resin.objects.all())
    valid = django_filters.BooleanFilter(field_name='valid')  

    class Meta:
        model = models.Resin
        fields = ['program', 'projectNr', 'ERMDS', 'fiber', 'resin', 'valid']
    # class Meta:
    #     model = models.R_and_D
    #     fields = {
    #         'program': ['icontains'], 
    #         'projectNr': ['icontains'],
    #         'ERMDS': ['icontains'],
    #         'fiber': ['exact'],
    #         'resin': ['exact'],
    #     }


class R_and_DFilterModify(django_filters.FilterSet):

    class Meta:
        model = models.R_and_D
        fields = {
            'program': ['exact'], 
            'projectNr': ['exact'],
            'ERMDS': ['exact'],
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
                'numberOfBobbins', 
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
                'yieldTorque', 'maxiTorque', 'yieldAngle', 'maxiTwistedAngle',  
                'fiberC', 'numberOfBobbinsC', 'resinC', 
                'hardenerC', 'curingCycleC', 'towC', 'texC', 'fiberDensityC', 'resinDensityC',
                'endEffectorC', 'impregnationBathC', 'entryNozzleDiamC', 'exitNozzleDiamC',
                'roomTemperatureC', 'roomhumidityC',
                'brakeForcebobinC', 'windingSpeedRangeC',
                'FVRC', 'compositeDensityC', 'porosityC', 'theoreticalSampleSectionC', 'experimentalSampleSectionC', 'agedC', 'temperatureOfTestsC',
                'numberOfSamplesC', 'configurarionC', 'sampleLengthC', 'numberOfCyclesC', 'sleeveC',
                'thermalExpansionCoefficientC', 'thermalConductivityC',
                'tensileYoungModulusC', 'tensileUltimateStressC', 'tensileUltimateStressMAC', 'tensileUltimateStressMBC',
                'tensileUltimateLoadC', 'tensileYieldStressC', 'tensileYieldStressMAC', 'tensileYieldStressMBC', 'tensileYieldLoadC',
                'compressionYoungModulusC', 'compressionUltimateStressC', 'compressionUltimateStressMAC', 'compressionUltimateStressMBC',
                'compressionUltimateLoadC', 'compressionYieldStressC', 'compressionYieldStressMAC', 'compressionYieldStressMBC', 'compressionYieldLoadC', 'poissonRatioC',
                'flexuralModulusILSSC', 'ultimateShearForceC', 'ultimateShearStressC', 'ultimateShearStressMAC', 'ultimateShearStressMBC',
                'flexuralModulusFC', 'flexuralUltimateStrengthC', 'flexuralUltimateStrengthMAC', 'flexuralUltimateStrengthMBC', 'strainUltimateStrengthC', 'flexuralUltimateForceC',
                'yieldTorqueC', 'maxiTorqueC', 'yieldAngleC', 'maxiTwistedAngleC',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


# class RDCommentModelForm(forms.ModelForm):
#     class Meta:
#         model = models.RDComment
#         fields = [
#                 'fiber', 'numberOfBobbins', 'resin', 
#                 'endEffector', 'impregnationBath', 'entryNozzleDiam', 'exitNozzleDiam',
#                 'roomTemperature', 'roomhumidity',
#                 'brakeForcebobin', 'windingSpeedRange',
#                 'FVR', 'compositeDensity', 'porosity', 'theoreticalSampleSection', 'experimentalSampleSection', 'aged', 'temperatureOfTests',
#                 'numberOfSamples', 'configurarion', 'sampleLength', 'numberOfCycles', 'sleeve',
#                 'thermalExpansionCoefficient', 'thermalConductivity',
#                 'tensileYoungModulus', 'tensileUltimateStress', 'tensileUltimateStressMA', 'tensileUltimateStressMB',
#                 'tensileUltimateLoad', 'tensileYieldStress', 'tensileYieldStressMA', 'tensileYieldStressMB', 'tensileYieldLoad',
#                 'compressionYoungModulus', 'compressionUltimateStress', 'compressionUltimateStressMA', 'compressionUltimateStressMB',
#                 'compressionUltimateLoad', 'compressionYieldStress', 'compressionYieldStressMA', 'compressionYieldStressMB', 'compressionYieldLoad', 'poissonRatio',
#                 'flexuralModulusILSS', 'ultimateShearForce', 'ultimateShearStress', 'ultimateShearStressMA', 'ultimateShearStressMB',
#                 'flexuralModulusF', 'flexuralUltimateStrength', 'flexuralUltimateStrengthMA', 'flexuralUltimateStrengthMB', 'strainUltimateStrength', 'flexuralUltimateForce',
#                 'yieldTorque', 'maxiTorque', 'yieldAngle', 'maxiTwistedAngle']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#         for name, filed_object in self.fields.items():
#             filed_object.widget.attrs = {"class": "form-control"}


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
                'yieldTorque', 'maxiTorque', 'yieldAngle', 'maxiTwistedAngle',  
                'fiberC', 'numberOfBobbinsC', 'resinC', 
                'hardenerC', 'curingCycleC', 'towC', 'texC', 'fiberDensityC', 'resinDensityC',
                'endEffectorC', 'impregnationBathC', 'entryNozzleDiamC', 'exitNozzleDiamC',
                'roomTemperatureC', 'roomhumidityC',
                'brakeForcebobinC', 'windingSpeedRangeC',
                'FVRC', 'compositeDensityC', 'porosityC', 'theoreticalSampleSectionC', 'experimentalSampleSectionC', 'agedC', 'temperatureOfTestsC',
                'numberOfSamplesC', 'configurarionC', 'sampleLengthC', 'numberOfCyclesC', 'sleeveC',
                'thermalExpansionCoefficientC', 'thermalConductivityC',
                'tensileYoungModulusC', 'tensileUltimateStressC', 'tensileUltimateStressMAC', 'tensileUltimateStressMBC',
                'tensileUltimateLoadC', 'tensileYieldStressC', 'tensileYieldStressMAC', 'tensileYieldStressMBC', 'tensileYieldLoadC',
                'compressionYoungModulusC', 'compressionUltimateStressC', 'compressionUltimateStressMAC', 'compressionUltimateStressMBC',
                'compressionUltimateLoadC', 'compressionYieldStressC', 'compressionYieldStressMAC', 'compressionYieldStressMBC', 'compressionYieldLoadC', 'poissonRatioC',
                'flexuralModulusILSSC', 'ultimateShearForceC', 'ultimateShearStressC', 'ultimateShearStressMAC', 'ultimateShearStressMBC',
                'flexuralModulusFC', 'flexuralUltimateStrengthC', 'flexuralUltimateStrengthMAC', 'flexuralUltimateStrengthMBC', 'strainUltimateStrengthC', 'flexuralUltimateForceC',
                'yieldTorqueC', 'maxiTorqueC', 'yieldAngleC', 'maxiTwistedAngleC',]
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


R_and_DFormSet = modelformset_factory(
    models.R_and_D,
    form=R_and_DModelForm,
    extra=1  # The number of additional forms added during initialization
)
# RDCommentFormSet = modelformset_factory(
#     models.RDComment,
#     form=RDCommentModelForm,
#     extra=1  # The number of additional forms added during initialization
# )

R_and_DMultFormSet = modelformset_factory(
    models.R_and_D,
    form=R_and_DForm,
    extra=1  # The number of additional forms added during initialization
)
class FiberResinForm(forms.Form):
    fiber = forms.ModelChoiceField(queryset=models.Fiber.objects.all(), required=True)
    resin = forms.ModelChoiceField(queryset=models.Resin.objects.all(), required=True)

def r_and_d_add_multiple(request):
    fibers = models.Fiber.objects.all()
    resins = models.Resin.objects.all()
    # print(fibers)
    formset = R_and_DFormSet(queryset=models.R_and_D.objects.none())
    fiber_resin_form = FiberResinForm()
   
    if request.method == 'POST':
        formset = R_and_DFormSet(request.POST)
        fiber_resin_form = FiberResinForm(request.POST)
       
        if formset.is_valid() and fiber_resin_form.is_valid():
            print("valid")
            instances = formset.save(commit=False)
            fiber = fiber_resin_form.cleaned_data['fiber']
            print(fiber)
            resin = fiber_resin_form.cleaned_data['resin']
            for instance in instances:
                instance.fiber = fiber
                instance.resin = resin
                instance.save()
          
            return redirect('/r_and_d/list/')  # Replace with your redirect URL
        else:
            # Handle formset or project_part_form validation errors here
            print(formset.errors)
            print(fiber_resin_form.errors)

    return render(request, 'r_and_d/r_and_d_add_multiple.html', {
        'fibers':fibers,
        'resins': resins,
        'fiber_resin_from': fiber_resin_form,
        'formset': formset,
    })


def r_and_d_modify_multiple(request):
   
    fibers = models.Fiber.objects.all()
    resins = models.Resin.objects.all()

    # Get filtered data
    r_and_d_filter = R_and_DFilterModify(request.GET, queryset=models.R_and_D.objects.all())
    
    # Define form set
    R_and_DMultFormSet = modelformset_factory(models.R_and_D, form=R_and_DModelForm, extra=0)
    
    if request.method == 'POST':
        print("try")
        formset = R_and_DMultFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                # Get fiber and resin from POST data
                fiber_id = request.POST.get(f'fiber_{instance.id}')
                resin_id = request.POST.get(f'resin_{instance.id}')
                if fiber_id:
                    instance.fiber_id = fiber_id
                if resin_id:
                    instance.resin_id = resin_id
                instance.save()
            return redirect('/r_and_d/list/')
        else:
            print(formset.errors)  # Print formset errors for debugging
        # print("try2")
        # fiber_resin_form = FiberResinForm(request.POST)
        # if formset.is_valid() and fiber_resin_form.is_valid():
        #     print("try3")
            
        #     fiber = fiber_resin_form.cleaned_data['fiber']
        #     resin = fiber_resin_form.cleaned_data['resin']
        #     instances = formset.save(commit=False)
        #     for instance in instances:
        #         instance.fiber = fiber
        #         instance.resin = resin
        #         instance.save()
        #     return redirect('/r_and_d/list/')
    else:
        print("try else")
        formset = R_and_DMultFormSet(queryset=r_and_d_filter.qs)
        # fiber_resin_form = FiberResinForm()

    return render(request, 'r_and_d/r_and_d_modify_multiple.html', {
        'filter': r_and_d_filter,
        'formset': formset,
        # 'fiber_resin_from': fiber_resin_form,
        'fibers':fibers,
        'resins': resins,
    })


def r_and_d_add(request):
    if request.method == "GET":
        form = R_and_DModelForm()
        return render(request, 'r_and_d/r_and_d_add.html', {"form": form})

    form = R_and_DModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'r_and_d/r_and_d_add.html', {"form": form})

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
                'yieldTorque', 'maxiTorque', 'yieldAngle', 'maxiTwistedAngle',  
                'fiberC', 'numberOfBobbinsC', 'resinC', 
                'hardenerC', 'curingCycleC', 'towC', 'texC', 'fiberDensityC', 'resinDensityC',
                'endEffectorC', 'impregnationBathC', 'entryNozzleDiamC', 'exitNozzleDiamC',
                'roomTemperatureC', 'roomhumidityC',
                'brakeForcebobinC', 'windingSpeedRangeC',
                'FVRC', 'compositeDensityC', 'porosityC', 'theoreticalSampleSectionC', 'experimentalSampleSectionC', 'agedC', 'temperatureOfTestsC',
                'numberOfSamplesC', 'configurarionC', 'sampleLengthC', 'numberOfCyclesC', 'sleeveC',
                'thermalExpansionCoefficientC', 'thermalConductivityC',
                'tensileYoungModulusC', 'tensileUltimateStressC', 'tensileUltimateStressMAC', 'tensileUltimateStressMBC',
                'tensileUltimateLoadC', 'tensileYieldStressC', 'tensileYieldStressMAC', 'tensileYieldStressMBC', 'tensileYieldLoadC',
                'compressionYoungModulusC', 'compressionUltimateStressC', 'compressionUltimateStressMAC', 'compressionUltimateStressMBC',
                'compressionUltimateLoadC', 'compressionYieldStressC', 'compressionYieldStressMAC', 'compressionYieldStressMBC', 'compressionYieldLoadC', 'poissonRatioC',
                'flexuralModulusILSSC', 'ultimateShearForceC', 'ultimateShearStressC', 'ultimateShearStressMAC', 'ultimateShearStressMBC',
                'flexuralModulusFC', 'flexuralUltimateStrengthC', 'flexuralUltimateStrengthMAC', 'flexuralUltimateStrengthMBC', 'strainUltimateStrengthC', 'flexuralUltimateForceC',
                'yieldTorqueC', 'maxiTorqueC', 'yieldAngleC', 'maxiTwistedAngleC', 'valid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def r_and_d_edit(request, aid):
    fibers = models.Fiber.objects.all()
    resins = models.Resin.objects.all()
    fiber_resin_form = FiberResinForm()

    r_and_d_object = models.R_and_D.objects.filter(id=aid).first()

    if request.method == "GET":
        form = R_and_DEditModelForm(instance=r_and_d_object)
        return render(request, 'r_and_d/r_and_d_form.html', {
            "form": form,
            'fibers':fibers,
            'resins': resins,
            'fiber_resin_from': fiber_resin_form,
            })

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