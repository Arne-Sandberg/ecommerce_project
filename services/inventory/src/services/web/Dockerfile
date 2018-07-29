FROM alpine
# Install all debian packages
COPY ./requirements.txt /app/
RUN apk add --no-cache python3-dev build-base linux-headers pcre-dev &&\
    wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py &&\
    wget https://bootstrap.pypa.io/get-pip.py &&\
    python3 virtualenv.py /venv/ --no-pip --no-wheel --no-setuptools &&\
    source /venv/bin/activate &&\
    python get-pip.py &&\
    pip install -r /app/requirements.txt &&\
    rm -rf /var/cache/apk/*

COPY . /app/web
RUN mkdir /var/log/uwsgi
# Forward uwsgi logs to the docker log collector
RUN ln -sf /dev/stdout /var/log/uwsgi/web.log \
    && ln -sf /dev/stdout /var/log/uwsgi/emperor.log
ENV PATH /venv/bin:$PATH
ENV PYTHONPATH /app/web
EXPOSE 80
CMD ["uwsgi", "--emperor", "/app/web", "--logto", "/var/log/uwsgi/emperor.log"]
