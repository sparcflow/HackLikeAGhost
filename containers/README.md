# Containers in attacking infrastructure

These are the descrition of the containers featured in How to Hack Like a Ghost

## Nginx
### Intro
The Nginx containers starts off with a base image from staticfloat (https://github.com/staticfloat/docker-nginx-certbot) that sets up a Nginx server with Certbot setup.  

We copy the Nginx config file that has three routes:
- default route serving pages from the www directory
- /st route that forwards request to an HTTPs listner on port 5080 on another machine
- /msf route that forwards request to an HTTPs listner on port 9910 on another machine

We copy the init.sh script that replaces updates the config file with the environment variables: $C2IP and $DOMAIN both of which should be set up when launching the container.  
It then runs the /scripts/entrypoint.sh script present in the default staticfloat image.


### Usage
Register a domain and point it to the host that will run this container.
```
docker build . -name nginx
docker run -d -p80:80 -p443:443 \
-e DOMAIN="www.customdomain.com" \
-e C2IP="xx.xx.xx.xx" \
-e CERTBOT_EMAIL="anyemail@gmail.com" \
-v /opt/letsencrypt:/etc/letsencrypt \
```
## SILENTTRINITY
### Usage
```
docker build . -name silent
docker run -d --net=host  -v /opt/st:/root/st/data silent
```
Next you can connect to the Team server on port 5000 (need to download the st.py file from SILENTTRINITY repo)
```
python3.7 st.py wss://username:strongPasswordCantGuess@yy.yy.yyy.yy:5000
``` 