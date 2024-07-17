from django.shortcuts import render, redirect
from .models import Item
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class SessionItem:
    def __init__(self, id, name, description=None, complete=False, created=None):
        self.id = id
        self.name = name
        self.description = description
        self.complete = complete
        if created:
            self.created = created
        else:
            self.created = datetime.now()
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'complete': self.complete,
            'created': self.created.isoformat()
        }

def getUniqueId():
    return uuid.uuid4().int

def itemList(request, pk=None):
    context = getContext(request, pk)
    return render(request, 'app/shopping_list.html', context )

def getContext(request, pk): 
    user = request.user
    item = None
    if user.is_authenticated:
        shopping_list = Item.objects.filter(user=user)
        if pk:
            item = Item.objects.get(id=pk)
    else:
        if 'shopping_list' not in request.session:
            request.session['shopping_list'] = []
        items_list = request.session.get('shopping_list')
        shopping_list = [item for item in items_list]
        if pk:
            for items in request.session['shopping_list']:
                if items['id'] == pk:
                    item = items
    context = {
        'shopping_list': shopping_list,
        'selected_item': item
    }
    return context

def redirectHome(request, pk):
    return redirect('shoppingList')

def addItem(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        current_pk = request.POST.get('current_pk')
        user = request.user
        if name:
            if user.is_authenticated:
                Item.objects.create(name=name.capitalize(),user=user)
            else:
                items_list = request.session.get('shopping_list')
                new_id = getUniqueId()
                item = SessionItem(new_id, name.capitalize())
                items_list.append(item.to_dict())
                request.session['shopping_list'] = sorted(items_list, key = lambda d: (d['complete'], d['created']))


        return redirect('itemDetail', pk=current_pk)

def deleteItem(request, pk):
    if request.method == 'POST':
        if request.user.is_authenticated:
            Item.objects.filter(id=pk).delete()
        else:
            item_list = request.session.get('shopping_list', [])
            new_item_list = [item for item in item_list if item['id'] != pk]
            request.session['shopping_list'] = new_item_list
        current_pk = request.POST.get('current_pk')
        return redirect('itemDetail', pk=current_pk)

def completeItem(request, pk):
    if request.method == 'POST':
        current_pk = request.POST.get('current_pk')
        if request.user.is_authenticated:
            item = Item.objects.get(id=pk)
            if item.complete == False:
                item.complete= True            
            else: 
                item.complete= False
            item.save()
        else:
            item_list = request.session['shopping_list']
            for item in item_list:
                if item['id'] == pk:
                    if item.get('complete'):
                        item['complete'] = False
                    else:
                        item['complete'] = True
            request.session['shopping_list'] = sorted(item_list, key = lambda d: (d['complete'], d['created']))
    return redirect('itemDetail', pk=current_pk)

def editDescription(request, pk):
    if request.method == 'POST':
        desc = request.POST.get('description')
        if request.user.is_authenticated:
            item = Item.objects.get(id=pk)
            item.description = desc
            item.save()
        else:
            item_list = request.session['shopping_list']
            for item in item_list:
                if item['id'] == pk:
                    print(item)
                    item['description'] = desc
                    print(item)
            request.session['shopping_list'] = item_list
    return redirect('itemDetail', pk=pk)

def clearAll(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            Item.objects.all().delete()
        else:
            request.session['shopping_list'] = []
    return redirect('shoppingList')

def loginPage(request):
    form = LoginForm()
    context = {"loginForm": form}        
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("shoppingList")
    return render(request, 'app/login_page.html', context)

def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        current_pk = request.POST.get('current_pk')
        return redirect('itemDetail', pk=current_pk)

def registerPage(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password1')
            User.objects.create_user(username, email=None, password=password)
    else:   
        form = RegisterForm()
    context = {"registerForm": form}
    return render(request, 'app/register_page.html', context)
