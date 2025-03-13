# FastAPI Log Management API

## Overview
This FastAPI application provides endpoints for user authentication, file uploads, and retrieving stored logs. Uploaded files are stored in the `logs/` directory, and if they are ZIP files, they are extracted and stored in the database.

## Installation
1. Clone the repository.
2. Install dependencies using `pip install -r requirements.txt`.
3. Upgrade with `alembic upgrade head`
4. Run the application using:
   ```sh
   uvicorn main:app --reload
   ```

## Endpoints

### Authentication

#### Login
**Endpoint:** `POST /login/`

**Request Body:**
- `username`: User's username.
- `password`: User's password.

**Response:**
- `access_token`: JWT token for authentication.
- `token_type`: Bearer.



### User Management

#### Create a New User
**Endpoint:** `POST /users/`

**Request Body:**
- `username`: User's username.
- `password`: User's password.

**Response:**
- User object (excluding password)


### File Upload

#### Upload a File
**Endpoint:** `POST /upload`

**Request Body:**
- `file`: Upload file (plain text or ZIP format).

**Response:**
- `{"success"}` if the upload is successful.



### Log Retrieval

#### Get Logs - Endpoint with authentication 
**Endpoint:** `GET /logs`

**Query Parameters:**
- `search_word` (optional): Filter logs by keyword.
- `start_time` (optional): Filter logs after this timestamp.
- `end_time` (optional): Filter logs before this timestamp.

**Response:**
- List of logs matching the criteria.


