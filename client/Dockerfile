FROM python:latest

COPY ./ /home/CNG
COPY ./entryPoint.sh /home/CNG

RUN chmod +x /home/CNG/entryPoint.sh
ENTRYPOINT [ "/home/CNG/entryPoint.sh" ]