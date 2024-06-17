from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.urls import path
from django import forms
from openpyxl import load_workbook

from web import models
from utils.encrypt import md5
import django_filters

class PartFilter(django_filters.FilterSet):
    project = django_filters.ModelChoiceFilter(queryset=models.Project.objects.all())
    partName = django_filters.CharFilter(field_name='partName', lookup_expr='icontains')
    valid = django_filters.BooleanFilter(field_name='valid')  

    class Meta:
        model = models.Part
        fields = ['project', 'partName', 'valid']
    # class Meta:
    #     model = models.Part
    #     fields = {
    #         'project': ['exact'], 
    #         'partName': ['icontains'],
    #     }
def part_list(request):
    """ list of part """

    part_filter = PartFilter(request.GET, queryset=models.Part.objects.all())
    return render(request, 'part/part_list.html', {'filter': part_filter})

def part_list_doc(request):
    """ list of part """

    part_filter = PartFilter(request.GET, queryset=models.Part.objects.all())
    return render(request, 'part/part_list_doc.html', {'filter': part_filter})

class PartFilterValid(django_filters.FilterSet):
    project = django_filters.ModelChoiceFilter(queryset=models.Project.objects.all())
    partName = django_filters.CharFilter(field_name='partName', lookup_expr='icontains')
    

    class Meta:
        model = models.Part
        fields = ['project', 'partName',]
   
def part_valid(request):
    """ list of part """

    part_filter = PartFilterValid(request.GET, queryset=models.Part.objects.filter(valid=True))
    return render(request, 'part/part_valid.html', {'filter': part_filter})

def part_valid_doc(request):
    """ list of part """

    part_filter = PartFilterValid(request.GET, queryset=models.Part.objects.filter(valid=True))
    return render(request, 'part/part_valid_doc.html', {'filter': part_filter})

def part_input(request):
    """ list of part """

    queryset = models.Part.objects.all().order_by("id")
    
    return render(request, 'part/part_input.html', {"queryset": queryset})

class PartModelForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ['project', 'partName',
                  'defaultInterfaceHeight', 'defaultInterfaceIntDiam', 'defaultLinkType', 'defaultLinkDefined', 'numberLink', 'numberBushing', 
                  'totalMassLink', 'totalMassAccumulation', 'totalMassWinding', 'totalMassBushing', 'additionalMass', 
                  'totalMassStructure', 'totalFiberLength', 'totalFiberMass', 'totalResinMass', 'projectImage','valid'
                #   'part_gh', 'part_mod', 'part_csv', 'part_rs', 'part_log', 'part_mp4', 'part_jpg'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}

class PartModelAddForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ['project', 'partName',
                  'defaultInterfaceHeight', 'defaultInterfaceIntDiam', 'defaultLinkType', 'defaultLinkDefined', 'numberLink', 'numberBushing', 
                  'totalMassLink', 'totalMassAccumulation', 'totalMassWinding', 'totalMassBushing', 'additionalMass', 
                  'totalMassStructure', 'totalFiberLength', 'totalFiberMass', 'totalResinMass', 'projectImage',
                 ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}

class PartModelImageForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ['project', 'partName',
                  'projectImage',
                 ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


class PartModelDocForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ['project', 'partName',
                  'part_gh', 'part_mod', 'part_csv', 'part_rs', 'part_log', 'part_mp4', 'part_jpg',
                 ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def part_add(request):
    if request.method == "GET":
        form = PartModelAddForm()
        return render(request, 'part/part_add.html', {"form": form})

    form = PartModelAddForm(request.POST,request.FILES)
    if not form.is_valid():

        print("Form is not valid:", form.errors)
        return render(request, 'part/part_add.html', {"form": form})


    # form.save()
    part = form.save(commit=False)
    part.user = models.User.objects.filter(id=request.info_dict['id']).first() 
    part.save()
    return redirect('/part/list/')

    # if request.method == 'POST':
    #     form = PartModelAddForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/part/list/')
    #     else:
    #         print("Form is not valid:", form.errors)
    # else:
    #     form = PartModelAddForm()
    # return render(request, 'part/part_add.html', {'form': form})

class PartEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ['project', 'partName',
                  'defaultInterfaceHeight', 'defaultInterfaceIntDiam', 'defaultLinkType', 'defaultLinkDefined', 'numberLink', 'numberBushing', 
                  'totalMassLink', 'totalMassAccumulation', 'totalMassWinding', 'totalMassBushing', 'additionalMass', 
                  'totalMassStructure', 'totalFiberLength', 'totalFiberMass', 'totalResinMass', 'projectImage','valid'
                #   'part_gh', 'part_mod', 'part_csv', 'part_rs', 'part_log', 'part_mp4', 'part_jpg'
                  ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}

class PartEditModelDocForm(forms.ModelForm):
    class Meta:
        model = models.Part
        fields = ['project', 'partName',
                  'part_gh', 'part_mod', 'part_csv', 'part_rs', 'part_log', 'part_mp4', 'part_jpg',
                 ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}

def part_edit(request, aid):
    part_object = models.Part.objects.filter(id=aid).first()

    if request.method == "GET":
        form = PartEditModelForm(instance=part_object)
        return render(request, 'part/part_form.html', {"form": form})

    form = PartEditModelForm(instance=part_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'part/part_form.html', {"form": form})

    # form.save()
    part = form.save(commit=False)
    part.user = models.User.objects.filter(id=request.info_dict['id']).first() 
    part.save()

    return redirect('/part/list/')



def part_edit_doc(request, aid):
    part_object = models.Part.objects.filter(id=aid).first()

    if request.method == "GET":
        form = PartEditModelDocForm(instance=part_object)
        return render(request, 'part/part_form.html', {"form": form})

    form = PartEditModelDocForm(instance=part_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'part/part_form.html', {"form": form})

    # form.save()
    part = form.save(commit=False)
    part.user = models.User.objects.filter(id=request.info_dict['id']).first() 
    part.save()

    return redirect('/part/list-doc/')

def part_delete(request):
    aid = request.GET.get("aid")
    # models.Part.objects.filter(id=aid).delete()
    part = models.Part.objects.filter(id=aid).first()
    if part:
        part.user = models.User.objects.filter(id=request.info_dict['id']).first()  
        part.delete()

    return JsonResponse({"status": True})

def handle_uploaded_file_part(f):
    # 加载Excel文件
    wb = load_workbook(filename=f, data_only=True)
    if 'CoverPage' not in wb.sheetnames:
        return {'error': 'CoverPage sheet not found'}
    if 'Input' not in wb.sheetnames:
        return {'error': 'Input sheet not found'}
    if 'Output' not in wb.sheetnames:
        return {'error': 'Output sheet not found'}
    
    sheetCP = wb['CoverPage']
    sheetIn = wb['Input']
    sheetOut = wb['Output']

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

    part_data = {}
    
    part_data['project_id'] = models.Project.objects.filter(projectName=project_data['projectName']).first().id
    # print(part_data['project_id'])
    part_data['partName'] = project_data['projectName']


    for row in sheetIn.iter_rows():
        for cell in row:
            if cell.value == "Interface Height [mm]":
                part_data['defaultInterfaceHeight'] = int(sheetIn.cell(row=cell.row, column=cell.column + 1).value)
            elif cell.value == "Interface Int. Diam [mm]":
                part_data['defaultInterfaceIntDiam'] = int(sheetIn.cell(row=cell.row, column=cell.column + 1).value)
            elif cell.value == "Link (Element) Type" and sheetIn.cell(row=cell.row+1, column=cell.column ).value == "Link defined by":
                part_data['defaultLinkType'] = sheetIn.cell(row=cell.row, column=cell.column+1 ).value
            elif cell.value == "Link defined by":
                part_data['defaultLinkDefined'] = sheetIn.cell(row=cell.row, column=cell.column + 1).value


    for row in sheetOut.iter_rows():
        for cell in row:
            if cell.value == "Number of links":
                part_data['numberLink'] = int(sheetOut.cell(row=cell.row, column=cell.column + 1).value)
            elif cell.value == "Number of bushings":
                part_data['numberBushing'] = int(sheetOut.cell(row=cell.row, column=cell.column + 1).value)
            elif cell.value == "Total mass of links [g]":
                part_data['totalMassLink'] = round(sheetOut.cell(row=cell.row, column=cell.column + 1).value, 2)
            elif cell.value == "Total mass of accumulation [g]":
                part_data['totalMassAccumulation'] = round(sheetOut.cell(row=cell.row, column=cell.column + 1).value, 2)
            elif cell.value == "Total mass of winding [g]":
                part_data['totalMassWinding'] = round(sheetOut.cell(row=cell.row, column=cell.column + 1).value, 2)
            elif cell.value == "Total mass of bushings [g]":
                part_data['totalMassBushing'] = round(sheetOut.cell(row=cell.row, column=cell.column + 1).value, 2)
            elif cell.value == "Additional masses [g]":
                part_data['additionalMass'] =  sheetOut.cell(row=cell.row, column=cell.column + 1).value 
            elif cell.value == "Total mass of structure [g]":
                part_data['totalMassStructure'] = round(sheetOut.cell(row=cell.row, column=cell.column + 1).value, 2)
            elif cell.value == "Total fiber length [m]":
                part_data['totalFiberLength'] = round(sheetOut.cell(row=cell.row, column=cell.column + 1).value, 2)
            elif cell.value == "Total fiber mass [kg]":
                part_data['totalFiberMass'] = round(sheetOut.cell(row=cell.row, column=cell.column + 1).value, 2)
            elif cell.value == "Total resin mass [g]":
                part_data['totalResinMass'] = round(sheetOut.cell(row=cell.row, column=cell.column + 1).value, 2)
            
            

    return part_data

def upload_file_part(request):
    if request.method == 'POST' and 'file' in request.FILES:
        part_data = handle_uploaded_file_part(request.FILES['file'])
        if 'error' in part_data:
            return JsonResponse(part_data, status=400)
        return JsonResponse(part_data)
    return JsonResponse({'error': 'Invalid request'}, status=400)
