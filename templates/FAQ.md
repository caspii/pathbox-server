{% extends "layout.html" %}
{% block body %}
<div class=" container">
{% filter markdown %}

# Frequently Asked questions

### Where can I download the app?

The app **was** available on Google play but didn't work that well. It's being redeveloped with new technologies. Stay tuned!

---
### How does it work?
You need an Android device on which to install the tracking app. 

Open the app and presss "Start tracking". That's all. You can then share your tracks by pressing the "Share Your tracks" button in the app and sending the link via email or Whatsapp.

Anyone with the link can see your location history.


---
### How can it work without an account, login or password?
The app generates a link that contains a unique key. Only people with that exact link can access the tracks from that particular install of the app. 


---
### Can I download my data?
You will be able to download your tracks in a GPX file format soon.

---
### How can I delete my data?
Please send a mail including the link to your tracks to <a href="mailto:caspar.wrede@gmail.com">this e-mail address</a>.

---
### How can I prevent others from seeing my tracks?
Only people you send the link to can see your tracks. The link is not public and contains a random string of characters meaning that it can't be guessed.

Just make sure you only share the link with people you trust.

---
### Is there an iOS / iPhone app?
Not yet.

---
### What is the battery impact of this app?
The battery drain is barely noticable. The app uses passive location services.

---
### Who made this and why?
This product was made by [Caspar von Wrede]('https://casparwre.de').
There are many location tracking services but I thought I could make the simplest one of all. 

Also, many of them do not come with their own easy way of viewing and sharing the recorded tracks.

---
{% endfilter %}
</div>
{% endblock %}  