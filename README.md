# Fertility Clinic Desktop Application

This desktop application is designed for a local fertility clinic and aims to streamline clinic operations, manage patient data, and assist in fertility treatments.

## Features

- **User-Friendly Interface**: The application features an intuitive user interface created using QtDesigner and PyQt5, making it easy to navigate and use.

- **Database Integration**: The application uses SQLite3 for local database storage and SQLAlchemy for database management, ensuring secure storage of client information.

- **Client Management**: Easily add, edit, or delete client records, and view detailed information about clients.

- **Reminder System**: Set up reminders for appointments, medication schedules, and other important events. Using the reminders interface, the admin can instantly reach clients via phone or email with a single click.

- **Data Import and Export**: Import and export client data using Excel sheets, making it convenient to work with client information and maintain records.

## Technologies Used

- **Python**: The application is built using Python.

- **QtDesigner | PyQt5**: I designed the user interface using QtDesigner, and then connected it with PyQt5 to create a sleek and professional-looking graphical user interface (GUI).

- **SQLite3**: SQLite3 is used as the database engine for storing client information and reminders locally.

- **SQLAlchemy**: SQLAlchemy is used to interact with and manage the SQLite database, providing a higher-level interface for database operations.

## Customize

To customize the application, follow these steps:

1. **Prerequisites**: Ensure you have Python installed on your system (this app uses python 3.10).

2. **Clone the Repository**: Clone this repository to your local machine.

    ```bash
    git clone https://github.com/your-username/fertility-clinic-desktop-app.git
    ```

3. **Install Dependencies**: Install the necessary Python packages using pip.

    ```bash
    pip install -r requirements.py
    ```

4. **Run the Application**: Run the main application file (main.py) to start using the desktop app.

    ```bash
    python main.py
    ```
5. **QtDesigner**: Open the UI templates on QtDesigner to edit them to follow your preferences.

