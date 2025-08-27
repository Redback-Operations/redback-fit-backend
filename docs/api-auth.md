# Authentication API
This document describes the **login** and **logout** endpoints implemented in the `auth` blueprint.

Authentication uses **Flask-Login** session cookies.  
- Login expects **form POST**.  
- Successful login redirects (302).  
- Failed login returns **400** with a plain-text error message.  
- Logout requires an active session and always redirects back to the login page.

Base path: `/auth`

---

## POST `/auth/login`

Log a user in.

### Request
- **Body fields**
  - `email` *(string, required)* – user email
  - `password` *(string, required)*
  - `remember` *(optional, any truthy value)* – set a long-lived session
  - `next` *(optional)* – relative path to redirect after login (validated for safety)

### Responses
- **302**: Redirect to:
  - `next` (if provided & safe), otherwise `/home`
- **400**: Plain text error  

### Rate limiting
- Limited to **5 POST requests per minute** per IP (`flask-limiter`).

### Examples

    **Success (redirect to /home)**
    ```bash
    curl -i -X POST http://localhost:5000/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "email=test@example.com&password=Password123&remember=1"

    curl -i -X POST "http://localhost:5000/auth/login?next=/dashboard" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "email=test@example.com&password=Password123"


    curl -i -X POST http://localhost:5000/auth/login \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "email=test@example.com&password=wrong"
    # HTTP/1.1 400 BAD REQUEST
    # body: Login failed. Incorrect email or password.

## GET `/auth/logout`

Logs out the current user (if logged in) and redirects to login

### Auth
- Requires an active session (`@login_required`)
- If not logged in, user is redirected to `\auth\login`

### Responses
- **302**: Redirect to `/auth/login`

### Examples
    curl -i http://localhost:5000/auth/logout

## POST `/auth/logout`

Same as GET, but uses POST (sometimes preferred fro CSRF-protected UIs)

### Responses
- **302**: Redirect to `/auth/login`
- If not logged in -> **302** to `/auth/login`

### Examples
    curl -i -X POST http://localhost:5000/auth/logout

## GET `/auth/signup`

Render the signup page (HTML)

### Responses
- **200** OK: return HTML signup form

## POST `/auth/signup`
Create a new account (UserCredential + UserProfile)

### Request
- Content-Type: application/x-www-form-urlencoded
- Body fields
    - name (string, required)
    - email (string, required, unique)
    - password (string, required, validated for strength)

### Responses
- **302**: Redirect to `/home` after successfull signup and auto-login
- **400**: Validation error (missing fields, weak password, etc.)
- **409**: Duplicate email

### Examples
    **Success (redirect to /home)**
        ```bash
        curl -i -X POST http://localhost:5000/auth/signup \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "name=Test User&email=new@example.com&password=Password123!"

        curl -i -X POST http://localhost:5000/auth/signup \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "name=Test User&email=test@example.com&password=Password123!"
        # HTTP/1.1 409 CONFLICT
        # body: Signup failed. Email already registered.

## Error Reference
| Endpoint       | Scenario                       | Status | Behavior / Message                           |
| -------------- | ------------------------------ | ------ | -------------------------------------------- |
| `/auth/login`  | Missing or wrong password      | 400    | `Login failed. Incorrect email or password.` |
| `/auth/login`  | Success no `next`              | 302    | Redirect to `/home`                          |
| `/auth/login`  | Success with safe `next`       | 302    | Redirect to that path                        |
| `/auth/logout` | Not logged in                  | 302    | Redirect to `/auth/login`                    |
| `/auth/logout` | Success                        | 302    | Redirect to `/auth/login`                    |
| `/auth/signup` | Success                        | 302    | Redirect to `/home`                          |
| `/auth/signup` | Duplicate email                | 409    | `Signup failed. Email already registered.`   |
| `/auth/signup` | Weak password / missing fields | 400    | Error message (e.g. "Password too short")    |

