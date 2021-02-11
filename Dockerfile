FROM apache/airflow:2.0.1
USER airflow
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN mkdir /home/airflow/project
COPY --chown=airflow:airflow . /home/airflow/project/
RUN cd /home/airflow/project &&\
    source /home/airflow/.poetry/env &&\
    poetry build &&\
    find dist -name '*.whl' -exec pip install --upgrade {} \;

