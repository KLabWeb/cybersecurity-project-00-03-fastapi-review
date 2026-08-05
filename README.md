# Phase 0: FastAPI Review - Official Docs Refresher API

This is the app I am building as I read and work through the remainder of the [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) I did not complete while at my previous full-stack software engineer role as a refresher and wrap-up.

This is a big work-in-progress, and the app itself changes a lot as I go — models get reworked, files get split up, and endpoints come and go with each new chapter. This README thus tracks the tutorial and what it teaches, rather than whatever my code happens to look like at any given chapter.

The API is live on Digital Ocean, which re-deploys each time I push an update to this GitHub repo. Play around with via the interactive [OpenAPI Swagger docs](https://cyb-project-00-03-fastapi-app-3qxik.ondigitalocean.app/docs) for it.

See the notes I am taking while completing the official docs [here](https://github.com/KLabWeb/cybersecurity-notes/blob/main/Phase%2000/00-03%20FastAPI%20Notes.pdf). New notes start from section "04. Request Body" and onwards. I also updated the old notes with up-to-date info in places where the tutorial was updated.

## Tutorial Progress

Currently done through **section 19: Response Status Code**. Checked = done. Sections completed = 24 / 43 = 55.8%

### Prereqs
Basic python review for types and concurrency
- [x] [Python Types](https://fastapi.tiangolo.com/python-types/)
- [x] [Concurrency and async / await](https://fastapi.tiangolo.com/async/)

### Request handling basics
The core of it — defining endpoints and pulling data in from the path, the query string, and the request body, with validation on all of it.
- [x] [First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [x] [Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/)
- [x] [Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [x] [Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [x] [Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/)
- [x] [Path Parameters and Numeric Validations](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/)

### Parameters and request models
Grouping params into models, and pulling data out of cookies and headers instead of just the path and query.
- [x] [Query Parameter Models](https://fastapi.tiangolo.com/tutorial/query-param-models/)
- [x] [Body - Multiple Parameters](https://fastapi.tiangolo.com/tutorial/body-multiple-params/)
- [x] [Body - Fields](https://fastapi.tiangolo.com/tutorial/body-fields/)
- [x] [Body - Nested Models](https://fastapi.tiangolo.com/tutorial/body-nested-models/)
- [x] [Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/)
- [x] [Extra Data Types](https://fastapi.tiangolo.com/tutorial/extra-data-types/)
- [x] [Cookie Parameters](https://fastapi.tiangolo.com/tutorial/cookie-params/)
- [x] [Header Parameters](https://fastapi.tiangolo.com/tutorial/header-params/)
- [x] [Cookie Parameter Models](https://fastapi.tiangolo.com/tutorial/cookie-param-models/)
- [x] [Header Parameter Models](https://fastapi.tiangolo.com/tutorial/header-param-models/)

### Responses
Controlling what goes back out — the response shape, extra models, and status codes.
- [x] [Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/)
- [x] [Extra Models](https://fastapi.tiangolo.com/tutorial/extra-models/)
- [x] [Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/)

### Forms and files
Handling form submissions and file uploads instead of JSON bodies.
- [x] [Form Data](https://fastapi.tiangolo.com/tutorial/request-forms/)
- [x] [Form Models](https://fastapi.tiangolo.com/tutorial/request-form-models/)
- [x] [Request Files](https://fastapi.tiangolo.com/tutorial/request-files/)
- [x] [Request Forms and Files](https://fastapi.tiangolo.com/tutorial/request-forms-and-files/)

### Errors and configuration
Returning proper errors, configuring endpoints, encoding data, and doing partial updates.
- [x] [Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [ ] [Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)
- [ ] [JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/)
- [ ] [Body - Updates](https://fastapi.tiangolo.com/tutorial/body-updates/)

### Dependencies
FastAPI's dependency injection — the thing auth and a lot of shared logic get built on top of. One of the sections I actually care about for AppSec.
- [ ] [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) *(+ Classes as Dependencies, Sub-dependencies, Dependencies in path operation decorators, Global Dependencies, Dependencies with yield)*

### Security
Auth from the ground up, through OAuth2 with password hashing and JWT tokens. This is the big one for me, and the foundation for the JWT work later in the study plan.
- [ ] [Security](https://fastapi.tiangolo.com/tutorial/security/) *(+ Security First Steps, Get Current User, Simple OAuth2 with Password and Bearer, OAuth2 with Password and hashing / JWT tokens)*

### Middleware, CORS, and databases
The cross-cutting stuff that matters most once an API is real — middleware, CORS policy, and wiring in a SQL database.
- [ ] [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [ ] [CORS (Cross-Origin Resource Sharing)](https://fastapi.tiangolo.com/tutorial/cors/)
- [ ] [SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)

### Bigger apps and the rest
Splitting into multiple files, streaming, background tasks, docs metadata, static files, testing, and debugging.
- [ ] [Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [ ] [Stream JSON Lines](https://fastapi.tiangolo.com/tutorial/stream-json-lines/)
- [ ] [Server-Sent Events (SSE)](https://fastapi.tiangolo.com/tutorial/server-sent-events/)
- [ ] [Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [ ] [Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/)
- [ ] [Frontend](https://fastapi.tiangolo.com/tutorial/frontend/)
- [ ] [Static Files](https://fastapi.tiangolo.com/tutorial/static-files/)
- [ ] [Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [ ] [Debugging](https://fastapi.tiangolo.com/tutorial/debugging/)

## Running the API Locally

The app is containerized with a modified config from my [Docker review project](https://github.com/KLabWeb/cybersecurity-project-00-04-docker-review) — Uvicorn behind a Dockerfile, and a Compose file with live-reload — so `docker compose up` runs the app, with the interactive Swagger docs at `/docs` to try out every endpoint I've built so far.

## Related

- [Portfolio](https://github.com/KLabWeb/cybersecurity-portfolio) — the work I am doing from what I am learning
- [Study Plan](https://github.com/KLabWeb/cybersecurity-study-plan) — the full curriculum
- [Study Notes](https://github.com/KLabWeb/cybersecurity-notes) — what I'm learning as I work through it
- [Study Tracker](https://github.com/KLabWeb/cybersecurity-study-tracker) — what I'm doing, for how long, and when
