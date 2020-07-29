FROM nginx
EXPOSE 80 8000 8080
RUN rm -rf /etc/nginx/conf.d/*.conf
ADD nginx.conf /etc/nginx/
RUN mkdir -p /usr/share/nginx/html/static
