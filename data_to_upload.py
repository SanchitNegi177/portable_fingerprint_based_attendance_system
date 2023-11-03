import mysql.connector
import json
import pygame
import user_interface as ui
import main_menu as mm

def retrieve_details( table_name,key_column, value_columns):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",
            database="attendance"
        )
        cursor = connection.cursor(dictionary=True)  
        query = f"SELECT {key_column}, {', '.join(value_columns)} FROM {table_name}"
        cursor.execute(query)
        
        data_dict = {}  

        for row in cursor:
            key_value = row[key_column]
            values = [row[col] for col in value_columns]

            if key_value in data_dict:
                data_dict[key_value].extend(values)
            else:
                data_dict[key_value] = values

        cursor.close()
        connection.close()
        return data_dict

    except mysql.connector.Error as err:
        TXT=f"MySQL error: {err}"
        TXXT="Data not uploaded"
        print(TXT)
        print(TXXT)
        ui.Display_text(TXT,TXXT,ui.RED,2)
        ui.lcd_screen.fill(ui.BLACK)
        return {}

def upload():

    # Read data from the attendance JSON file
    with open('data_to_upload.json', 'r') as attendance_file:
        attendance_data = json.load(attendance_file)

    # Read data from the UIDs JSON file
    with open('verified_uids.json', 'r') as uids_file:
        uids = json.load(uids_file)

    # Establish a MySQL database connection
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="admin",  
            database="attendance"
        )

        cursor = connection.cursor()
        date = attendance_data['Date'].replace("-", "_").replace(" ", "")
        subject_code = "".join([str(x) for x in attendance_data['Subject_Code']])
        sections = attendance_data['Sections']
        table_name = date
        
        # Create a tables in database if unavailable
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor]            
        if table_name not in tables:
            create_table_query = """
            CREATE TABLE """+table_name+""" (
                SUBJECT_CODE VARCHAR(10),
                NAME VARCHAR(50),
                SECTION VARCHAR(5),
                ROLL_NUMBER VARCHAR(10),
                UID VARCHAR(20)
            )
            """
            cursor.execute(create_table_query)

        detail_dict=retrieve_details("details","UID", ["NAME","SECTION","ROLL_NUMBER"])
        table_dict=retrieve_details(table_name,"UID", ["SUBJECT_CODE"])

        # Insert attendance data into the database table

        for uid in uids:
            if detail_dict.get(uid)==None:
                print(f"Details not available for UID: {uid}")
                continue
            name=str(detail_dict[uid][0])
            section=str(detail_dict[uid][1])
            roll=str(detail_dict[uid][2])
            if section in sections and (table_dict.get(uid)==None or subject_code != str(table_dict[uid][0])):
                cursor.execute("INSERT INTO "+table_name+" (SUBJECT_CODE,NAME,SECTION,ROLL_NUMBER,UID) VALUES (%s,%s,%s,%s,%s)", (subject_code,name,section,roll,uid))
                connection.commit()

        cursor.close()
        connection.close()
        ui.lcd_screen.fill(ui.BLACK)
        TXT="Data uploaded successfully to "
        TXXT=f"{table_name}"
        ui.Display_text(TXT,TXXT,ui.GREEN,2)
        print(TXT+TXXT)
        ui.lcd_screen.fill(ui.BLACK)

    except mysql.connector.Error as err:
        ui.lcd_screen.fill(ui.BLACK)
        TXT=f"MySQL error: {err}"
        TXXT="Data not uploaded"
        print(TXT)
        print(TXXT)
        ui.Display_text(TXT,TXXT,ui.RED,2)
        ui.lcd_screen.fill(ui.BLACK)
    except Exception as e:
        ui.lcd_screen.fill(ui.BLACK)
        TXT=f"Error: {str(e)}"
        TXXT="Data not uploaded"
        print(TXT)
        print(TXXT)
        ui.Display_text(TXT,TXXT,ui.RED,2)
        ui.lcd_screen.fill(ui.BLACK)

def main():

    pygame.display.set_caption("Data Upload")

    # Upload the data from JSON files to the cloud server
    upload()
    mm.main()
    
if __name__ == '__main__':
    main()

