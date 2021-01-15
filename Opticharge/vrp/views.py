from .models import *
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse,HttpResponseRedirect
import pandas as pd
from .exports import *
from django.urls import reverse,reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
import subprocess
from subprocess import run,PIPE
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decimal import Decimal
import math
import sys

# Create your views here.
def index(request):
    context = {'msg':'Welcome'}
    return render(request,'vrp/index.html',context)

def export(request):
    generate_stop_csv()
    return HttpResponse("Hello world, you exported the addresses.")

def show(request, pk):
    my_list = []
    df = pd.read_csv("data/dist_mat_[tour_{}].csv".format(pk))
    for i in df.index:
        my_list.append([df.iloc[i,0], df.iloc[i,1], df.iloc[i,2], df.iloc[i,3]])

    context = {'object_list': my_list}
    return render(request, 'vrp/show.html', context)

def show_vrp(request, pk):
    my_list = []
    df = pd.read_csv("data/dist_mat_[tour_{}].csv".format(pk))
    for i in df.index:
        my_list.append([df.iloc[i,0], df.iloc[i,1], df.iloc[i,2], df.iloc[i,3]])

    context = {'object_list': my_list}
    return render(request, 'vrp/show.html', context)

# java test
def java(request):
    """Test call to a java jar"""
    subprocess.Popen(['java', '-jar', 'hello.jar', "argument-1", "argument-2"])
    context = {'msg': "ran java"}
    return render(request, 'vrp/index.html', context)

#adress views
class AddressListView(ListView):
    model = Address
    template_name ='vrp/adress_list.html'
    paginate_by = 5

class AddressDetailView(DetailView):
        model = Address
        template_name='vrp/adress_detail.html'

class AddressCreateView(CreateView):
    model = Address
    fields = ["name", "street", "city", "latitude", "longitude" ]
    template_name='vrp/adress_form.html'

    def get_success_url(self):
        return reverse('address-list')

class AddressUpdateView(UpdateView):
    model = Address
    fields = ["name", "street", "city", "latitude", "longitude" ]
    template_name = "vrp/address_update_form.html"

    def get_success_url(self):
        return reverse('address-list')

class AddressDeleteView(DeleteView):
    model = Address

    def get_success_url(self):
        return reverse('address-list')

# Vehicle Views
class VehicleListView(ListView):
    model = Vehicle
    template_name ='vrp/vehicule_list.html'
    paginate_by=5

class VehicleDetailView(DetailView):
    model = Vehicle
    template_name='vrp/vehicle_detail.html'

class VehicleCreateView(CreateView):
    model = Vehicle
    fields = ["marque","registrationnumber","capacity","type", "notes", ]
    template_name='vrp/vehicle_form.html'

    def get_success_url(self):
        return reverse('vehicle-list')

class VehicleUpdateView(UpdateView):
    model = Vehicle
    fields = ["marque","registrationnumber", "capacity", "type", "notes", ]
    template_name = "vrp/vehicle_update_form.html"

    def get_success_url(self):
        return reverse('vehicle-list')

class VehicleDeleteView(DeleteView):
    model = Vehicle

    def get_success_url(self):
        return reverse('vehicle-list')

#Planification Views
class PlanificationListView(ListView):
    model = Planification
    template_name ='vrp/planification_list.html'
    paginate_by = 5

class PlanificationDetailView(DetailView):
    model = Planification
    template_name='vrp/planification_detail.html'

class PlanificationCreateView(CreateView):
    model = Planification
    fields = ["date", "valide"]
    template_name='vrp/planification_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
      return reverse('planification-list')



class PlanificationUpdateView(UpdateView):
    model = Planification
    fields = ['date','valide']
    template_name='vrp/planification_update_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        planification = self.get_object()
        if self.request.user == planification.author:
            return True
        return False
    def get_success_url(self):
        return reverse('planification-list')

class PlanificationDeleteView(DeleteView):
    model = Planification
    success_url = '/planification/'

    def test_func(self):
        planification = self.get_object()
        if self.request.user == planification.author:
            return True
        return False

#Customer Views

class CustomerListView(ListView):
    model = Customer
    template_name ='vrp/customer_list.html'
    paginate_by = 5

class CustomerDetailView(DetailView):
    model = Customer
    template_name='vrp/customer_detail.html'

class CustomerCreateView(CreateView):
    model = Customer
    fields = ["firstname", "familyname", "address", "demand", "phone", "typevehicle"]
    template_name='vrp/customer_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('customer-list')

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ["firstname", "familyname", "address", "demand","typevehicle","phone"]
    template_name='vrp/customer_update_form.html'
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('customer-list')

class CustomerDeleteView(DeleteView):
    model = Customer
    def get_success_url(self):
        return reverse('customer-list')


# Tour Views

class TourListView(ListView):
    model = Tour
    template_name='vrp/tour_list.html'
    paginate_by=5

class TourDetailView(DetailView):
    model = Tour
    template_name='vrp/tour_detail.html'

class TourCreateView(CreateView):
    model = Tour
    form_class = TourForm
    # fields = ["date", "start_location", "end_location", "stops", "vehicles", "drivers", "notes", ]
    template_name='vrp/tour_form.html'

    def get_success_url(self):
        return reverse('tour-list')

class TourUpdateView(UpdateView):
    model = Tour
    form_class = TourForm
    # fields = ["date", "start_location", "end_location", "stops", "vehicles", "drivers", "notes", ]
    template_name = "vrp/tour_update_form.html"

    def get_success_url(self):
        return reverse('tour-list')

class TourDeleteView(DeleteView):
    model = Tour

    def get_success_url(self):
        return reverse('tour-list')

def tour_calculate(request, pk):
    """Calculates the optimal solution for a tour"""
    tour = Tour.objects.get(pk=pk)
    addresses = tour.stops.all()

    # delete previously existing files:
    filename = "data/vrp_output/solution_tour[{}].xml".format(pk)
    if os.path.exists(filename):
        os.remove(filename)

    # export points (for dist mat and services)
    export_points(tour)
    export_vehicles(tour)

    # gen distmat
    f_in = "data/points_for_[tour_{}].csv".format(pk)
    f_out = "data/dist_mat_[tour_{}].csv".format(pk)
    # clean old files
    if os.path.exists(f_out):
        os.remove(f_out)
    gh_folder = "data/gh_data"
    p = subprocess.Popen(['java', '-jar', 'java/gh_module.jar', f_in, f_out, gh_folder])

    # start calculation
    context = {'object': tour, 'addresses': addresses}
    return render(request, 'vrp/tour_calculate.html', context)

def tour_show_routes(request, pk):
    """Calculates the optimal solution for a tour"""
    tour = Tour.objects.get(pk=pk)
    tour.parse_xml()
    routes = tour.route_set.all()
    #TODO calculate routes in ghopper
    dist_mat = pd.read_csv("data/dist_mat_[tour_{}].csv".format(pk))
    dist_mat["distance"] = round(dist_mat["distance"]/1000,2)
    dist_mat["distance"] = dist_mat["distance"].apply(Decimal)
    dist_mat["duration"] = dist_mat["duration"].apply(Decimal)

    print(dist_mat)

    for r in routes:
        stops = r.stop_set.all()
        length = stops.count()
        for i in range(1,length):
            stop = stops[i]
            from_id = stops[i-1].address.id
            to_id = stop.address.id
            print(stops[i-1].address.id, stop.address.id)
            print(dist_mat[(dist_mat["from id"] == from_id) & (dist_mat["to id"] == to_id)])
            print(dist_mat[(dist_mat["from id"] == from_id) & (dist_mat["to id"] == to_id)]["distance"])
            stop.distance = dist_mat[(dist_mat["from id"] == from_id) & (dist_mat["to id"] == to_id)]["distance"].values[0]
            stop.duration = dist_mat[(dist_mat["from id"] == from_id) & (dist_mat["to id"] == to_id)]["duration"].values[0]
            stop.save(update_fields=['distance', 'duration'])
            print(stop.distance, stop.duration)




    context = {'tour': tour, 'routes': routes}

    return render(request, 'vrp/show_routes.html', context)

def tour_send_routes_old(request, pk):
    tour = Tour.objects.get(pk=pk)
    routes = tour.route_set.all()
    msg = "Hallo Olli,\nthese are the routes:\n\n"
    for r in routes:
        msg += "*" + r.__str__() + ":*\n"

    subject = "Tour Plan"
    res = send_mail(subject, msg, "novaky.nurse@gmail.com", ["oliver.folba@gmail.com"])
    return HttpResponse('%s'%res)

def tour_send_routes(request, pk):
    tour = Tour.objects.get(pk=pk)
    routes = tour.route_set.all()
    subject, from_email, to = '{} Plan'.format(tour), 'novaky.nurse@gmail.com', 'oliver.folba@gmail.com'
    html_content = render_to_string('vrp/tour_email.html', {'tour': tour, 'routes': routes}) # ...
    text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    context = {"msg": "Email sent"}
    return render(request, 'vrp/index.html', context)


def customer_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location=settings.CUSTOMER_ROOT+'/text')
        filename = fs.save(myfile.name, myfile)
        uploaded_file_customer_url = fs.url(filename)
        context={'file_customer':myfile}
        return render(request, 'vrp/simple_upload_customer.html',context)
    return render(request, 'vrp/simple_upload_customer.html')


def vehicle_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(location=settings.VEHICLE_ROOT+'/text')
        filename = fs.save(myfile.name, myfile)
        uploaded_file_vehicle_url = fs.url(filename)
        return render(request, 'vrp/simple_upload_vehicle.html')
    return render(request,'vrp/simple_upload_vehicle.html')

def manage_file(request):
    path= settings.CUSTOMER_ROOT
    files_list = os.listdir(path+'/json')
    context = {'customers' : files_list}
    return render(request, "vrp/planification_form.html", context)

def customer_to_json(request):
        from .text2jsonCust import main
        main()
        return HttpResponseRedirect('/file-customer/')

def vehicle_to_json(request):
    from .text2jsonVeh import main
    main()
    return HttpResponseRedirect('/file-vehicle/')

from Opticharge.settings import BASE_DIR
import os.path
import csv
from .GA_utils import load_instance
import json
def vrp_planning(request):
    if request.method == "POST" and request.FILES['file_customer'] and request.FILES['file_vehicle']:
        InstanceC = request.FILES['file_customer']
        InstanceV = request.FILES['file_vehicle']
        population_size=request.POST.get("population")
        individual_size=request.POST.get("individual_size")
        number_generation =request.POST.get("number_generation")
        crossover = request.POST.get("crossover")
        mutation=request.POST.get("mutation")
        tour_file_name=f'{InstanceC}_{InstanceV}.csv'
        path= settings.RESULT_ROOT
        csvfile=os.path.join(path,tour_file_name)
        print(csvfile)
        context={
            'population_size': population_size,
            'individual_size' : individual_size,
            'number_generation': number_generation,
            'crossover': crossover,
            'mutation': mutation,
            'InstanceC':InstanceC,
            'InstanceV':InstanceV,
            'csvfile':csvfile
        }
        from .GA_Algo import run_gavrp
        run_gavrp(instanceC_name=InstanceC,instanceV_name=InstanceV,ind_size=individual_size,pop_size=population_size,cx_pb=crossover,mut_pb=mutation,n_gen=number_generation,export_csv=True)
        pd.set_option('display.max_rows', None)
        datatour = pd.read_csv(csvfile)
        data_html = datatour.to_dict()
        df=pd.DataFrame(data=data_html)

        data_html=df.to_dict()
        dv=pd.DataFrame(df.Route.apply(lambda x:pd.Series(str(x).split("],"))))
        df=pd.DataFrame(df.Route.apply(lambda x:pd.Series(str(x).split("],"))))
        rows=len(df.columns)
        dv_t=dv.T
        for i in range(1,rows):
            dv_t.at[i,1]=dv_t[0].iloc[i][2:].split(',')[0]
            dv_t.at[i,2]=dv_t[0].iloc[i][5:].split(']')[0]
            i=+1
        dv_t.at[0,1]=dv_t[0].iloc[0][2:].split(',')[0]
        dv_t.at[0,2]=dv_t[0].iloc[0][5:].split(']')[0]

        json_data_dirC = os.path.join(BASE_DIR, 'dataC', 'json')
        json_fileC = os.path.join(json_data_dirC, f'{InstanceC}')
        instance = load_instance(json_file=json_fileC)

        customers=[0]*len(dv_t[2])
        latitude=[0]*len(dv_t[2])
        longitude=[0]*len(dv_t[2])
        for tour in range(len(dv_t[2])):
            customers[tour]=dv_t[2].iloc[tour].split(',')
            latitude[tour]=dv_t[2].iloc[tour].split(',')
            longitude[tour]=dv_t[2].iloc[tour].split(',')
            list=[0]*len(dv_t[2])
            for point in range (len(customers[tour])):
                list[tour]=instance[f'customer_{int(customers[tour][point])}']['coordinates']['x']
                latitude[tour][point] = instance[f'customer_{int(customers[tour][point])}']['coordinates']['x']
                longitude[tour][point] = instance[f'customer_{int(customers[tour][point])}']['coordinates']['y']
        latitude=json.dumps(latitude)
        longitude=json.dumps(longitude)
        context = {'loaded_data': dv_t.index.tolist(),'dv_t':dv_t[1].tolist(),'df_t':dv_t[2].tolist(),'latitude':latitude,'longitude':longitude}
        return render (request,'vrp/vrp.html',context)
    return HttpResponse ('hi')


