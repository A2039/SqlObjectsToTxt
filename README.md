# SqlObjectsToTxt
SqlObjectsToTxt

SqlObjectsToTxt Tool
Welcome to the SQL Script Extraction Tool repository! This Python-based tool is designed to extract SQL objects such as stored procedures, functions, tables, views, and triggers from a SQL Server database and save them as .sql files. The tool also handles any locked or encrypted objects, logging them in an Excel file for easy reference.

Features
Multi-Database Support: Extract objects from multiple databases.
Object Types Supported: Stored Procedures, Functions, Tables, Views, Triggers, and Table-Valued Functions.
Automatic Metadata Addition: Adds metadata to the generated .sql files.
Locked Objects Handling: Locked or encrypted objects are logged in an Excel file.
Progress Feedback: Displays a dynamic progress bar to track script execution.
Organized Output: Files are neatly categorized into folders by database and object type.
Getting Started
There are two ways you can set up the environment for running the script:

Option 1: Using Anaconda Environment (Recommended)
Anaconda helps manage dependencies more easily, making this the recommended option.

Step-by-Step Setup:
Install Anaconda:
Download and install Anaconda from here.

Option 2: Setting Up on Local Machine (Without Anaconda)
For users who prefer not to use Anaconda, you can set up the environment using pip.

Step-by-Step Setup:
Install Python:
Ensure Python 3.11 or higher is installed on your machine. You can download it from here.

Configuration
Before running the script, you'll need to adjust some configurations in the main() function:

Server Name: Update the server variable with your SQL Server instance name.
Username: Provide your SQL Server username.
Password: Enter the password for your SQL Server.
Databases: Specify the databases you wish to extract objects from in the databases list.

server = 'YOUR_SERVER_NAME'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
databases = ['database1', 'database2']  # List your databases here

How It Works
Database Connection:
The script first connects to your SQL Server using the provided credentials.

Object Extraction:
It retrieves the SQL objects (Stored Procedures, Functions, Tables, etc.) from each specified database.

File Generation:
For each object, a .sql file is created, containing the object definition along with metadata like:

Database Name
Object Type
Creation Date
Locked Objects:
If any objects are locked or encrypted, the tool logs them in an Excel file called DatabaseName_Locked_Objects.xlsx, stored in the Reference folder.

Progress Bar:
A dynamic progress bar tracks the extraction progress using the tqdm library.

Requirements
To run the script, ensure the following are installed:

Python: 3.11 or higher
ODBC Driver: ODBC Driver 17 for SQL Server
Python Libraries: pyodbc, pandas, and tqdm
Troubleshooting
ODBC Driver Error:
If you're unable to connect to SQL Server, ensure that ODBC Driver 17 is installed and configured correctly.

Locked Objects:
If the script encounters locked or encrypted objects, they will be logged in the Excel file for further review.

Contributing
Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request. Let's make this tool even better together!

License
This project is licensed under the MIT License, so you’re free to use it, modify it, and share it.

Enjoy using the SQL Script Extraction Tool! If you encounter any issues, don’t hesitate to open an issue or contribute to the project!
