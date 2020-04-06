FROM nginx:latest
RUN rm /etc/nginx/conf.d/default.conf
COPY sites-enabled /etc/nginx/conf.d
RUN pip install -r requirements.txt
# RUN mkdir /etc/nginx/ssl
# COPY ssl/ /etc/nginx/ssl/