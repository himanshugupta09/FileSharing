# Simple File Sharing Site

A Flask-based web application that allows users to register, log in, upload, download, and manage their files. Users can also share their files with others by setting a "folder password."

## Functionality

*   **User Authentication:**
    *   User registration with a unique username and password.
    *   User login and logout.
*   **File Management (User's Own Files):**
    *   **Upload:** Users can upload files to their personal, secure space. Uploaded files are stored in a user-specific directory within the `uploads` folder (e.g., `F:\File-sharing-site\uploads\<username>\`).
    *   **View Files:** Users can view a list of files they have in their `files` directory (e.g., `F:\File-sharing-site\files\<username>\`).
    *   **Delete Files:** Users can delete files from their `files` directory.
*   **File Sharing & Downloading:**
    *   **Set Folder Password:** Users can set a "folder password" for sharing their uploaded files.
    *   **Download Own Files:** (Implicitly, by knowing the filename, though a direct download link from the user's directory listing isn't explicitly implemented for files in the `uploads` folder in the current `directory` view).
    *   **Download Other Users' Files:** Users can access and download files from another user's `uploads` directory if they provide the correct target username and that user's "folder password."
*   **Account Management:**
*       *   Change "folder password."

## Libraries & Technologies

*   **Flask:** A micro web framework for Python, used as the core of the application.
*   **Werkzeug:** A comprehensive WSGI web application library; used here primarily for `secure_filename` to ensure safe filenames.
*   **WTForms:** A flexible forms validation and rendering library for Python web development (imported, though direct usage in forms might be minimal or planned for future expansion).
*   **SQLite3:** A C library that provides a lightweight disk-based database (used via Python's built-in `sqlite3` module for storing user credentials and folder passwords).
*   **HTML/CSS:** For structuring and styling the web pages.

## Use Case

This project serves as a basic platform for individuals to:
1.  Store personal files in a web-accessible location.
2.  Manage their stored files (view, upload, delete).
3.  Share their collection of uploaded files with other specific users by providing them with a username and a dedicated "folder password."

## Setup and Running the Application

1.  **Prerequisites:**
    *   Python 3.x
    *   `pip` (Python package installer)

2.  **Clone the Repository (if applicable):**
    ```bash
    git clone <your-repository-url>
    cd File-sharing-site
    ```

3.  **Create a Virtual Environment (recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

4.  **Install Dependencies:**
    Create a `requirements.txt` file in the root of your project (`F:\File-sharing-site\`) with the following content:
    ```
    Flask
    WTForms
    Werkzeug
    ```
    Then install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Initialize the Database:**
    The application uses an SQLite database named `base.db`. You need to create this database and the `data` table. You can do this using an SQLite browser or by running a Python script with the following commands:
    ```python
    import sqlite3

    conn = sqlite3.connect('base.db')
    c = conn.cursor()

    # Create table
    c.execute('''
    CREATE TABLE IF NOT EXISTS data (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        folder_password TEXT
    )
    ''')

    conn.commit()
    conn.close()
    print("Database and table initialized.")
    ```
    Save this as `init_db.py` in the project root and run `python init_db.py`.

6.  **Create Necessary Directories:**
    The application expects certain directories to exist. Ensure these are created:
    *   `F:\File-sharing-site\files`
    *   `F:\File-sharing-site\uploads`
    User-specific subdirectories (e.g., `F:\File-sharing-site\files\<username>`) are created upon user registration. User-specific upload subdirectories (e.g., `F:\File-sharing-site\uploads\<username>`) are created upon the first file upload by that user.

7.  **Run the Application:**
    Navigate to the project directory (`F:\File-sharing-site\`) in your terminal and run:
    ```bash
    flask run
    ```
    Or, if you prefer to use the `if __name__ == "__main__":` block in `app.py`:
    ```bash
    python app.py
    ```
    The application should then be accessible at `http://127.0.0.1:5000` or `http://0.0.0.0:5000`.

## Important Notes & Potential Improvements

*   **Hardcoded Paths:** The application uses hardcoded absolute paths for file storage (e.g., `F:\File-sharing-site\files`, `F:\File-sharing-site\uploads`). For better portability, these should be made relative to the application root or configurable (e.g., via environment variables or a configuration file).
*   **File Listing vs. Upload Location:**
    *   The `directory()` route (listing user's files) and `delete()` route operate on files within `F:\File-sharing-site\files\<username>\`.
    *   The `uploadd_file()` route saves uploaded files to `F:\File-sharing-site\uploads\<username>\`.
    *   The `downloading()` route (for shared files) serves files from `F:\File-sharing-site\uploads\<username>\`.
    This means files uploaded via the `/uploader` are not directly listed by the `/home/directory` route or deletable via the `/delete` route as they are in different base directories. This could be streamlined for consistency.
*   **Security:**
    *   The `secret_key` is hardcoded. In a production environment, this should be a complex, random string loaded from an environment variable or a secure configuration.
    *   Passwords are stored directly. For better security, passwords should be hashed before storing in the database.
    *   Consider adding more input validation and sanitization.
*   **Error Handling:** While some error handling is present (e.g., for file uploads), it could be made more comprehensive across the application.
*   **User Experience:** The UI is basic. Further development could improve navigation, feedback to the user, and overall aesthetics.

