from django.urls import path
from . import views
#urls and routes that determines the progression and redirection of pages
#it is also responsible for linking urls to functions in the views.py page to determine each pages functionality
urlpatterns = [
    path('log_reg', views.index),#root_page
    path('process', views.process_registration),#process registration form
    path('check_login', views.check),#process login form
    path('process/success_login', views.successful_login),#a value wasn't passed because request.session was used to pass the user_id #redirect to succefull log in page if the user really exists after vlaidation takes place
    path('process/success_register/<int:user_id>', views.successful_register),#a value was passed via url to view the user's name in the success page #redirect to succefull registration page and creates a new user to the database after vlaidation takes place
    path('destroy', views.delete),]#After logging out the users session is cleared to prevent access to the success page without logging in