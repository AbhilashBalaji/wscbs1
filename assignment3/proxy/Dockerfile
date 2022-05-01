FROM nginx

# RUN  unlink /etc/nginx/sites-enabled/default.conf
COPY ./reverse-proxy.conf /etc/nginx/conf.d/reverse-proxy.conf
RUN mkdir -p  /etc/nginx/sites-enabled/ 
RUN  ln -s /etc/nginx/conf.d/reverse-proxy.conf  /etc/nginx/sites-enabled/reverse-proxy.conf
RUN  service nginx restart