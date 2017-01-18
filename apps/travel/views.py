from django.shortcuts import render, redirect
from .models import User, Trip, Join

# Create your views here.
def index(request):
    return render (request, 'travel/index.html')

def register(request):
    if request.method == "POST":
        result = User.uManager.register(name=request.POST['name'], username=request.POST['username'], password=request.POST['password'], confirm=request.POST['confirm'])
        if result[0]:
            request.session['current_user_id'] = result[1].id
            request.session['errors'] = []
            return redirect('/main/travels')
        else:
            request.session['errors'] = result[1]
            return redirect('/main')
    else:
        return redirect ('/main')

def login(request):
    if request.method == "POST":
        result = User.uManager.login(login_username=request.POST['login_username'], login_password=request.POST['login_password'])

        if result[0]:
            request.session['current_user_id'] = result[1][0].id
            request.session['errors'] = []
            return redirect('/main/travels')
        else:
            request.session['errors'] = result[1]
            return redirect('/main')
    else:
        return redirect ('/main')

def welcome(request):
    if request.session['current_user_id']:
        request.session['errors'] = []
        query = User.uManager.filter(id=request.session['current_user_id'])
        query2 = Join.objects.filter(user=request.session['current_user_id'])
        query3 = Trip.tManager.exclude(user_id=request.session['current_user_id'])
        context = {
            'info' : query,
            'trips' : query2,
            'other_trips' : query3
        }
        return render (request, 'travel/dashboard.html', context)
    else:
        return redirect ('/main')

def logout(request):
    request.session['current_user_id'] = ""
    request.session['errors'] = []
    request.session['join_error'] = ""
    return redirect('/main')

def add_page(request):
    request.session['join_error'] = ""
    return render (request, 'travel/add_trip.html')

def add_trip(request):
    if request.method == "POST":
        result = Trip.tManager.add(destination=request.POST['destination'], plan=request.POST['plan'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], user_id=request.session['current_user_id'])
        if result[0]:
            request.session['add_errors'] = []
            Join.objects.create(user=User.uManager.get(id=request.session['current_user_id']), trip=Trip.tManager.get(id=result[1].id))
            return redirect('/main/travels')
        else:
            request.session['add_errors'] = result[1]
            return redirect('/main/travels/add')
    else:
        return redirect ('/main/travels/add')

def show (request, trip_id):
    request.session['join_error'] = ""
    query = Trip.tManager.filter(id=trip_id)
    query2= Join.objects.filter(trip_id=trip_id)
    context = {
        'details' : query,
        'others' : query2
    }
    return render (request, 'travel/destination.html', context)

def join(request, trip_id):
    #check if user joined trip
    check = Join.objects.filter(user_id=User.uManager.get(id=request.session['current_user_id']))
    #hasn't joined, join user
    if len(check) == 0:
        Join.objects.create(user=User.uManager.get(id=request.session['current_user_id']), trip=Trip.tManager.get(id=trip_id))
        return redirect ('/main/travels')
    #has joined, error
    else:
        request.session['join_error'] = 'You already joined this trip!'
        return redirect ('/main/travels')

def unjoin(request, trip_id):
    #check if user user joined trip
    check = Join.objects.filter(user_id=User.uManager.get(id=request.session['current_user_id']))
    #has't joined, error
    if len(check) == 0:
        request.session['join_error'] = "You haven't joined this trip!"
        return redirect ('/main/travels')
    #has joined, delete
    else:
        Join.objects.filter(user_id=User.uManager.get(id=request.session['current_user_id'])).delete()
        return redirect ('/main/travels')

def delete_trip(request, trip_id):
    #check if trip exists
    Trip.tManager.filter(id=trip_id).delete()
    return redirect ('/main/travels')
