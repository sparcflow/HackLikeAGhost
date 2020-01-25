FROM python:3.7-slim-stretch

RUN apt-get update && apt-get install -y git make gcc
RUN git clone https://github.com/byt3bl33d3r/SILENTTRINITY/ /root/st/
WORKDIR /root/st/
RUN python3 -m pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "teamserver.py", "0.0.0.0", "strongPasswordCantGuess"]