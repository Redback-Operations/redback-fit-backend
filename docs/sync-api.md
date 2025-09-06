# Time Sync API


## 1. Overview 

Log user’s last-sync timestamp and allow retrieving.

### Use Cases:
    - Audit logs: Verify each data timestamp
    - Session management
    - Data consistency: Coordinate time-sensitive updates


## 2. Getting Started

### Base URL

    Base path: `https://localhost:5000/api/synced`

### Authentication

    All requests requires an `Authentication` header with Bearer token:
    Authorization: Bearer `API-TOKEN`

## 3. Endpoints
### GET
    Purpose: To fetch data/time based on the recoreded timestamp.

### URL & Method:
    GET /sync/last

### Parameter
    - userId: int

### Success Response (200 OK)
    {
        "userId": ???,
        "lastSyncedAt": "????-??-??T??:??:??Z"
    }

### Error Response
    - 401 Unauthorized
        {"error": "Invalid or missing token"}
    - 404 Not Found
        {"error": "No sync record found for userId=??"}
    - 500 Internal Server Error
        {"error": "Database unavailable"}

### POST
    Purpose: To record new sync timestamp of a device.

### URL & Method:
    POST /sync/update

### Parameter
    - userID: int
    - syncedAt: string

### Success Response (201 Created)
    {
        "userId": ???,
        "lastSyncedAt": "????-??-??T??:??:??Z"
    }

### Error Response
    - 400 Bad Request
        {"error": "Malformed JSON or missing fields"}
    - 401 Unauthorized
        {"error": "Invalid or missing token"}
    - 500 Internal Server Error
        {"error": "Failed to write to database"}

## 4. Data Models
    - userId: int
    - lastSyncedAt: string

## 5. Error Handling
    - Always check the HTTP status code first.
    - Inspect error field in response JSON for details.
    - Common remedies:
        401 → Refresh or correct your token
        400 → Validate your payload structure and fields
        404 → Ensure userId exists or call POST first
        500 → Retry after a brief pause; contact support if persistent