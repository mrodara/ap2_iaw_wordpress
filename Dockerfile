FROM php:8.4-apache

ARG WORDPRESS_VERSION=7.1.4

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl ca-certificates libfreetype6-dev libicu-dev libjpeg62-turbo-dev \
       libpng-dev libwebp-dev libzip-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg --with-webp \
    && docker-php-ext-install -j"$(nproc)" exif gd intl mysqli zip \
    && rm -rf /var/lib/apt/lists/*

COPY src/wordpress/ /var/www/html/

RUN chown -R root:root /var/www/html \
    && find /var/www/html -type d -exec chmod 755 {} \; \
    && find /var/www/html -type f -exec chmod 644 {} \; \
    && chown -R www-data:www-data /var/www/html/wp-content

COPY config/wp-config.php /var/www/html/wp-config.php
COPY apache/001-wordpress.conf /etc/apache2/sites-available/001-wordpress.conf

RUN chown root:www-data /var/www/html/wp-config.php \
    && chmod 640 /var/www/html/wp-config.php \
    && a2enmod rewrite \
    && a2ensite 001-wordpress.conf \
    && a2dissite 000-default.conf \
    && apache2ctl configtest

EXPOSE 80

CMD ["apache2-foreground"]