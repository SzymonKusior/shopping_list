from django.urls import path
from .views import itemList, addItem, deleteItem, completeItem, editDescription, redirectHome, clearAll
urlpatterns = [
    path('', itemList, name='shoppingList'),
    path('item_detail/<int:pk>/', itemList, name='itemDetail'),
    path('item_detail/', redirectHome, {'pk': None}, name='itemDetail'),
    path('add_item/', addItem, name='itemAdd'),
    path('delete_item/<int:pk>/', deleteItem, name='itemDelete'),
    path('complete_item/<int:pk>/', completeItem, name='itemComplete'),
    path('edit_description/<int:pk>/', editDescription, name='descriptionEdit'),
    path('clear_all/', clearAll, name="clearAllItems")

]