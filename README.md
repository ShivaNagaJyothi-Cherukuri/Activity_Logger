# Activity_Logger
Track your Activities Every Hour To keep track of your time effectively, and analyse later.

-- This application logs your activities every hour. It prompts you with a popup window to enter your activity and saves it to an SQLite database.

## Setup

1. **Clone the repository**:
   git clone https://github.com/ShivaNagaJyothi-Cherukuri/Activity_Logger

   ***Directory Structure***
        activity_logger.py: Main application script.
        requirements.txt: Project dependencies.
        sounds/: Directory for sound files.
        data/: Directory for SQLite database.
        README.md: Project documentation.

    
    ### Setting Up in Visual Studio

        1. Open Visual Studio and create a new Python project.
        2. Add your files: Right-click the project in Solution Explorer, select "Add" > "Existing Item," and add `activity_logger.py`, `requirements.txt`, and other files.
        3. Set up a virtual environment: Open the terminal in Visual Studio and run `python -m venv venv`, then activate it and install dependencies using `pip install -r requirements.txt`.
        4. Run your application: You can execute `activity_logger.py` from the terminal or set it as the startup file in Visual Studio.

This structure and setup will help you organize your project effectively and make it easier to manage and extend.


2. **Navigate to the project directory**:
    cd activity_logger

3. **Install dependencies**:
    pip install -r requirements.txt

4. **Run the application**:
    python activity_logger.py