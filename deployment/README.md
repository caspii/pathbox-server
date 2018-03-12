## How to setup production

1. Place repo into `/var/www/loc.b3rlin.net`
1. Create venv if necessary
2. Place conf file `loc.b3rlin.net.conf into `/etc/apache2/sites-available/`
3. Run `a2ensite loc.b3rlin.net`
4. Restart Apache: `service apache2 reload
