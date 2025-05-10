# redback-fit-backend

Backend API for Redback Project 3 (Wearables for athletes), built with Python and Flask.

## Prerequisites
- [Git](https://git-scm.com/downloads) installed
- [Python 3.9+](https://www.python.org/downloads/) installed
- [Postman](https://www.postman.com/downloads/) installed (optional, for testing endpoints)


### Getting Started
1. Clone the repository to your local machine  
    ```bash
    git clone https://github.com/Redback-Operations/redback-fit-backend.git
    ```

2. Navigate to the project directory  
    ```bash
    cd redback-fit-backend
    ```

3. Create a virtual environment  
    ```bash
    python -m venv env
    ```

4. Activate the virtual environment  
    - **Windows**  
        ```bash
        env\Scripts\activate
        ```
    - **Mac/Linux**  
        ```bash
        source env/bin/activate
        ```

5. Install required dependencies from `requirements.txt`  
    ```bash
    pip install -r requirements.txt
    ```

6. Create a `.env` file in the project root with the following content:
    ```env
    FLASK_ENV=development
    FLASK_APP=app.py
    SECRET_KEY=your-secret-key-here  # ⚠️ Change this to a strong, unique value before deploying to production
    DATABASE_URL=sqlite:///your_database.db
    PORT=5000

    # Firebase Configuration
    FIREBASE_API_KEY=your-api-key
    FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
    FIREBASE_PROJECT_ID=your-project-id
    FIREBASE_STORAGE_BUCKET=your-project.appspot.com
    FIREBASE_MESSAGING_SENDER_ID=your-messaging-sender-id
    FIREBASE_APP_ID=your-app-id
    FIREBASE_MEASUREMENT_ID=your-measurement-id
    FIREBASE_DATABASE_URL=https://your-project.firebaseio.com
    FIREBASE_CREDENTIALS_PATH=path/to/your/firebase/credentials.json
    ```

    > ⚠️ Do not commit your `.env` file or Firebase credentials to version control. Add these files to your `.gitignore`.

7. Run the Flask server  
    ```bash
    python app.py
    ```

Once running, the backend will be available at:  
`http://localhost:5000`
