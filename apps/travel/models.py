from __future__ import unicode_literals

from django.db import models

import re

passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

import bcrypt

from datetime import date, time
import types



class UserManager(models.Manager):
    def register(self, name, username, password, confirm):
        errors = 0
        messages = {}
        messages['name_error'] = []
        messages['username_error'] = []
        messages['password_error'] = []
        messages['confirm_error'] = []
        #Validations
        #First Name Field
        if len(name) <3:
            messages['name_error'].append('Name must be at least 3 characters!')
            errors += 1
        #Username Field
        if len(username) <3:
            messages['username_error'].append('Username must be at least 3 characters!')
            errors += 1
        #Password Field
        if len(password) < 8:
            messages['password_error'].append('Password must be more than 8 characters!')
            errors += 1
        elif not passwordRegex.match(password):
            messages['password_error'].append('Password must contain at least one lowercase letter, one uppercase letter, and one digit')
            errors += 1
        #Confirm Field
        if len(confirm) < 8:
            messages['confirm_error'].append('Confirm Password must be more than 8 characters!')
            errors += 1
        elif password != confirm:
            messages['confirm_error'].append("Passwords Do Not Match")
            errors += 1
        #FAST-FAIL
        if errors>0:
            #return error messages
            return(False, messages)
        else:
            #register and add user to db
            secret = bcrypt.hashpw(str(password), bcrypt.gensalt())
            query = User.uManager.create(name=name, username=username, password=secret)
            query.save()
            return(True, query)

    def login(self, login_username, login_password):
        errors = 0
        login_messages = {}
        login_messages['login_username_error'] = []
        login_messages['login_password_error'] = []
        #Validations
        #Email Field
        if len(login_username) < 3:
            login_messages['login_username_error'].append("Username must be at least 3 characters!")
            errors += 1
        #Password Field
        if len(login_password) < 8:
            login_messages['login_password_error'].append("Password must be more than 8 characters!")
            errors += 1
        elif not passwordRegex.match(login_password):
            login_messages['login_password_error'].append("Password must contain at least one lowercase letter, one uppercase letter, and one digit")
            errors += 1
        #FAST-FAIL
        if errors>0:
            #return error messages
            return(False, login_messages)
        else:
            #check if username exists in db
            query = User.uManager.filter(username=login_username)
            input_password = login_password.encode()

            #if username doesn't match, return error message
            if len(query) == 0:
                login_messages['login_username_error'].append("Username not in database! Please register!")
                return(False, login_messages)

            #if username matches, check if passwords match
            elif bcrypt.checkpw(input_password, query[0].password.encode()):
                return(True, query)

            #if username matches and passwords do not match, return error message
            else:
                login_messages['login_password_error'].append('Incorrect Password!')
                return(False, login_messages)

        return redirect('/')



class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    uManager = UserManager()


class TripManager(models.Manager):
    def add(self, destination, plan, start_date, end_date, user_id):
        errors = 0
        messages = {}
        messages['destination_error'] = []
        messages['plan_error'] = []
        messages['start_date_error'] = []
        messages['end_date_error'] = []

        #Validations
        #Destination Field
        if len(destination) <1:
            messages['destination_error'].append('Please enter a destination!')
            errors += 1
        #Plan Field
        if len(plan) <1:
            messages['plan_error'].append('Please enter a plan!')
            errors += 1
        #Start Date Field

        start = start_date
        end = end_date
        now = unicode(date.today())

        print start

        if start < now:
            messages['start_date_error'].append('Start date must be in the future!')
            errors += 1
        #End Date Field Field
        if end < now:
            messages['end_date_error'].append("End date must be in the future!")
            errors += 1
        elif end < start:
            messages['end_date_error'].append("You can't come home before your trip starts!")
            errors += 1
        #FAST-FAIL
        if errors>0:
            #return error messages
            return(False, messages)
        else:
            #add trip to db
            query = Trip.tManager.create(destination=destination, plan=plan, end_date=end_date, start_date=start_date, user=User.uManager.get(id=user_id))
            query.save()
            return(True, query)

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField(default=date.today())
    end_date = models.DateField(default=date.today())
    plan = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User)

    tManager = TripManager()

class Join(models.Model):
    user = models.ForeignKey(User)
    trip = models.ForeignKey(Trip)
