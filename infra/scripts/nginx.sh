curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt update
apt install -y docker-ce
docker run -dti -p80:80 -p443:443 \
-e DOMAIN="$DOMAIN" \
-e C2IP="$C2IP" \
-e CERTBOT_EMAIL="anyemail@gmail.com" \
-v /opt/letsencrypt:/etc/letsencrypt \
"$CONTAINER"