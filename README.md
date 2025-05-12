# redback-fit-backend

Backend API for Redback Project 3 (Wearables for athletes), built with Python and Flask.

## Prerequisites
- [Git](https://git-scm.com/downloads) installed
- [Python 3.9+](https://www.python.org/downloads/) installed
- [Postman](https://www.postman.com/downloads/) installed (optional, for testing endpoints)

## Technology Stack
### Copmpnent            ###Technology                ###Purpose
Framework                Flask                        REST API development
Database                 SQLite (Development)         Local data storage
Auth                     Firebase Auth                Secure user authentication
Testing                  Postman                      Endpoint validation
CI/CD                    Github Actions               Security scans & automated tests    

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

6. Initialize Database  
    ```bash
    python scripts/create_db.py
    ```

6. Run the Flask server  
    ```bash
    python app.py
    ```
Once running, the backend will be available at:  
`http://localhost:5000`

The Environment used in the backend are available for reference in the .env.example file located inside the Backend folder.
