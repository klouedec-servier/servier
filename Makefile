install: 
	poetry build
	find dist -name '*.whl' -exec pip install --upgrade {} \;

build:
	docker build -t glahlou/servier:latest .

init_docker: build
	mkdir -p logs
	mkdir -p plugins
	echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
	docker-compose up airflow-init

run_dag:
	docker-compose run airflow-worker airflow dags trigger my_dag

test:
	pytest tests
