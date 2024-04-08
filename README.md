# Tech Spec

This is a REST API to store, retrieve and search natural language documents. It uses Elasticsearch as persistence layer.
The endpoints exposed are the following

### POST /store

#### Request body

Using `application/json` as content type

```json
{
  "text": "this is a test document"
}
```

#### Response

On success `200` with body

```json
{
  "document_id": "abc"
}
```

### GET /retrieve/{document_id}

#### Response

On success `200` with the id matching content

```json
{
  "text": "this is a test document"
}
```

### POST /search

#### Request body

Using `application/json` as content type

```json
{
  "text": "content to match against",
  "number_of_results": 12
}
```

#### Response

On success `200` with a list of matching documents and their scores in JSON

```json
[
  {
    "document": "foo",
    "score": 12
  },
  {
    "document": "bar",
    "score": 4
  }
]
```

On top of that it exposes an endpoint where the user can query information from an LLM instead of
searching in the persistence layer.

### POST /ask

#### Request body

Using `application/json` as content type

```json
{
  "message": "What is the capital of Greece?"
}
```

#### Response

On success `200` with the response body

```json
{
  "reply": "the capital of Greece is Athens"
}
```

For detailed information about the logs you can navigate to `localhost:8000/docs`

# Run the code

## Using Docker and docker-compose

The easiest way to run the code is to run to use the `docker-compose.yml`. This requires a working installation of
Docker and `docker-compose`. After you make sure that both requirements are fulfilled, you can use the `start_up.sh` and
`clean_up.sh` scripts for both starting the stopping the environment.

Give the environment some time to load or check the logs.

## Manually

1. Pull and run the Elasticsearch container

```bash
docker network create elastic
docker run -d --rm --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" elasticsearch:8.12.2
docker build -t natural_language_search . 
```

2. Start the search API's uvicorn server

```bash
uvicorn router:natural_language_search --reload
```

# Testing

There are limited unit tests in the project for testing the Elasticsearch repository. There are no
unit tests on the level of the API (fastAPI provides tools that do this out-of-the-box) or testing the
LLM. These should be added on a later iteration.

