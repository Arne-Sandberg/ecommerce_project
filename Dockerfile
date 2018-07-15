FROM python:2.7.13-alpine
LABEL AUTHOR="Avik Sarkar <avik.sarkar@nutanix.com>"
COPY ./src /usr/src
CMD [ "python", "/usr/src/app.py" ]
