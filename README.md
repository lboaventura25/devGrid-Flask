# Technical Challenge
This repository is dedicated to backend technical challenge from DevGrid.

This is a simple flask api with two endpoints:

> - /api/weather?max_number=<max_number>
> - METHOD: GET

Get all cached cities, up to the latest n entries (configurable) or max_number (if especified).

---

> - /api/weather/<city_name>
> - METHOD: GET

Get all cached cities, up to the latest n entries (configurable) or max_number (if especified).

## Specifications

This API using python3 and Flask, and have a external connection with [Open Weather API](https://openweathermap.org/api).

## Run

### Flask

### Build

```bash
$ docker-compose build
```

### Run api

```bash
$ docker-compose up
```

### Pytest / Coverage

#### To run tests

```bash
$ docker-compose run api coverage run -m pytest
```

#### To report results with Coverage

```bash
$ docker-compose run api coverage report -m
```

