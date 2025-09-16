Catnip API + Web

## Description

This is a deliverable for the following challenge:

### Objective

Your objective is to build an API for a fake financial institution using a language of your choice, you may use an API framework of your choice if you’d like.

### Brief

While modern banks have evolved to serve a plethora of functions, at their core, banks must provide certain basic features. Today, your task is to build the basic API for one of those banks! Imagine you are designing an administrative application for bank employees.
You should build a backend API that ultimately be consumed by multiple frontends (web, iOS, Android etc). Please avoid using AI during this assessment.

### Tasks

There should be API routes that allows them to:

- Create a new bank account with an initial deposit amount. A single customer may have multiple bank accounts.
- Transfer amounts between any two accounts, including those owned by different customers.
- Retrieve balances for a given account.
- Retrieve transfer history for a given account.
- There is no need to implement authentication
- Account balances must never be negative.

### Extra Credit

Build a basic webapp using this API where an admin can create accounts and transfer money between them.

## Resolution

### Database

I've chosen [PostgreSQL](https://www.postgresql.org) as the database. No special reason, I'm just used to it and it's robust.

### API

I'm used to work in Node.js/Deno runtimes for APIs, but since the position requires Python, I've chosen to use:

- [FastAPI](https://fastapi.tiangolo.com) for the API framework.
- [SQLModel](https://sqlmodel.tiangolo.com) for the ORM

### Frontend

For frontend I will use [React](https://react.dev) with [TypeScript](https://www.typescriptlang.org), but I don't have a framework decided yet, nor the UI Library. Probably a static (no backend) version with Vite and something like [shadcn/ui](https://ui.shadcn.com) or [Reshaped](https://reshaped.so) for the UI.

## Environment

I've created a Docker Compose environment to easily run the project. In order to run it you should:

- Have [Docker](http://docker.com) installed and running in your environment.
- Copy the [.env.example](./.env.example) file in the root folder as `.env` and adapt to your needs.
- run `docker compose up -d`

You should be able to open:

- A test frontend app on [http://localhost:5173](http://localhost:5173)
- API Swagger docs on [http://localhost:8000/docs](http://localhost:8000/docs)

### Development

In order to work with the API itself, you should have the database running first, so run the following command on the root folder:

```
docker compose up catnip-db -d
```

then `cd` into the `./api` folder and setup the environment with:

```
make venv
```

to create the virtual environment and install dependencies.
Feel free to use [Alembic](https://alembic.sqlalchemy.org) if you update the database models to create the migrations.
