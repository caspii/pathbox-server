{% extends "layout.html" %}
{% block body %}
<div class=" container">
{% filter markdown %}

# Frequently Asked questions

#### How does it work?
You need an Android device on which to install the tracking app. Get the app here from Google Play.

Open the app and presss "Start tracking". That's all. You can then share your tracks by pressing the "Share Your tracks" button in the app and sending the link via email or Whatsapp.

Anyone with the link can see your location history.

---
#### Can I download my data?
You will be able to download your tracks in a GPX file format soon.

---
#### Can I delete my data?
Not yet. This feature is being worked on.

---
#### How can I prevent others from seeing my tracks?
Only people you send the link to can see your tracks. The link is not public and contains a random string of characters meaning that it can't be guessed.

Just make sure you only share the link with people you trust.

---
#### Is there an iOS / iPhone app?
Not yet.

---
#### What is the battery impact of this app?
The battery drain is barely noticable. The app uses passive location services.

---
#### What is the technology stack?
The server:

* The server is a [Python Flask](http://flask.pocoo.org/) application.
* It runs on a very small [Digital Ocean](http://digitalocean.com/) virtual server running Ubuntu.
* The frontend is styled with Bootstrap and [Bootswatch](https://bootswatch.com/).
* The database is SQLite and uses [Peewee](http://docs.peewee-orm.com/) as an ORM.
* It was coded with [PyCharm](https://www.jetbrains.com/pycharm/).

The app:

* Is a JAVA Android Application
* It was coded with [Android Studio](https://developer.android.com/studio/index.html).

---
#### Who made this and why?
This product was made by [Caspar von Wrede]('https://casparwre.de').
There are many location tracking services but I thought I could make the simplest one of all. 

Also, many of them do not come with their own easy way of viewing and sharing the recorded tracks.

---
{% endfilter %}
</div>
{% endblock %}  