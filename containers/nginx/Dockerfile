FROM staticfloat/nginx-certbot

COPY *.conf /etc/nginx/conf.d/
COPY --chown=www-data:www-data html/* /var/www/html/

COPY init.sh /scripts/

ENV DOMAIN="www.customdomain.com"
ENV C2IP="192.168.1.29"
ENV CERTBOT_EMAIL="whateveremail@gmail.com"

CMD ["/bin/bash", "/scripts/init.sh"]