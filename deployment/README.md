## How to setup production

1. Install Apache and required modules `apt-get install apache2 libapache2-mod-wsgi-py3`
1. Generate SSH key `ssh-keygen -t rsa`
1. Add SSH key to GitHub
1. Place repo into `/var/www/loc.b3rlin.net`
1. Create venv if necessary
2. Place conf file `loc.b3rlin.net.conf into `/etc/apache2/sites-available/`
3. Run `a2ensite loc.b3rlin.net`
3. Enable Apache modules `a2enmod expires wsgi`
4. Restart Apache: `service apache2 reload`

**NOTE** Currently the virtualenv is not used. This must be configured in apache_conf.wsgi
