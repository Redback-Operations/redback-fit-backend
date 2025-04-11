# SQLite3 Database Interaction Guide

To interact with the database, use SQLite3 after the app is run. The database is initialized and stored in the `instance` folder. The app will automatically create the database file (`reflexion_pro.db`) and the necessary tables when it is first run.

## Interacting with the Database

Once the app is running and the database is initialized, you can interact with the database using the SQLite3 command line tool:

1. Open the terminal or command prompt.
2. Navigate to the `instance` folder where the `reflexion_pro.db` file is located.
3. Run the following command to open the SQLite3 database:

   ```bash
   sqlite3 reflexion_pro.db