def clean(cart_detail):
    print(cart_detail.cart.restaurant, cart_detail.food.restaurant)
    if cart_detail.cart.restaurant == cart_detail.food.restaurant:
        pass
    else:
        print("cart detail clean")
        # erase all the items from other restaurant
        CartDetail.objects.filter(cart=cart_detail.cart).delete()
        cart = cart_detail.cart
        # reset the cart restaurant
        
        cart.restaurant = cart_detail.food.restaurant
        cart.bill = 0
        # print("125", restaurant,self.food.restaurant, cart.id, cart.bill)
        cart.save()
