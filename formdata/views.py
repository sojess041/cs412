from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.



def show_form(request):
    return render(request, 'formdata/form.html')  


def submit(request):

    template_name= "formdata/confirmation.html"
#process to submit the form submission and generate a result 
    print(request)

    if request.POST:
        #extract form fields into variables 
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        context = {
            'name': name,
            'favorite_color': favorite_color,
        }

    return render(request, template_name, context = context)