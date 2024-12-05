FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d

# Copy SSL certificates into the container
COPY /etc/letsencrypt/live/api.diplomaroad.pro /etc/letsencrypt/live/api.diplomaroad.pro
