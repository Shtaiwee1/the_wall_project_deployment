from django.shortcuts import render , redirect
from django.contrib import messages#import error messages for display
import bcrypt#importing bcrypt after installing using pip install bcrypt used for hashing,encoding and decoding
from .models import User#importing class from models.py


#root page
def index(request):
    context={"all_users":User.objects.all()}#passes the models attributes to the rendered page
    return render(request, "index.html",context)
#registration information processing function and validation
def process_registration(request):
    errors = User.objects.basic_validator(request.POST)#passes the data from form to the validators function in models which are then called (postData)-validates and then returns errors from the models page
    request.session["coming_from"]="REGISTER"
    if len(errors) > 0:#if there are errors loop through keys and values in the errors dictionary
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/log_reg')#if there are any errors redirect to the root page
    else:
        #save info from form and create a new user with a hashed password
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()#hashing the new users password
        #creating a new user using info from registration form
        new_user=User.objects.create(first_name=first_name,
                                    last_name=last_name,
                                    email=email,
                                    password=pw_hash)
        return redirect(f"/process/success_register/{new_user.id}")#redirection to the success page passing the user_id via url to display the name
#process and validation for the login form information
def check(request):
    errors = User.objects.basic_validator_second(request.POST)
    request.session["coming_from"]="LOGIN"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/log_reg')#if there are any errors redirect to the root page no access for the success page
    else:
        user = User.objects.filter(email=request.POST['email_login'])#searches the database for the email input in the login form
        if user: #if there is a user with the input email = true
            logged_user = user[0]#save the user info ina varibale called logged_user
            print(logged_user)
            #check if the password form thelogin form equals the hashed password in the database
            #converts the password from the form from string to byte and the hashed password in the database from hash to byte and compares the two of them 
        if bcrypt.checkpw(request.POST['password_login'].encode(), logged_user.password.encode()):#if the passwords match redirect to success page and save the logged in users info to display them in the success page
            request.session['userid'] = logged_user.id
            request.session['firstname'] = logged_user.first_name
            request.session['lastname'] = logged_user.last_name
            request.session['email'] = logged_user.email
            return redirect('/')
    return redirect('/log_reg')#if passwords don't match redirect to root page to let the user try again
#function induced upon succeful registration
def successful_register(request , user_id):#gets the user_id as a parameter from the process registration page which sends user_id via url route
    registered_user=User.objects.get(id=user_id)#get the specific user for that specific id
    context={"new_user" : registered_user}#use a dictionary to save info values of the user in a key named new_user
    return render(request, "success_register.html", context)#access the info values of the user in successs page using context dictionary to access the key:new_user andthe values:rigestered user ##page rendered upon successful registration
#function induced upon succeful logging in
def successful_login(request):
    if "email" not in request.session:#prevents users to access success page before logging in
        return redirect('/log_reg')#if email is not saved in session redirect to root
    return render(request, "success_login.html")#page rendered upon successful logging in
#function induced when pressing the logout url anchor in the success page
def delete(request):#the logout button redirects to the (destroy) route in the urls.py and then induces this function in the views.py to clear logged user info
    request.session.clear()
    return redirect('/log_reg')
    # user_log_out=User.objects.get(id=user_id)
    # user_log_out.delete()
    # log_out_user=User.objects.get(id=user_id)
    


