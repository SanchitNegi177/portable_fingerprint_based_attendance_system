import mysql.connector


def main():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="attendance"
        )

        cursor = connection.cursor()

        name=input("Enter Name\n")
        uid=input("Enter UID\n")
        section=input("Enter Section\n")
        roll=input("Enter Roll Number\n")

        cursor.execute("INSERT INTO details (NAME, UID, SECTION,ROLL_NUMBER) VALUES (%s, %s, %s,%s)", (name, uid, section,roll))

        connection.commit()
        cursor.close()
        connection.close()

        print(f"Data uploaded successfully\n")

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
        print("Data not uploaded\n")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Data not uploaded\n")


if __name__ == '__main__':
    main()