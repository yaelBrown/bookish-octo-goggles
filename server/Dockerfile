FROM python:latest

COPY ./api/ /home/CNG
COPY ./entryPoint.sh /home/CNG

EXPOSE 5000
RUN chmod +x /home/CNG/entryPoint.sh
ENTRYPOINT [ "/home/CNG/entryPoint.sh" ]