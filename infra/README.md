# C2 infrastructure using Terraform

Terraform is a tool that automates the creation and setup of resources on many Cloud providers. Check out the full docs and intro at (https://www.terraform.io/docs/index.html).  

## What does it do
This folder contains the C2 infrastructure described in How to Hack Like a Ghost:
- An front server running an Nginx container that redirects traffic to a backend server
- A backend system with a container running SILENTTRINITY (or Metasploit, Merlin, what have you)

If you follow the guide below, you will have a working setup in no time that you can clone and reproduce at will.
## Setup
1. Install Terraform:
```
wget https://releases.hashicorp.com/terraform/0.12.12/terraform_0.12.12_linux_amd64.zip
unzip terraform_0.12.12_linux_amd64.zip 
chmod +x terraform
```  
2. Setup AWS access keys with EC2 full permissions *(detailed walkthrough: http://bit.ly/2FzddLA)*

```
sudo apt install awscli
aws configure
[Enter access keys]
```  
   
3. Clone the current repo  
```
git clone https://github.com/HackLikeAPornstar/GreschPolitico
cd GreschPolitico/infra
```  
4. Edit the values in variables.tf to suit your needs:
   1. **adminIP** your IP to allow SSH into the machines  
   2. **C2Container** Name of the C2 container to run
   3. **certificateARN** *optional* ARN of the certificate if you route traffic through an ALB instead of Nginx 
   4. **domain** is the name of the domain name   
   5. **nginxContainer** Name of the Nginx container to run   
   6. **sshkey** Your public ssh key
   
5. Create your resources:
```
./terraform apply
...
output:
nginx_ip_address: xx.xxx.xx.xx
c2_ip_address: yy.yy.yyy.yy

``` 
6. Redirect the domain name to the Nginx IP on your DNS dashboard, wait 60 seconds for everything to get setup and enjoy!  


## Usage

The servers run the two containers defined in ../containers. Check their Readme files to know how they operate.  
Briefly: the Nginx container serves decoy pages from www folder.   
It redirects URLs starting with "/st" and and "/msf" to the backend C2 containers on ports (5080 and 9910).  
Make sure to use these settings when configuring your listener.

More info on SILENTTRINITY, see https://github.com/byt3bl33d3r/SILENTTRINITY )*  

In this setup you can quickly to the backend connect using:
```
python3.7 st.py wss://username:password@yy.yy.yyy.yy:5000
``` 
## Using an ALB to route traffic
If you wish to use an AWS ALB to route traffic to C2, renambe "alb.tf.disabled" to "alb.tf". Configure a certificate on [AWS ACM](https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html), and put its value in variables.tf/certificateARN.  

Using an ALB makes it easier to add new routes to new listeners, as opposed to an Nginx server that would need to be restarted every time.  
In this scenario, the Nginx server would only be used to serve decoy pages.

## Customization
Change the values in variables.tf to suit your needs. The scripts folder contains instructions running at the boot of the machine. You can edit it to start any container you wish.  
They get injected in the main.tf file in the user-data section of EC2 resources.

## TODO
- Register a zone using route53
- generate a certificate using ACM

# Credits
- byt3bl33d3r for SILENTTRINITY: https://github.com/byt3bl33d3r/SILENTTRINITY
- staticfloat for the automated Nginx setup: https://github.com/staticfloat/docker-nginx-certbot 