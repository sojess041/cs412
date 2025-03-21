from django.shortcuts import render
import random
import time
from datetime import datetime, timedelta
# Create your views here.


def main_page(request):
    #show main page of the restaurant 
    template_name = 'restaurant/main.html'

    return render(request, template_name)
 
def order_form(request):
    specials = ["Burger Meal ($8)", "Pasta Combo ($9)", "Chicken Platter ($12)", "Kids Chicken Meal ($10)"]
    daily_special = random.choice(specials)  

    context = {"daily_special": daily_special}
    return render(request, "restaurant/order.html", context)
def submit_order(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        instructions = request.POST.get("instructions")
        print("change")

        menu_options = {
            "Chickenjoy": 10,
            "Jolly Spaghetti": 5,
            "French Fries": 3,
            "Kids Meal": 5,
        }
        dessert_options = {
            "Chocolate Sundae": 3,
            "Caramel Sundae": 3,
            "Plain Cone": 2,
            "Peach Mango Pie": 2,
        }

        order_items = []
        total_price = 0 

        for item, price in menu_options.items():
            if request.POST.get(item):
                order_items.append(f"{item} (${price})")
                total_price += price

        dessert_items = []
        for dessert, price in dessert_options.items():
            if request.POST.get(dessert):
                dessert_items.append(f"{dessert} (${price})")
                total_price += price
        ready_minutes = random.randint(30, 60)
        ready_time = (datetime.now() + timedelta(minutes=ready_minutes)).strftime("%I:%M %p")

        context = {
            "name": name,
            "phone": phone,
            "email": email,
            "instructions": instructions,
            "order_items": order_items,
            "dessert_items": dessert_items,
            "total_price": total_price, 
            "ready_time": ready_time, 
        }
        


        return render(request, "restaurant/confirmation.html", context)