# Introduction

Here is the graph task-dependency implemented in Airflow
![alt text](https://user-images.githubusercontent.com/22119606/107688524-06d72280-6ca8-11eb-8c41-91d344101eee.jpg)

# Project set up

The project requires docker and docker-compose installed

Installation
``` bash
	$ make init_docker
        $ docker-compose up -d
```

To manually trigger the pipeline::

```bash
	$ make run_dag
```
To retrieve the output.json file ::

```bash
	$ make get_final_output
```


## TO DO List

* Unit test
	* function testing
	* Workflow testing
* CI/CD
	* Build versioned docker image with python package
	* Update Airflow DAG on server

These two tasks are paramount to 
