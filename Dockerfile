FROM python:3.6-slim

# Installing packages
RUN pip install pipenv gunicorn==19.8.1 meinheld==0.6.1

ADD app.py Pipfile* /app/

WORKDIR /app

RUN pipenv install --system --deploy

# the sources are copied as late as possible since they are likely to change often
ADD idunn /app/idunn

# set the multiprocess mode for gunicorn
ENV IDUNN_PROMETHEUS_MULTIPROC=1
ENV prometheus_multiproc_dir=/app/idunn/prometheus_multiproc
RUN mkdir /app/idunn/prometheus_multiproc

EXPOSE 5000

ADD gunicorn_logging.conf .
# You can set the number of workers by passing --workers=${NB_WORKER} to the docker run command.
# For some reason, an array is required here to accept other params on run.
ENTRYPOINT ["gunicorn", "app:app", "--bind=0.0.0.0:5000", "--pid=pid", \
  "--worker-class=meinheld.gmeinheld.MeinheldWorker", "--preload", "--log-config=/app/gunicorn_logging.conf"]
