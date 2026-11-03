# Organ Donor Matching Web Application

A fully functional, elegantly designed full-stack web application designed to connect organ donors with hospitals and recipients seamlessly.

## Tech Stack
-   **Backend:** Python 3.x, Flask
-   **Database:** SQLite
-   **Frontend:** Vanilla HTML5, Modern CSS3 (CSS Variables, Flexbox, Grid)

## Features
-   **Role-Based Access Control:** Separate workflows and dashboards for "Donors" and "Hospitals".
-   **Donor Profiles:** Securely register, log in, and update medical history, blood type, and offered organs.
-   **Hospital Query Engine:** Advanced search interface to find compatible donors based on required blood and organ types.
-   **Responsive & Modern UI:** A beautifully designed frontend that provides an excellent user experience.

## Installation & Setup

1.  **Clone the Repository (or navigate to the project root):**
    ```bash
    cd "organ donor app"
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the Database:**
    ```bash
    flask --app app init-db
    ```

5.  **Run the Development Server:**
    ```bash
    flask run --port=5000
    ```

6.  **Access the Application:**
    Open your browser and navigate to `http://127.0.0.1:5000/`.

## Application Architecture

The application is structured using standard Flask conventions:
-   `app.py`: The core Flask application containing all routing logic.
-   `db.py`: Database connection and initialization scripts.
-   `schema.sql`: The SQLite definition of `users` and `matches` tables.
-   `templates/`: HTML templates utilizing Jinja2 for dynamic rendering.
-   `static/css/style.css`: The central stylesheet controlling the app's modern aesthetics.
