import os
import pyodbc
import re
import time
import pandas as pd
from tqdm import tqdm

def connect_to_sql_server(server, username, password):
    try:
        conn = pyodbc.connect(
            f'DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};UID={username};PWD={password}'
        )
        print(f"🔗 Connected to SQL Server")
        return conn, 0
    except pyodbc.InterfaceError as e:
        print(f"❌ Could not connect to the server: {server}. Please check your connection. Error: {e}")
        return None, 1
    except pyodbc.Error as e:
        print(f"❌ Failed to connect to the SQL Server. Error: {e}")
        return None, 1

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

def add_sql_metadata(database_name, function_name):
    return f"""
USE [{database_name}]
GO

/****** Object:  Function [dbo].[{function_name}]    Script Date: {time.strftime('%d-%m-%Y %H:%M:%S')} ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
"""

def handle_locked_objects(locked_objects, database_name):
    if locked_objects:
        reference_folder = "Reference"
        if not os.path.exists(reference_folder):
            os.makedirs(reference_folder)

        df = pd.DataFrame(locked_objects, columns=["Object Name"])
        df.insert(0, 'Database', database_name)

        excel_file_name = os.path.join(reference_folder, f"{database_name}_Locked_Objects.xlsx")
        df.to_excel(excel_file_name, index=False)
        print(f"⚠️ Locked or encrypted objects were found and listed in '{excel_file_name}'.")

def read_and_create_txt_files(conn, database_name, object_type):

    try:
        cursor = conn.cursor()
        cursor.execute(f"""SELECT name FROM sys.objects WHERE type = 'FN'""")  # Changed to query SQL functions

        objects = cursor.fetchall()
        total_objects = len(objects)
        locked_objects = []

        if total_objects == 0:
            print(f"❌ No {object_type.capitalize()} found under the database '{database_name}'.")
            return 0

        folder_name = f"{database_name}_{object_type.capitalize()}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        colors = ["yellow", "magenta", "cyan", "blue", "red"]
        with tqdm(total=total_objects, desc=f"Converting {database_name} {object_type.capitalize()}", ncols=100,
                  colour=colors[0]) as progress_bar:
            for idx, row in enumerate(objects):
                object_name = row[0]
                sanitized_object_name = sanitize_filename(object_name)
                try:
                    cursor.execute(f"EXEC sp_helptext '{object_name}'")
                    object_definition = ''.join([x[0] for x in cursor.fetchall()])

                    sql_content = add_sql_metadata(database_name, object_name) + object_definition

                    with open(os.path.join(folder_name, f"{sanitized_object_name}.sql"), "w") as file:
                        file.write(sql_content)

                except pyodbc.Error as e:
                    if "No results" in str(e).lower() or "not a query" in str(e).lower():
                        locked_objects.append({"Object Name": object_name})

                progress_bar.colour = colors[idx % len(colors)]
                progress_bar.update(1)

            progress_bar.colour = "green"

        cursor.close()
        handle_locked_objects(locked_objects, database_name)

    except pyodbc.Error as e:
        print(f"❌ Error executing query in database {database_name}. Error: {e}")
        return 1

    return 0

def main():
    server = 'Your_Server_Name'
    username = 'Server_UserId'
    password = 'Server_Password'
    databases = ['DB1', 'DB2','DB3','DB4']  # Multiple databases pass as array

    start_time = time.time()
    overall_flag = 0
    print(f"🔗 Attempting to connect to SQL Server...")
    conn, conn_flag = connect_to_sql_server(server, username, password)

    if conn_flag == 1:
        print("❌ Failed to establish SQL Server connection.")
        overall_flag = 1
    else:
        for database_name in databases:
            try:
                conn.execute(f"USE {database_name}")
                db_flag = read_and_create_txt_files(conn, database_name, 'Functions')
                if db_flag == 1:
                    overall_flag = 1
            except pyodbc.ProgrammingError as e:
                print(f"❌ Database '{database_name}' does not exist on the server. Error: {e}")
                overall_flag = 1
            except pyodbc.Error as e:
                print(f"❌ Database '{database_name}' not exist. Error: {e}")
                overall_flag = 1

        conn.close()

    end_time = time.time()
    total_time = end_time - start_time

    if overall_flag == 1:
        print(f"❌ Conversion failed. Total execution time: {total_time:.2f} seconds")
    else:
        print(f"✅ Conversion complete. 🐍 Thanks for using Python. Total execution time: {total_time:.2f} seconds")

if __name__ == "__main__":
    main()
