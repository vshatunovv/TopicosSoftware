from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views import View
from django import forms


# Create your views here.
class HomePageView(TemplateView):
 template_name = 'pages/home.html'


class AboutPageView(TemplateView):
 template_name = 'pages/about.html'
 
 def get_context_data(self, **kwargs):
  context = super().get_context_data(**kwargs)
  context.update({
    "title": "About us - Online Store",
    "subtitle": "About us",
    "description": "This is an about page ...",
    "author": "Developed by: Vladlen Shatunov",
 })
  return context
 
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)    

            
 
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 800},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 999},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 99},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 75}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {
            "title": "Products - Online Store",
            "subtitle": "List of products",
            "products": Product.products
        }
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        product_id = self.get_product_index(id)

        if product_id is None:
            return redirect('home')

        product = Product.products[product_id]
        viewData["title"] = f"{product['name']} - Online Store"
        viewData["subtitle"] = f"{product['name']} - Product information"
        viewData["product"] = product

        return render(request, self.template_name, viewData)

    def get_product_index(self, id):
        try:
            index = int(id) - 1
            if 0 <= index < len(Product.products):
                return index
        except ValueError:
            pass
        return None



class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        data = self.cleaned_data['price']

        if data < 1:
            raise forms.ValidationError("The price should be a number greater than zero")
        
        return data

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            return render(request, 'products/confirmation.html')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)