FROM python:3.8
WORKDIR .
COPY run.sh /
RUN chmod 755 /run.sh

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY decision_maker /decision_maker
ENTRYPOINT ["./run.sh"]