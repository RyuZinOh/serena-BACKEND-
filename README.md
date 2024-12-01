# Flask Backend with JWT Authentication

This project implements a simple Flask backend with user registration, login, and JWT authentication, using MongoDB for data storage.

## Table of Contents

1. [Requirements](#requirements)
2. [Setup Instructions](#setup-instructions)
3. [Environment Variables](#environment-variables)
4. [API Endpoints](#api-endpoints)
   - [POST /user/register](#post-userregister)
   - [POST /user/login](#post-userlogin)
5. [Testing with Postman](#testing-with-postman)

## Requirements

- Python 3.x
- MongoDB
- Postman (for API testing)

### Python Packages

- Flask
- Flask-PyMongo
- Flask-Marshmallow
- PyJWT
- python-dotenv
- werkzeug

Install the required packages by running:

```bash
pip install -r requirements.txt
```

## Setup Instructions

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/flask-jwt-auth.git
   cd flask-jwt-auth
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up MongoDB (locally or using MongoDB Atlas) and ensure the database is accessible.

4. Create a `.env` file in the root directory and add the following environment variables:

   ```env
   MONGO_URI=your_mongo_uri_here
   SECRET_KEY=your_secret_key_here
   ```

5. Run the Flask app:

   ```bash
   python app.py
   ```

   The app will be available at `http://localhost:5000`.

## Environment Variables

Ensure the following variables are set in the `.env` file:

- `MONGO_URI`: MongoDB URI (e.g., `mongodb://localhost:27017/yourdbname`).
- `SECRET_KEY`: Secret key for signing the JWT token (use a random string).

## API Endpoints

### POST `/user/register`

**Description**: Registers a new user.

**Request Body**:

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123",
  "phone": "1234567890",
  "address": "123 Main St",
  "securityQues": "What is your pet's name?",
  "role": "user" // 1 for admin, 0 for regular user
}
```

### POST `/user/login`

**Description**: Logs in an existing user and returns a JWT token.

**Request Body**:

```json
{
  "email": "john.doe@example.com",
  "password": "password123"
}
```

## Testing with Postman

### 1. Register a User

- Set request type to `POST`.
- URL: `http://localhost:5000/user/register`
- Set `Body` to `raw`, format as `JSON`, and add the following data:

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "password123",
  "phone": "1234567890",
  "address": "123 Main St",
  "securityQues": "What is your pet's name?",
  "role": "user"
}
```

### 2. Log in and Get JWT Token

- After registration, set the request type to `POST`.
- URL: `http://localhost:5000/user/login`
- Set `Body` to `raw`, format as `JSON`, and provide login credentials:

```json
{
  "email": "john.doe@example.com",
  "password": "password123"
}
```

### 3. Use JWT Token to Access Protected Routes

- For subsequent requests, pass the JWT token in the `Authorization` header as follows:

  ```
  Authorization: Bearer <your_token_here>
  ```

You can use Postman or similar tools to test this setup and implement secure routes.

### note
The admin user is created manually and does not have a separate login route. Admins log in through the existing /user/login endpoint under the user route. Validation for admin-specific actions is handled using the is_admin middleware, which checks the role value in the user’s record to determine if they have administrative privileges.

Additionally, while the is_admin middleware has been recently added, the existing user routes were already secured with other mechanisms prior to this change. Therefore, no modifications have been made to the previous routes, and they continue to operate as originally implemented. The middleware applies to admin-specific routes only.

This approach ensures compatibility with the pre-existing architecture while maintaining security for admin operations.




    #app.run(host='0.0.0.0', port=8080, debug=True)

