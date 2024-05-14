# views.py
from django.shortcuts import render, redirect
from form import UserFormSet

def manage_items(request):
    if request.method == 'POST':
        formset = UserFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save()
            return redirect('items_view')  # 重定向到条目列表页或其他
    else:
        formset = UserFormSet()
    return render(request, 'add.html', {'formset': formset})
