FROM staticfloat/nginx-certbot

COPY *.conf /etc/nginx/conf.d/
COPY html/* /var/www/html/
RUN chown -R www-data:www-data /var/www

COPY init.sh /scripts/

ENV DOMAIN="www.customdomain.com"
ENV C2IP="192.168.1.29"
ENV CERTBOT_EMAIL="whateveremail@gmail.com"

CMD ["/bin/bash", "/scripts/init.sh"]