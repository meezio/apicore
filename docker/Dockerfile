FROM debian:stretch

# Set UTF8 locale
ARG locale=fr_FR.UTF8
RUN apt-get update && \
    apt-get install -y locales && \
    echo ${locale}' UTF-8' >> /etc/locale.gen && \
    locale-gen && \
    /usr/sbin/update-locale LANG=$locale
ENV LANG $locale

RUN apt-get -y install ca-certificates uwsgi-core uwsgi-plugin-python3 build-essential python3-dev python3-pip

# Install app files
ENV HOME /opt/api
WORKDIR /opt/api
RUN pip3 install --no-cache-dir apicore

# Setup directories
RUN mkdir /var/data && chown -R www-data:www-data /var/data
VOLUME ["/var/data"]
EXPOSE 80
ENTRYPOINT ["uwsgi", "--http-socket", "0.0.0.0:80", "--uid", "www-data", "--gid", "www-data", "--master", "--plugins", "python3", "--module", "main:api"]
CMD ["--processes", "4", "--threads", "8"]
