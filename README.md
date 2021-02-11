# Introduction
The objective of this project is to build a Data Pipeline on drug mentions in scientific articles.

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

# Important architecture choices

## Trie data structure to search drugs in corpus of journals

See [wikipedia](https://en.wikipedia.org/wiki/Trie) for more details. 

Advantages:
* Fast Lookup 0(1)
* light storage

## Final json output

Here is an extract of the final json output

```json
    {
        "Journal of emergency nursing": {
            "pubmed": [
                [
                    "1",
                    "A04AD",
                    "2019-01-01"
                ],
                [
                    "2",
                    "A04AD",
                    "2019-01-01"
                ]
            ],
            "clinical_trial": [
                [
                    "NCT04189588",
                    "A04AD",
                    "2020-01-01"
                ],
                [
                    "NCT01967433",
                    "A04AD",
                    "2020-01-01"
                ],
                [
                    "NCT04237091",
                    "A04AD",
                    "2020-01-01"
                ],
                [
                    "NCT04188184",
                    "A01AD",
                    "2020-04-27"
                ]
            ]
        },
        ...
    }

```
I chose this json for several reasons:

* Very light. Journal's title and drug full name are not stored into the json.
  Only their ids.
* Considering the only task at hand (Find the journal with most drugs mention),
  this schema (journal as first keys instead of drugs) allows to answer the question
  without reversing the json.


# TO DO List

## Next steps
Among other things, here is the very next things to do:


* Unit test
	* function testing
	* Workflow testing
* CI/CD
	* Build versioned docker image with python package
	* Update Airflow DAG on server

These two tasks are paramount to 
