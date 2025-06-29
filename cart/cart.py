from store.models import Product, Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        # Get request
        self.request = request
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        if product_id not in self.cart:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Covert {'3':1,  '2':4 } to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id not in self.cart:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Covert {'3':1,  '2':4 } to {"3":1, "2":4}
            carty=str(self.cart)
            carty= carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


    def cart_total(self):
        # Get product IDS
        product_ids = self.cart.keys()
        # lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        # Start counting at 0
        total = 0
        for key, value in quantities.items():
            # Covert key string into int so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + product.price * value

        return total

    def __len__(self):
        return len(self.cart)

    def get_product(self):
        # Get ID from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get cart
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True
        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Covert {'3':1,  '2':4 } to {"3":1, "2":4}
            carty=str(self.cart)
            carty= carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            # Get current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Covert {'3':1,  '2':4 } to {"3":1, "2":4}
            carty=str(self.cart)
            carty= carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
