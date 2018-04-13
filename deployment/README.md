## How to setup production

1. Install Apache and required modules `apt-get install apache2 libapache2-mod-wsgi-py3`
1. Generate SSH key `ssh-keygen -t rsa`
1. Add SSH key to GitHub
1. Place repo into `/var/www/pathbox.co`
1. Create venv if necessary
2. Place conf file `pathbox.co.conf into `/etc/apache2/sites-available/`
3. Run `a2ensite pathbox.co`
3. Enable Apache modules `a2enmod expires wsgi`
4. Restart Apache: `service apache2 reload`

**NOTE** Currently the virtualenv is not used. This must be configured in apache_conf.wsgi

### SSL
When using the Cloudflare flexible SSL, Apache must listening on port 80. 
This is because traffic between Cloudflare and the server is not encrypted!
