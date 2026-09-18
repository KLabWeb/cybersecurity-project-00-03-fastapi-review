# Phase 0: FastAPI Review - Official Docs Refresher API

I built this app while working through the remainder of the [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) that I had not completed during my previous full-stack software engineer role, as a refresher and a wrap-up of that work.

This app was a big work-in-progress, based on the docs, which taught via a "teach the concept, not best practices" manner for most of the material — as such, throughout the project, models got reworked, files got split up, and endpoints came and went with each new chapter. This README tracks the tutorial and what I learned from it, through the code that I built along the way, as seen via this FastAPI REST API.

Note, that some security violations have intentionally been left in this app, as this app will serve as a testing ground for later phase work. There are deliberate inconsistencies here: scopes enforced on some routes and ignored on others, a mix of legacy hardcoded and SQL data, dependencies here but not there, and so forth, but the goal of building this app was never to have a proper production ready API, but rather one that I slowly built on itself and improved in parts as I worked through the official FastAPI docs, as a teaching application.

This API is live on Digital Ocean. Play around with via the interactive [OpenAPI Swagger docs](https://cyb-project-00-03-fastapi-app-3qxik.ondigitalocean.app/docs) for it.

Also, see the notes I took while completing the official docs [here](https://github.com/KLabWeb/cybersecurity-notes/blob/main/Phase%2000/00-03%20FastAPI%20Notes.pdf).

## Design for this Project
Concepts implemented in this API are built from what the official FastAPI docs tutorial teaches. Unlike the official docs, though, I designed this API using strict Domain-Driven Design principles and layers.

```
.
├── data                          the data stores themselves, not commited
│   ├── legacy                      raw in-memory data (item, purchase, user, wishlist)
│   └── sqlite                      database.db, supplied at runtime by the compose volume
│
└── src
    ├── app.py                    creates the app's FastAPI instance
    ├── main.py                   entry point; wires the app via include_router and route imports
    ├── models                    domain objects (Item, User, Purchase, ...), and their exceptions
    │
    ├── api                       the HTTP layer
    │   ├── models                  request and response Data Transfer Objects
    │   ├── routes                  client-facing endpoints and `@app.exception_handler`
    │   └── dependencies            reusable `Depends` shared across routes (headers, debug)
    │
    ├── repository                owns all access to data; no other layer touches a store
    │   ├── __init__.py             init_storage(), the single entry point for storage setup
    │   ├── legacy                  CRUD access methods for legacy store w/ translations to domain
    │   └── sql                     CRUD access methods for SQLite store via SQLModel w/ translations to domain
    │       ├── db                    engine, session factory, and the SQL_SESSION dependency
    │       └── models                table models, translation layer, and the CRUD functions
    │
    ├── security
    │   ├── hashing.py              password hashing (isolated from business logic)
    │   └── auth                    auth, token schemes (jwt, legacy), and role verification
    │
    └── middleware                cross-cutting request/response work (process time, CORS)
```

Each layer owns its own models, data access and manipulation, data interpretation, and interface. Each layer aims to be a black box internally, and business objects define the API.

## Running the API Locally

The app is containerized with a modified config from my [Docker review project](https://github.com/KLabWeb/cybersecurity-project-00-04-docker-review) — Uvicorn behind a Dockerfile, and a Compose file with live-reload — so `docker compose up` runs the app, with the interactive Swagger docs at `/docs` to try out every endpoint I've built so far.

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
- [x] [Path Operation Configuration](https://fastapi.tiangolo.com/tutorial/path-operation-configuration/)
- [x] [JSON Compatible Encoder](https://fastapi.tiangolo.com/tutorial/encoder/)
- [x] [Body - Updates](https://fastapi.tiangolo.com/tutorial/body-updates/)

### Dependencies
FastAPI's dependency injection — the thing auth and a lot of shared logic get built on top of. One of the sections I actually care about for AppSec.
- [x] [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [x] [Classes as Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/)
- [x] [Sub-dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/)
- [x] [Dependencies in path operation decorators](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)
- [x] [Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/)
- [x] [Dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)

### Security
Auth from the ground up, through OAuth2 with password hashing and JWT tokens. This is the big one for me, and the foundation for the JWT work later in the study plan.
- [x] [Security](https://fastapi.tiangolo.com/tutorial/security/)
- [x] [Security - First Steps](https://fastapi.tiangolo.com/tutorial/security/first-steps/)
- [x] [Get Current User](https://fastapi.tiangolo.com/tutorial/security/get-current-user/)
- [x] [Simple OAuth2 with Password and Bearer](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/)
- [x] [OAuth2 with Password (and hashing), Bearer with JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)

### Middleware, CORS, and databases
The cross-cutting stuff that matters most once an API is real — middleware, CORS policy, and wiring in a SQL database.
- [x] [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [x] [CORS (Cross-Origin Resource Sharing)](https://fastapi.tiangolo.com/tutorial/cors/)
- [x] [SQL (Relational) Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)

### Bigger apps and the rest
Splitting into multiple files, testing, and debugging.
- [x] [Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [x] [Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [x] [Debugging](https://fastapi.tiangolo.com/tutorial/debugging/)

### Advanced User Guide
The docs' separate Advanced guide (the docs themselves note these are "not necessarily advanced").
- [x] [Response Cookies](https://fastapi.tiangolo.com/advanced/response-cookies/)
- [x] [Response Headers](https://fastapi.tiangolo.com/advanced/response-headers/)
- [x] [Advanced Dependencies](https://fastapi.tiangolo.com/advanced/advanced-dependencies/)
- [x] [Advanced Security - OAuth2 scopes](https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/)
- [x] [Behind a Proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/)
- [x] [Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [x] [Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)
- [x] [Strict Content-Type Checking](https://fastapi.tiangolo.com/advanced/strict-content-type/)

## Related

- [Portfolio](https://github.com/KLabWeb/cybersecurity-portfolio) — the work I am doing from what I am learning
- [Study Plan](https://github.com/KLabWeb/cybersecurity-study-plan) — the full curriculum
- [Study Notes](https://github.com/KLabWeb/cybersecurity-notes) — what I'm learning as I work through it
- [Study Tracker](https://github.com/KLabWeb/cybersecurity-study-tracker) — what I'm doing, for how long, and when
