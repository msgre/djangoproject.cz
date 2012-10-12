#!/usr/local/bin/bash
export PYTHONPATH="/home/michal/projects/www/djangoproject.cz/django_src"
# spustime skript, vytahneme dynamicka data z externich webu
/usr/local/bin/python /home/michal/projects/www/djangoproject.cz/djcz/fetcher/fetcher.py $@ > /home/michal/projects/www/djangoproject.cz/cache/fetcher/$@.temp.html
# pokud se neco vycetlo (je to vetsi nez 20 bytu), prejmenuju temp na html
ls -l /home/michal/projects/www/djangoproject.cz/cache/fetcher/$@.temp.html | awk '{print $5}' > thesize
if [ `cat thesize` -gt 20 ]
	then
	mv /home/michal/projects/www/djangoproject.cz/cache/fetcher/$@.temp.html /home/michal/projects/www/djangoproject.cz/cache/fetcher/$@.html
	exit 0
	fi
