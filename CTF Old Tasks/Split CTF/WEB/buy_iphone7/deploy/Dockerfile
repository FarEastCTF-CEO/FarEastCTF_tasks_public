FROM richarvey/nginx-php-fpm
HEALTHCHECK CMD curl --fail 127.0.0.1 || exit 1
ADD ./static/ /var/www/html/
EXPOSE 80
