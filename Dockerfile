FROM apache/airflow:2.0.1
USER root
RUN apt update && apt install -y git && apt-get install -y build-essential
USER airflow
RUN curl https://pyenv.run | bash
RUN echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc && echo 'eval "$(pyenv init -)"' >> ~/.bashrc && echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
RUN pyenv install -v 3.8.0
# RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
