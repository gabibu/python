
FROM python:3.8

ARG URL
ARG DEPTH

RUN echo $URL
RUN echo $DEPTH


#RUN pip install Flask==2.2.2 uWSGI==2.0.21
WORKDIR .

COPY run.sh /
RUN chmod 755 /run.sh

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY data_collector /data_collector
#COPY main.py /data_collector

#CMD ["python3" , "-m", "data_collector.main", "--url", "$URL", "depth", "$DEPTH"]
ENTRYPOINT ["./run.sh"]