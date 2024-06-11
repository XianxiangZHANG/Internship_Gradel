from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory
from openpyxl import load_workbook

from web import models
from utils.encrypt import md5
import django_filters

class InterfaceFilter(django_filters.FilterSet):
    class Meta:
        model = models.Interface
        fields = {
            'project': ['exact'], 
            'part': ['exact'],
            'interfaceName': ['icontains'],
        }

def interface_list(request):
    """ list of interface """

    interface_filter = InterfaceFilter(request.GET, queryset=models.Interface.objects.all())
    return render(request, 'interface/interface_list.html', {'filter': interface_filter})

def interface_valid(request):
    """ list of interface """
    interface_filter = InterfaceFilter(request.GET, queryset=models.Interface.objects.filter(part__valid=True))
    return render(request, 'interface/interface_valid.html', {'filter': interface_filter})

def interface_input(request):
    """ list of interface """

    # [obj,]
    queryset = models.Interface.objects.all().order_by("id")
  
    return render(request, 'interface/interface_input.html', {"queryset": queryset})

   
class InterfaceModelForm(forms.ModelForm):
    class Meta:
        model = models.Interface
        fields = ['interfaceName', 'height', 'intDiameter', 'totalLink', 'totalArm', 'totalSection',
                'extDiameter', 'accMass', 'finODiam', 'finAccSection', 'safetyFactor',
                'interfaceCenterX', 'interfaceCenterY', 'interfaceCenterZ',
                'directionVectorX', 'directionVectorY', 'directionVectorZ',
                'divisionStep',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


class ProjectPartForm(forms.Form):
    project = forms.ModelChoiceField(queryset=models.Project.objects.all(), required=True)
    part = forms.ModelChoiceField(queryset=models.Part.objects.all(), required=True)
    

InterfaceFormSet = modelformset_factory(
    models.Interface,
    form=InterfaceModelForm,
    extra=1  
)

def interface_add_multiple(request):
    projects = models.Project.objects.all()
    formset = InterfaceFormSet(queryset=models.Interface.objects.none())
    project_part_form = ProjectPartForm()
    # interfaceError = None

    if request.method == 'POST':
        formset = InterfaceFormSet(request.POST)
        project_part_form = ProjectPartForm(request.POST)

        if formset.is_valid() and project_part_form.is_valid(): 
            instances = formset.save(commit=False)
            project = project_part_form.cleaned_data['project']
            part = project_part_form.cleaned_data['part']
            for instance in instances:
                instance.project = project
                instance.part = part
                instance.save()
            return redirect('/interface/list/')  # Replace with your redirect URL
        else:
            # Handle formset or project_part_form validation errors here
            print(formset.errors)
            print(project_part_form.errors)

    return render(request, 'interface/interface_add_multiple.html', {
        'projects': projects,
        'formset': formset,
        'project_part_form': project_part_form,
        # 'interfaceError': interfaceError,
    })



def interface_add(request):
    if request.method == "GET":
        form = InterfaceModelForm()
        return render(request, 'interface/interface_form.html', {"form": form})

    form = InterfaceModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'interface/interface_form.html', {"form": form})


    # save -> DB
    form.save()
    return redirect('/interface/list/')

def interface_modify_multiple(request):
    # Get filtered data
    interface_filter = InterfaceFilter(request.GET, queryset=models.Interface.objects.all())
    
    # Define form set
    InterfaceFormSet = modelformset_factory(models.Interface, form=InterfaceModelForm, extra=0)
    
    if request.method == 'POST':
        formset = InterfaceFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('/interface/list/')
    else:
        formset = InterfaceFormSet(queryset=interface_filter.qs)

    return render(request, 'interface/interface_modify_multiple.html', {
        'filter': interface_filter,
        'formset': formset,
    })

class InterfaceEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Interface
        fields = ['project', 'part', 'interfaceName', 'height', 'intDiameter', 'totalLink', 'totalArm', 'totalSection',
                'extDiameter', 'accMass', 'finODiam', 'finAccSection', 'safetyFactor',
                'interfaceCenterX', 'interfaceCenterY', 'interfaceCenterZ',
                'directionVectorX', 'directionVectorY', 'directionVectorZ',
                'divisionStep',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['part'].queryset = models.Part.objects.all()
        self.fields['project'].queryset = models.Project.objects.all()
        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def interface_edit(request, aid):
    interface_object = models.Interface.objects.filter(id=aid).first()

    if request.method == "GET":
        form = InterfaceEditModelForm(instance=interface_object)
        return render(request, 'interface/interface_form.html', {"form": form})

    form = InterfaceEditModelForm(instance=interface_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'interface/interface_form.html', {"form": form})

    form.save()

    return redirect('/interface/list/')


def interface_delete(request):
    aid = request.GET.get("aid")
    models.Interface.objects.filter(id=aid).delete()

    return JsonResponse({"status": True})

def handle_uploaded_file_interface(f):
    # 加载Excel文件
    wb = load_workbook(filename=f, data_only=True)
    if 'CoverPage' not in wb.sheetnames:
        return {'error': 'CoverPage sheet not found'}
    if 'Input' not in wb.sheetnames:
        return {'error': 'Input sheet not found'}
    if 'Output' not in wb.sheetnames:
        return {'error': 'Output sheet not found'}
    if 'Bushing Table' not in wb.sheetnames:
        return {'error': 'Bushing Table sheet not found'}
    
    sheetCP = wb['CoverPage']
    sheetIn = wb['Input']
    sheetOut = wb['Output']
    sheetBT = wb['Bushing Table']

    # 获取项目数据
    interface_data = {}
    interfaceName = {}
    height = {}
    intDiameter = {}
    totalLink = {}
    totalArm = {}
    totalSection = {}
    extDiameter = {}
    accMass = {}
    finODiam = {}
    finAccSection = {}

    safetyFactor = {}

    interfaceCenterX = {}
    interfaceCenterY = {}
    interfaceCenterZ = {}
    # directionVectorX = {}
    # directionVectorY = {}
    # directionVectorZ = {}

    # divisionStep = {}
    
    project_data = {}
    for row in sheetCP.iter_rows():
        for cell in row:
            if cell.value == "Program : ":
                project_data['program'] = sheetCP.cell(row=cell.row, column=cell.column + 2).value
            elif cell.value == "Customer : ":
                project_data['customer'] = sheetCP.cell(row=cell.row, column=cell.column + 2).value
            elif cell.value == "Project No:":
                project_data['projectNo'] = sheetCP.cell(row=cell.row, column=cell.column + 2).value
    project_data['projectName'] = project_data['projectNo'] +' - '+ project_data['customer'] +' - '+ project_data['program']

    
    interface_data['project_id'] = models.Project.objects.filter(projectName=project_data['projectName']).first().id


    # for row in sheetCP.iter_rows():
    #     for cell in row:
    #         if cell.value == "Program : ":
    #             # interface_data['project_projectName'] = sheetCP.cell(row=cell.row, column=cell.column + 2).value
    #             interface_data['project_id'] = models.Project.objects.filter(projectName=sheetCP.cell(row=cell.row, column=cell.column + 2).value).first().id
               

    for row in sheetOut.iter_rows():
        for cell in row:
            if cell.value == "Number of bushings":
                numberBushing = int(sheetOut.cell(row=cell.row, column=cell.column + 1).value)
                # print(type(numberBushing))
    
    numberInterface = 0
    for row in sheetIn.iter_rows():
        for cell in row:
            if cell.value == "# of int.":
                for i in range(0, numberBushing):
                    numberInterface += int(sheetIn.cell(row=cell.row+1+i, column=cell.column ).value)
                    # print(numberInterface)

    for row in sheetBT.iter_rows():
        for cell in row:
            if cell.value == "Interface" and cell.row > 3:
                for i in range(0, numberInterface):
                    # print(cell.row, cell.column)
                    interfaceName[i] = sheetBT.cell(row=cell.row, column=cell.column + 1 + i ).value
                    print(interfaceName[i])
            elif cell.value == "Height [mm]":
                for i in range(0, numberInterface):
                    height[i] = int(sheetBT.cell(row=cell.row, column=cell.column+1+i ).value)
                    # print(height[i])
            elif cell.value == "Int. Diameter [mm]":
                for i in range(0, numberInterface):
                    intDiameter[i] = int(sheetBT.cell(row=cell.row, column=cell.column+1+i ).value)
                    # print(intDiameter[i])
            elif cell.value == "Total Link":
                for i in range(0, numberInterface):
                    totalLink[i] = int(sheetBT.cell(row=cell.row, column=cell.column+1+i ).value)
                    # print(totalLink[i])
            elif cell.value == "Total Arm":
                for i in range(0, numberInterface):
                    totalArm[i] = int(sheetBT.cell(row=cell.row, column=cell.column+1+i ).value)
                    # print(totalArm[i])
            elif cell.value == "Total Section [mm²]":
                for i in range(0, numberInterface):
                    totalSection[i] = round(sheetBT.cell(row=cell.row, column=cell.column+1+i ).value, 2)
                    # print(totalSection[i])
            elif cell.value == "Ext. Diameter [mm]":
                for i in range(0, numberInterface):
                    extDiameter[i] = round(sheetBT.cell(row=cell.row, column=cell.column+1+i ).value, 2)
                    # print(extDiameter[i])
            elif cell.value == "Acc. Mass [g]":
                for i in range(0, numberInterface):
                    accMass[i] = round(sheetBT.cell(row=cell.row, column=cell.column+1+i ).value, 2)
                    # print(accMass[i])
            elif cell.value == "Fin. O. Diam. [mm]":
                for i in range(0, numberInterface):
                    finODiam[i] = sheetBT.cell(row=cell.row, column=cell.column+1+i ).value
                    # print(finODiam[i])
            elif cell.value == "Fin. Acc. section [mm²]":
                for i in range(0, numberInterface):
                    finAccSection[i] = sheetBT.cell(row=cell.row, column=cell.column+1+i ).value
                    # print(finAccSection[i])
            elif cell.value == "Safety Factor [%]":
                for i in range(0, numberInterface):
                    safetyFactor[i] = int(sheetBT.cell(row=cell.row, column=cell.column+1+i ).value * 100)
                    # print(safetyFactor[i])
            elif cell.value == "X":
                for i in range(0, numberInterface):
                    interfaceCenterX[i] = sheetBT.cell(row=cell.row+1+i, column=cell.column ).value
                    # print(interfaceCenterX[i])
            elif cell.value == "Y":
                for i in range(0, numberInterface):
                    interfaceCenterY[i] = sheetBT.cell(row=cell.row+1+i, column=cell.column ).value
                    # print(interfaceCenterY[i])
            elif cell.value == "Z":
                for i in range(0, numberInterface):
                    interfaceCenterZ[i] = sheetBT.cell(row=cell.row+1+i, column=cell.column ).value
                    # print(interfaceCenterZ[i])
            # elif cell.value == "":
            #     for i in range(0, numberInterface):
            #         directionVectorX[i] = sheetBT.cell(row=cell.row+1+i, column=cell.column ).value
            #         # print(directionVectorX[i])
            # elif cell.value == "":
            #     for i in range(0, numberInterface):
            #         directionVectorY[i] = sheetBT.cell(row=cell.row+1+i, column=cell.column ).value
            #         # print(directionVectorY[i])
            # elif cell.value == "":
            #     for i in range(0, numberInterface):
            #         directionVectorZ[i] = sheetBT.cell(row=cell.row+1+i, column=cell.column ).value
            #         # print(directionVectorZ[i])
    
    interface =  {
        'numberInterface':numberInterface,
        'interface_data':interface_data,
        'interfaceName':interfaceName,
        'height':height,
        'intDiameter':intDiameter,
        'totalLink':totalLink,
        'totalArm':totalArm,
        'totalSection':totalSection,
        'extDiameter':extDiameter,
        'accMass':accMass,
        'finODiam':finODiam,
        'finAccSection':finAccSection,
        'safetyFactor':safetyFactor,
        'interfaceCenterX':interfaceCenterX,
        'interfaceCenterY':interfaceCenterY,
        'interfaceCenterZ':interfaceCenterZ,
    }
    return interface

def upload_file_interface(request):
    if request.method == 'POST' and 'file' in request.FILES:
        interface = handle_uploaded_file_interface(request.FILES['file'])
        print(interface)
        if 'error' in interface:
            return JsonResponse(interface, status=400)
        return JsonResponse(interface)
    return JsonResponse({'error': 'Invalid request'}, status=400)
