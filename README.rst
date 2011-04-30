=========================================
 Django Facebook App basics
=========================================

Requirements
============
* Django
* `facebook_sdk`_
.. _facebook_sdk: https://github.com/facebook/python-sdk


Why another django project about facebook apps?
=========================================
Because Pyfacebook is out of date and i wanted something much more simple and flexible than the other projects i found.



Installation
============
Just download and modify facebook_settings.py according to your facebook app data



Description
===========
This Django project explains in 70 lines of code some of the basics of creating Facebook apps using Django.

At the url /canvas/  you'll find a view that:

* Checks if the data are really coming from Facebook
* If the user did not authorize your app, redirects to Facebook OAuth dialog page
* If the application is authorized, creates an instance of a FacebookUser model containing some of the user's data
* That's all...

Thanks to Sulil Arora for sharing this snippet, it helped a lot: http://sunilarora.org/parsing-signedrequest-parameter-in-python-bas  


