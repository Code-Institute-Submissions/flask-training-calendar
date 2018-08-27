# Running Calendar

Data Centric Development Project - Code Institute

Running Calendar is a web app for planning runs with a social media aspect where users can perform the following functions:
* Plan upcoming runs
* Mark runs as complete
* Edit and delete runs
* Upload workout photos
* Update account information
* Get password reset emails
* Follow other users
* Comment on runs

It was built in Python3 using the Flask microframework.

### This project is for educational purposes only

### A live version is hosted [here](http://mpark-flask-training-calendar.herokuapp.com/)  

## UX

The inspiration for this project came when I was writing out a training schedule for an upcoming race and realised that, while there are many run tracking apps, very few offer functionality to plan upcoming runs.  
I felt the opportuntiy was there for users to plan out training schedules and then be able to easily access the site to see what their planned run for the day consisted of.  

The visual theme for the site is kept relatively simple and consistent throughout the site.  
A background image of a silhouetted runner against the sun is used to evoke an inspirational view of running.  
I felt it is a powerful image and chose to give it a sharp focus throughout the site, dedicating a third of the screensize to it.  
On smaller devices the image of the runner is not visible. However I chose to keep the background image, as the viewable portion (an orange sky at sunset) makes the background visually interesting while still unobtrusive.  
Beyond that all information for the user is displayed intuitively to make it easy for the user to comprehend and interact with. 


On the home page information is displayed relating to the planned workouts for the current day.  
If there are no workouts planned for the current day the homepage will instead display random motivational messages.  
If an unregistered user visits the site the home screen will display options for logging in or registering.  


A user is required to have an account to access all features of the site.  
For the purposes of viewing/testing the site I have created the following dummy accounts that make use of the site's features, please use them or create your own account to access the site, where you can also follow these accounts:

* Account 1
    * **username:** Daniel Tibor
    * **email:** dan@fake.com
    * **password:** danpassword
* Account 2 
    * **username:** Hilde Farley
    * **email:** hilde@fake.com
    * **password:** hildepassword
* Account 3
    * **username:** Shelby Morris
    * **email:** shelby@fake.com
    * **password:** shelbypassword
* Account 4
    * **username:** Anna Garcia
    * **email:** anna@fake.com
    * **password:** annapassword


## Technologies Used
* HTML
* CSS
* Bootstrap
* Python3
* Flask Microframework
* Flask-Bcrypt
    * A flask extension for encypting passwords
* Flask-Login
    * A flask extension for user session management
* Flask-Mail
    * A flask extension used for sending emails
* Flask-S3
    * A flask extension for hosting static assets from Amazon S3
* Flask-SQLAlchemy
    * A flask extension that adds support for SQLAlchemy
* Jquery
* Popper.js
    * A javascript library for enabling dropdowns
* lightbox
    * A javascript library for displaying images


### Wireframing

Wireframes were made using the pencil application and can be found in the wireframes folder

## Features

### Existing Features
* Users can easily register and log in.
* A user can request a password reset email if they forget their password
* A user can plan an upcoming run.
* In planning an upcoming run various run specific options are availble to be chosen such as run type, unit of measurement etc.
* Runs can be edited, deleted, or marked as completed.
* Upcoming runs are displayed with the nearest upcoming run displayed first.
* Completed runs are displayed with the most recent completed run first.
* A user can upload photos taken on their run.
* Users can search for and follow other users.
* Users can comment on their own and other user's runs.
* A user can edit or delete any comment they've made.
* A user can delete any comment made on a run they've created.
* A user cannot edit a comment they didn't create.
* A user can unfollow a user they're following.
* A user can update their account imformation through the accounts page - name, email and account image.
* Users can log out.
* A user cannot view a workout of a user they are not following

### Features left to implement
* Give users the option to delete workout photos
* Enable easier navigations between next/previous workouts on the workout page
* Increase the intuitiveness of site navigation. Presently there is an over-reliance on using the navbar links and browser back button.
* Set up a request system where a user can request to follow another user, presently a user can follow any user on the site
* Set up a newsfeed where users can view activities of other users as they create them.
* notifications for a user when a follower comments on one of their workouts.
* Enable users to comment on individual photos.
* A calendar view where users can view there upcoming workouts on a calendar and change the dates of the workouts by clicking and dragging.
* I would like to further refine the style, for example on the image gallery, I would like to make the simple thumbnail grid more visually appealing.


## Testing
The site was tested on 21" monitors, 15" and 13" laptop screens and on an iPhone SE and iPhone 8 screen to test responsiveness.  
It was also tested using chrome, firefox and safari.
 

All testing was performed manually to ensure links/form submissions/model relationships worked correctly and that the site was defensively designed.  

Manual testing was done to ensure:
* The site works as intended
* User entered information was handled correctly (adding/editing/deleting workouts & comments, uploading photos, changing account information)
* Password reset emails work correctly
* logging in and out and registering works as intended
* Defensive design:
    * Unregistered users do not have access to any area of the site other than login and register routes
    * Registered users cannot access information relating to a user whom they are not following.
    * Only a user who creates a run can edit/delete the run or mark it as complete.
    * Only a user who creates a comment can edit it
    * Only the user who creates a comment or the user whose workout the comment is attached to can delete it

A bug was found on safari where the input date field on adding/editing a workout does not show a datepicker. It requires the user to input a target date in the correct format.  
This is a bug I have yet to find a solution for. 

Originally the form to add a workout only accepted dates from the current date on so a user could not plan a workout with a date in the past. However this caused issue if a user wanted to edit a completed run with a date in the past.  
I felt it was better to remove the neccessity to enter a date in the future as users also may want to enter details of a workout they've already completed.

## Deployment
The site is hosted on heroku.  
Static assets are hosted on Amazon S3. 

### Run locally
The code is set up to host static assets on aws.  
To run this site locally including hosting static assets locally please use the following steps:
1. Clone the [github repository](https://github.com/mparkcode/flask-training-calendar)
2. In your terminal enter:
```
pip3 install -r requirements.txt
```
3. You will have to create the database tables, in the python3 interpreter enter:
```
from flasktrainingcalendar import db
db.create_all()
```
4. To get your static assets from local folders, in \_\_init\_\_.py change the setting on FLASK_S3 active to false like so:
```
app.config['FLASKS3_ACTIVE'] = False
```
5. You will need to set a secret key in your environment variables, you can get a randomly generated one from [https://randomkeygen.com/](https://randomkeygen.com/)
6. To upload user account image photos and workout photos to the local static folder, in routes.py you will have to change the following two functions to look as they appear below:
    
```
*function for saving profile picture


def save_profile_picture(form_picture):          
    random_hex = ''.join([random.choice(string.digits) for n in range(8)])    
    _, f_ext = os.path.splitext(form_picture.filename)  
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
```
    
```
*function for saving workout picture


def save_workout_picture(form_picture):          
    random_hex = ''.join([random.choice(string.digits) for n in range(8)])    
    _, f_ext = os.path.splitext(form_picture.filename)  
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/workout_pics', picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn
```
7. You will need to install pillow for saving images locally, in your terminal enter 
```pip3 install pillow```
8. In the import section at the top of routes.py, import Image from pillow like so:
```
from PIL import Image
```
9. You will need to create a folder called workout_pics in your static folder, user uploaded workout pictures will be saved here.
9. To run the app from your terminal type: 
```python3 run.py```
10. If you wish to set up the password reset function, currently the settings are for a google account, in your environment variable you can enter information for the mail address and password. Please note that you will have to change the security settings on this email account to allow less secure access.

## Credits

### Media
* The background image was obtained from Pexel
* user uploaded images on dummy accounts were obtained from google images
* Fonts used were obtained from Google Fonts

### Acknowledgements
Understanding of how to structure an app built with the Flask microframework in this fashion and how to use the various flask extensions, as well as minor styling influences were obtained from [Corey Schafer's flask blog tutorials](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH).  
Various code snippets were obtained from this tutorial as well.  
Understanding of how to implement a followers system was obtained from [Miguel Grinberg's flask mega-tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-viii-followers-contacts-and-friends).