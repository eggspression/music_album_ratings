# Music Album Ratings API

A REST API built with FastAPI for browsing music albums, viewing artists and track listings, writing album reviews, and saving albums to a personal collection. The project uses PostgreSQL for persistence, SQLAlchemy for ORM modeling, and JWT bearer authentication for protected routes.

This project was built as an API-first backend service with a clean layered structure: routes handle HTTP concerns, services contain business logic, schemas define request and response models, and SQLAlchemy models map the relational database.

## Features

- User registration and login with JWT authentication
- Browse albums with search, filtering, sorting, and pagination controls
- View detailed album information
- View album statistics such as average rating, review count, and save count
- View track listings for individual albums
- Create, update, and delete album reviews
- Save and unsave albums
- Browse artists and view the albums associated with each artist
- View the current user's saved albums and submitted reviews
- Interactive API documentation via Swagger UI and ReDoc

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- JWT authentication
- Passlib / bcrypt

## Project Structure

```text
music_album_ratings/
  backend/
    app/
      main.py          # FastAPI application entry point
      database.py      # SQLAlchemy engine, session, and base setup
      security.py      # JWT auth helpers and current-user dependency
      config.py        # Environment variable loading
      schemas.py       # Pydantic request and response schemas
      models/          # SQLAlchemy ORM models
      routes/          # API route definitions
      services/        # Business logic and database queries
  frontend/            # Reserved for future frontend work
  .env.example         # Example environment variables
  README.md
```

## Architecture Overview

The backend follows a simple layered design:

- `routes/` defines HTTP endpoints and response models
- `services/` contains database queries and business logic
- `models/` defines the relational data model with SQLAlchemy
- `schemas.py` defines request validation and response serialization
- `security.py` handles password hashing, token creation, and protected-route authentication

This separation keeps the API easier to maintain and makes features easier to extend without mixing HTTP code and database logic.

## Relational Database Schema

The API is backed by a PostgreSQL relational database with six main tables:

### Tables

- `users`
  - stores account information for registered users
  - unique fields: `username`, `email`
- `artists`
  - stores artist information such as name, bio, and image URL
- `albums`
  - stores album metadata and links each album to an artist
  - unique constraint on `(title, artist_id)`
- `reviews`
  - stores a user's rating and optional comment for an album
  - unique constraint on `(user_id, album_id)`
  - check constraint enforcing ratings from `1` to `10`
- `saved_albums`
  - join table for a user's saved albums
  - composite primary key on `(user_id, album_id)`
- `tracks`
  - stores track listings for albums

### Relationships

- One `artist` can have many `albums`
- One `album` belongs to one `artist`
- One `user` can write many `reviews`
- One `album` can have many `reviews`
- One `user` can save many `albums` through `saved_albums`
- One `album` can be saved by many `users` through `saved_albums`
- One `album` can have many `tracks`

### Schema Summary

```text
users (1) -----< reviews >----- (1) albums
users (1) ---< saved_albums >--- (1) albums
artists (1) --------------------< albums
albums (1) ---------------------< tracks
```

## Authentication

Protected endpoints use JWT bearer authentication.

Authentication flow:

1. Register a user with `POST /auth/register`
2. Log in with `POST /auth/login`
3. Copy the returned access token
4. Click `Authorize` in Swagger UI
5. Send the token as `Bearer <token>` for protected routes

Protected routes include:

- creating album reviews
- updating reviews
- deleting reviews
- saving albums
- unsaving albums
- viewing current-user review history
- viewing current-user saved albums

## Main Endpoints

### Root

- `GET /`

### Auth

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Albums

- `GET /albums`
- `GET /albums/{album_id}`
- `GET /albums/{album_id}/stats`
- `GET /albums/{album_id}/tracks`
- `GET /albums/{album_id}/reviews`
- `POST /albums/{album_id}/reviews`
- `POST /albums/{album_id}/save`
- `DELETE /albums/{album_id}/save`

### Artists

- `GET /artists`
- `GET /artists/{artist_id}`
- `GET /artists/{artist_id}/albums`

### Reviews

- `PUT /reviews/{review_id}`
- `DELETE /reviews/{review_id}`

### Users

- `GET /users/me/reviews`
- `GET /users/me/saved-albums`

## Album Query Parameters

The album listing endpoint supports several query parameters to make browsing more flexible:

- `search`
  - filters albums by title
- `genre`
  - filters albums by genre
- `artist_id`
  - filters albums by artist
- `start_date`
  - filters albums released on or after a given date
- `end_date`
  - filters albums released before a given date
- `sort`
  - currently supports values such as `newest` and `oldest`
- `limit`
  - limits the number of returned albums
- `offset`
  - paginates through the album list

Example:

```text
/albums?search=blue&genre=jazz&sort=newest&limit=10&offset=0
```

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd music_album_ratings
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the dependencies your local environment uses for this project.

If you are managing packages manually, install at least:

- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `psycopg2` or `psycopg2-binary`
- `python-jose`
- `passlib`
- `bcrypt`
- `email-validator`

### 4. Create a PostgreSQL database

Create a local PostgreSQL database, for example:

- database name: `album_app`

### 5. Create the environment file

Create a `.env` file in the project root, next to `.env.example`.

Example:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/album_app
JWT_SECRET_KEY=replace-with-a-secure-secret
```

### 6. Run the API

From the `backend` folder:

```powershell
uvicorn app.main:app --reload
```

Once running, open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Environment Variables

The project reads configuration from environment variables through the `.env` file.

### Required variables

- `DATABASE_URL`
  - PostgreSQL connection string used by SQLAlchemy
- `JWT_SECRET_KEY`
  - secret used to sign and verify authentication tokens

Example:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/album_app
JWT_SECRET_KEY=replace-with-a-secure-secret
```

## Suggested API Test Flow

If you are exploring the project through Swagger, this is a good order:

1. Open `/docs`
2. Register a user with `POST /auth/register`
3. Log in with `POST /auth/login`
4. Authorize with the returned bearer token
5. Browse albums with `GET /albums`
6. Open one album with `GET /albums/{album_id}`
7. View `GET /albums/{album_id}/stats`
8. View `GET /albums/{album_id}/tracks`
9. Create a review with `POST /albums/{album_id}/reviews`
10. Save an album with `POST /albums/{album_id}/save`
11. Check `GET /users/me/reviews`
12. Check `GET /users/me/saved-albums`

## Notes and Current Limitations

- The project currently focuses on the backend API layer
- Frontend work is planned but not yet part of the delivered MVP
- Configuration is handled through `.env` variables
- The project would benefit further from automated tests and migrations in a future iteration

## Future Improvements

- Add automated test coverage
- Add Alembic migrations
- Add a frontend client for album browsing and review management
- Extend analytics endpoints for users and review activity
- Improve pagination responses with metadata such as total count
- Add stricter query parameter validation and standardized error handling

## Live Deployment

Add your deployed links here once available:

- API Base URL: `TBD`
- Swagger Docs: `TBD`
- ReDoc: `TBD`
