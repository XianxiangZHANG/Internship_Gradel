import warnings
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django import forms
from django.forms import modelformset_factory
from openpyxl import load_workbook

from web import models
from utils.encrypt import md5
import django_filters

class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = models.Link
        fields = {
            'project': ['exact'], 
            'part': ['exact'],
            'linkName': ['icontains'],
        }

def link_list(request):
    """ list of link """

    link_filter = LinkFilter(request.GET, queryset=models.Link.objects.all())
    return render(request, 'link/link_list.html', {'filter': link_filter})

def link_valid(request):
    """ list of link """

    link_filter = LinkFilter(request.GET, queryset=models.Link.objects.filter(part__valid=True))
    return render(request, 'link/link_valid.html', {'filter': link_filter})

def link_input(request):
    """ list of link """

    # [obj,]
    queryset = models.Link.objects.all().order_by("id")
  
    return render(request, 'link/link_input.html', {"queryset": queryset})

   
class LinkModelForm(forms.ModelForm):
    class Meta:
        model = models.Link
        fields = ['linkName', 'interface1', 'interface2', 'length',  'sequence', 'armDiam', 'armSection', 
                  'cycle', 'finArmSection', 'finArmDiam', 'finArmRadius',
                'mass', 'angle']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field_object in self.fields.items():
            field_object.widget.attrs = {"class": "form-control"}


class ProjectPartForm(forms.Form):
    project = forms.ModelChoiceField(queryset=models.Project.objects.all(), required=True)
    part = forms.ModelChoiceField(queryset=models.Part.objects.all(), required=True)
    

LinkFormSet = modelformset_factory(
    models.Link,
    form=LinkModelForm,
    extra=1 
)

def link_add_multiple(request):
    projects = models.Project.objects.all()
    formset = LinkFormSet(queryset=models.Link.objects.none())
    project_part_form = ProjectPartForm()
   

    if request.method == 'POST':
        formset = LinkFormSet(request.POST)
        project_part_form = ProjectPartForm(request.POST)

        if formset.is_valid() and project_part_form.is_valid(): 
            instances = formset.save(commit=False)
            project = project_part_form.cleaned_data['project']
            part = project_part_form.cleaned_data['part']
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.project = project
                instance.part = part
                instance.save()
            return redirect('/link/list/')  # Replace with your redirect URL
        else:
            # Handle formset or project_part_form validation errors here
            print(formset.errors)
            print(project_part_form.errors)

    return render(request, 'link/link_add_multiple.html', {
        'projects': projects,
        'formset': formset,
        'project_part_form': project_part_form,
        'linkError': "Link name is Required",
    })

def link_modify_multiple(request):
    # Get filtered data
    link_filter = LinkFilter(request.GET, queryset=models.Link.objects.all())
    
    # Define form set
    LinkFormSet = modelformset_factory(models.Link, form=LinkModelForm, extra=0)
    
    if request.method == 'POST':
        formset = LinkFormSet(request.POST)
        if formset.is_valid():
            # formset.save()
            instances = formset.save(commit=False)
            
            for instance in instances:
                instance.user = models.User.objects.filter(id=request.info_dict['id']).first()  
                instance.save()
            return redirect('/link/list/')
    else:
        formset = LinkFormSet(queryset=link_filter.qs)

    return render(request, 'link/link_modify_multiple.html', {
        'filter': link_filter,
        'formset': formset,
        'linkError': "Link name is Required",
    })

def link_add(request):
    if request.method == "GET":
        form = LinkModelForm()
        return render(request, 'link/link_form.html', {"form": form})

    form = LinkModelForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'link/link_form.html', {"form": form})


    # form.save()
    link = form.save(commit=False)
    link.user = models.User.objects.filter(id=request.info_dict['id']).first()  
    link.save()
    return redirect('/link/list/')


class LinkEditModelForm(forms.ModelForm):
    class Meta:
        model = models.Link
        fields = ['project', 'part', 'linkName', 'interface1', 'interface2', 'length', 'sequence', 'armDiam', 'armSection', 
                  'cycle',  'finArmSection', 'finArmDiam', 'finArmRadius',
                'mass', 'angle',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['part'].queryset = models.Part.objects.all()
        self.fields['project'].queryset = models.Project.objects.all()
        for name, filed_object in self.fields.items():
            filed_object.widget.attrs = {"class": "form-control"}


def link_edit(request, aid):
    link_object = models.Link.objects.filter(id=aid).first()

    if request.method == "GET":
        form = LinkEditModelForm(instance=link_object)
        return render(request, 'link/link_form.html', {"form": form})

    form = LinkEditModelForm(instance=link_object, data=request.POST)
    if not form.is_valid():
        return render(request, 'link/link_form.html', {"form": form})

    # form.save()
    link = form.save(commit=False)
    link.user = models.User.objects.filter(id=request.info_dict['id']).first()  
    link.save()

    return redirect('/link/list/')


def link_delete(request):
    aid = request.GET.get("aid")
    # models.Link.objects.filter(id=aid).delete()
    link = models.Link.objects.filter(id=aid).first()
    if link:
        link.user = models.User.objects.filter(id=request.info_dict['id']).first()  
        link.delete()
    
    return JsonResponse({"status": True})

def link_delete_mult(request):
    aid = request.GET.get("aid")
    if not aid:
        return JsonResponse({"status": False, "error": "ID cannot be empty"})

    try:
        link = models.Fiber.objects.get(id=aid)
        # link.delete()
        if link:
            link.user = models.User.objects.filter(id=request.info_dict['id']).first()  
            link.delete()

        return JsonResponse({"status": True})
    except models.Fiber.DoesNotExist:
        return JsonResponse({"status": False, "error": "Fiber not found"})

def custom_warning_filter(message, category, filename, lineno, file=None, line=None):
    if "Unknown extension is not supported and will be removed" in str(message) or \
       "Conditional Formatting extension is not supported and will be removed" in str(message):
        return
    else:
        warnings.showwarning(message, category, filename, lineno, file, line)

# Apply custom warning filter
warnings.showwarning = custom_warning_filter


def handle_uploaded_file_link(f):
    # load Excel document
    wb = load_workbook(filename=f, data_only=True)
    if 'CoverPage' not in wb.sheetnames:
        return {'error': 'CoverPage sheet not found'}
    if 'Link Table' not in wb.sheetnames:
        return {'error': 'Link Table sheet not found'}
    
    sheetCP = wb['CoverPage']
    sheetLT = wb['Link Table']

    numberLink = 0

    link_data = {}
    linkName = {}
    interface1 = {}
    interface2 = {}

    lengthLink = {}
    # linkType = {}
    armDiam = {}
    armSection = {}

    cycle = {}
    sequence = {}
    finArmSection = {}
    finArmDiam = {}
    finArmRadius = {}
    mass = {}
    angle = {}
    
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

    
    link_data['project_id'] = models.Project.objects.filter(projectName=project_data['projectName']).first().id


    # for row in sheetCP.iter_rows():
    #     for cell in row:
    #         if cell.value == "Program : ":
    #             # link_data['project_projectName'] = sheetCP.cell(row=cell.row, column=cell.column + 2).value
    #             link_data['project_id'] = models.Project.objects.filter(projectName=sheetCP.cell(row=cell.row, column=cell.column + 2).value).first().id
               
    for row in sheetLT.iter_rows():
        for cell in row:
            if cell.value == "Link":
                i = 1
                while sheetLT.cell(row=cell.row+i, column=cell.column ).value != None:
                    numberLink += 1
                    # print(numberLink)
                    i +=1
                # print(numberLink)

        for cell in row:
            if cell.value == "Link":
                for i in range(0, numberLink):
                    # print(cell.row, cell.column)
                    linkName[i] = sheetLT.cell(row=cell.row+ 1 + i, column=cell.column ).value
                    # print(str(i) + linkName[i])
            elif cell.value == "Bushing Bi":
                for i in range(0, numberLink):
                    interface1[i] = sheetLT.cell(row=cell.row+ 1 + i, column=cell.column).value
                    # print(interface1[i])
            elif cell.value == "Bushing Bj":
                for i in range(0, numberLink):
                    interface2[i] = sheetLT.cell(row=cell.row+ 1 + i, column=cell.column ).value
                    # print(interface2[i])
            elif cell.value == "Sequence":
                for i in range(0, numberLink):
                    sequence[i] = sheetLT.cell(row=cell.row+ 1 + i, column=cell.column).value
                    # print(sequence[i])
            elif cell.value == "Length [mm]":
                for i in range(0, numberLink):
                    lengthLink[i] = round(sheetLT.cell(row=cell.row+ 1 + i, column=cell.column ).value,2)
                    # print(lengthLink[i])
            elif cell.value == "Arm diam. [mm]":
                for i in range(0, numberLink):
                    armDiam[i] = sheetLT.cell(row=cell.row+ 1 + i, column=cell.column ).value
                    # print(armDiam[i])
            elif cell.value == "Arm Sec. [mm²]":
                for i in range(0, numberLink):
                    armSection[i] = sheetLT.cell(row=cell.row+ 1 + i, column=cell.column ).value
                    # print(armSection[i])
            elif cell.value == "Cycle #":
                for i in range(0, numberLink):
                    cycle[i] = sheetLT.cell(row=cell.row+ 1 + i, column=cell.column ).value
                    # print(cycle[i])
            elif cell.value == "Fin. Arm Sec. [mm²]":
                for i in range(0, numberLink):
                    finArmSection[i] = round(sheetLT.cell(row=cell.row+ 1 + i, column=cell.column ).value,2)
                    # print(finArmSection[i])
            elif cell.value == "Fin. Arm diam. [mm]":
                for i in range(0, numberLink):
                    finArmDiam[i] = round(sheetLT.cell(row=cell.row+ 1 + i, column=cell.column ).value,2)
                    # print(finArmDiam[i])
            elif cell.value == "Fin. Arm radius [m]":
                for i in range(0, numberLink):
                    finArmRadius[i] = sheetLT.cell(row=cell.row+ 1 + i, column=cell.column ).value 
                    # print(finArmRadius[i])
            elif cell.value == "Mass [g]":
                for i in range(0, numberLink):
                    mass[i] = round(sheetLT.cell(row=cell.row+1 + i, column=cell.column ).value,2)
                    # print(mass[i])
            # elif cell.value == "Angle":
            #     for i in range(0, numberLink):
            #         angle[i] = sheetLT.cell(row=cell.row+1+i, column=cell.column ).value
            #         # print(angle[i])

    link =  {
        'numberLink':numberLink,
        'link_data':link_data,
        'linkName':linkName,
        'interface1':interface1,
        'interface2':interface2,
        'lengthLink' :lengthLink,
        'armDiam':armDiam,
        'armSection':armSection,
        'cycle':cycle,
        'sequence':sequence,
        'finArmSection':finArmSection,
        'finArmDiam':finArmDiam,
        'finArmRadius':finArmRadius,
        'mass':mass,
        'angle':angle,
    }
    return link

def upload_file_link(request):
    if request.method == 'POST' and 'file' in request.FILES:
        link = handle_uploaded_file_link(request.FILES['file'])
        # print(link)
        if 'error' in link:
            return JsonResponse(link, status=400)
        return JsonResponse(link)
    return JsonResponse({'error': 'Invalid request'}, status=400)
