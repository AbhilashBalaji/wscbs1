FROM nginx:alpine

# RUN  unlink /etc/nginx/sites-enabled/default.conf
RUN rm -rf /etc/nginx/conf.d/ 
COPY ./reverse-proxy.conf /etc/nginx/conf.d/reverse-proxy.conf
RUN mkdir -p  /etc/nginx/sites-enabled/ 
RUN  ln -s /etc/nginx/conf.d/reverse-proxy.conf  /etc/nginx/sites-enabled/reverse-proxy.conf
# RUN  service nginx restart
EXPOSE 80
ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]