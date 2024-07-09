from django.shortcuts import render, redirect
from .models import Item

def itemList(request, pk=None):
    context = getContext(pk)
    return render(request, 'app/shopping_list.html', context )

def redirectHome(request, pk):
    return redirect('shoppingList')

def getContext(pk):
    shopping_list = Item.objects.filter()
    item = Item.objects.get(id=pk) if pk else None
    context = {
        'shopping_list': shopping_list,
        'selected_item': item
    }
    return context

def addItem(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        current_pk = request.POST.get('current_pk')
        if name:
            Item.objects.create(name=name.capitalize())
        return redirect('itemDetail', pk=current_pk)

def deleteItem(request, pk):
    if request.method == 'POST':
        Item.objects.filter(id=pk).delete()
        current_pk = request.POST.get('current_pk')
        return redirect('itemDetail', pk=current_pk)

def completeItem(request, pk):
    if request.method == 'POST':
        item = Item.objects.get(id=pk)
        current_pk = request.POST.get('current_pk')
        if item.complete == False:
            item.complete= True            
        else: 
            item.complete= False
        item.save()
        return redirect('itemDetail', pk=current_pk)


def editDescription(request, pk):
    if request.method == 'POST':
        desc = request.POST.get('description')
        item = Item.objects.get(id=pk)
        item.description = desc
        item.save()
    return redirect('itemDetail', pk=pk)

def clearAll(request):
    if request.method == 'POST':
        Item.objects.all().delete()
        return redirect('shoppingList')