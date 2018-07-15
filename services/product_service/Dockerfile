FROM python3.6.1-alphine
LABEL AUTHOR="Avik Sarkar <avik.sarkar@nutanix.com>"
COPY ./src /app
ENV DEBUG=TRUE
ENTRYPOINT ['python', '/app/app.py']