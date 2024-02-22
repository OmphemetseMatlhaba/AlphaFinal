from django.conf import settings
from item.models import Item

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart: 
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
        
    def __iter__(self):
        for p in self.cart.keys():
           self.cart[str(p)]['item'] = Item.objects.get(pk=p)
        
        for product in self.cart.values():
            product['total_price'] = product['item'].price * product['quantity'] 
            
            yield product
    
    def __len__(self):
        return sum(product['quantity'] for product in self.cart.values())
    
    def add(self, item_id, quantity=1, update_quantity=False):
        item_id = str(item_id)
        
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 1, 'id': item_id}

        if update_quantity:
            self.cart[item_id]['quantity'] += int(quantity) 
            
            if self.cart[item_id]['quantity'] == 0:
                self.remove(item_id)
                
        self.save()  
        
    def remove(self, item_id):
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()     
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
    
    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['item']= Item.objects.get(pk=p)
        
        return sum(product['quantity'] * product['item'].price for product in self.cart.values())

    