from reservadjango.models import Servicio
from accounts.models import Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        #get current session key if exists
        cart = self.session.get('session_key')
        #if new
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart


    def db_add (self, servicio, cantidad):
        servicio_id = str(servicio)
        cantidad = int(cantidad)
        if servicio_id in self.cart:
            self.cart[servicio_id]+= cantidad
        else:
            self.cart[servicio_id] = int(cantidad)
        
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id= self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))


    def add (self, servicio, cantidad):
        servicio_id = str(servicio.id)
        cantidad = int(cantidad)
        if servicio_id in self.cart:
            self.cart[servicio_id]+= cantidad
        else:
            self.cart[servicio_id] = int(cantidad)
        
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id= self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))
    
    def __len__(self):
        return len(self.cart)
    
    def get_products(self):
        #get ids from cart
        servicio_ids = self.cart.keys()
        #usar ids para ver los proudctos en DB
        servicios = Servicio.objects.filter(id__in= servicio_ids)

        return servicios
    
    
    def get_cantidades(self):
        cantidades = self.cart
        return cantidades
    
    def update(self, servicio, cantidad):
        print(servicio, cantidad)
        servicio_id = str(servicio)
        cantidad = int(cantidad)

        #get cart {'4':3, '1':2}
        cart = self.cart
        cart[servicio_id] = cantidad

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id= self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))

        return self.cart
    

    def delete(self,servicio):
        servicio_id = str(servicio)
        
        if servicio_id in self.cart:
            del self.cart[servicio_id]
        
        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id= self.request.user.id)
            carty = str(self.cart)
            carty = carty.replace("\'","\"")
            current_user.update(old_cart=str(carty))

        return self.cart
    

    def cart_total(self):
        #get service ids
        servicio_id = self.cart.keys()
        #look in db
        servicios = Servicio.objects.filter(id__in=servicio_id)
        cantidades = self.cart
        total = 0

        for key, value in cantidades.items():
            key = int(key)
            for servicio in servicios:
                if servicio.id == key:
                    if servicio.descuento:
                        total = total + (servicio.precio_descuento * value)
                    else:
                        total = total + (servicio.precio * value)
        
        return total
        
