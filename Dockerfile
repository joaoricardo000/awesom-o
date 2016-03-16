FROM ubuntu:14.04

MAINTAINER Joao Ricardo "joaoricardo000@gmail.com"

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y python2.7 python-dev python-pip python-virtualenv &&\
	apt-get install -y libfontconfig libjpeg-dev zlib1g-dev &&\
	apt-get install -y git curl supervisor espeak

RUN curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash - &&\
	apt-get install -y nodejs

RUN npm -g install pageres-cli

COPY src/ /awesomo
COPY opt/requirements.pip /requirements.pip
COPY opt/supervisor.conf /etc/supervisor/conf.d
COPY opt/patch.sh /patch.sh

RUN virtualenv venv && /./venv/bin/pip install -r requirements.pip

RUN chmod +x /patch.sh 
RUN /./patch.sh

ENV WHATSAPP_LOGIN=""
ENV WHATSAPP_PW=""
ENV BING_API_KEY=""
ENV WHATSAPP_ADMIN=""

EXPOSE 9005

RUN touch /var/log/whatsapp-bot.log
CMD ["/usr/bin/supervisord"]