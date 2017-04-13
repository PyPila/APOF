FROM python:2.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /run/service
ADD . /run/service
WORKDIR /run/service

RUN pip install -U pip
RUN pip install -I -e .[develop] --process-dependency-links

WORKDIR /run/service/src/apof
ENTRYPOINT ["apofcmd"]
CMD ["django","runserver","0.0.0.0:8000"]
