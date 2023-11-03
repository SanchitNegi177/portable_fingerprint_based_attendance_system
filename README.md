# portable_fingerprint_based_attendance_system
This repo contains code to build a portable fingerprint-based attendance system using Raspberry Pi.
When I created this project, I used R307 fingerprint sensor connected to a Rasberry Pi model b+ with a TTL converter.
This project features a graphical user interface (GUI) that allows teachers to accurately record students' attendance without the possibility of false or fake attendance records.
This project provides various options like  enroll, re-enroll, and delete fingerprints. It also has options for taking attendance and then sending it to a cloud server.
This project uses library like pygame library for GUI, pyfingerprint library for registering and verifying fingerprints,fernet library for encrypting and decrypting fingerprint data, sql-connecter library for sending data to a sql database.


# Details of files present

admin.py: This file  is used to assign fingerprints of the administrator/teacher which in turn can be used for authentication when accessing some options given in the system.

data_to_upload.py: This JSON file is used to store data(section, date, time, subject code) that needs to be sent to the database.

data_to_upload.py: This  file is used to send attendance data to a database on a cloud server.

details_of_student.py: This file is used to send details of students like name, roll number, section, and uid to the database on a cloud server.

fingerprint_registration.py: This file contains the code to enroll,re-enroll, and delete the fingerprint of the student.

fingerprint_validation.py: This file contains code to take attendance by matching the fingerprints of students with stored fingerprint data.

fingerprints.json: This file is used to store uid alongside with fingerprint data of the student(in encrypted form).

jura.ttf: This file contains jura font.

main_menu.py: This file displays the main menu (various options like register fingerprint, take attendance, upload attendance, quit)of our system and provides GUI for them.

user_interface.py: This file contains various functions/methods that are frequently used in other files. Functions like authentication of admin/teacher, display message on screen, creating buttons, and other GUI-related stuff.

verified_uids.json: This JSON file is used to store attendance data(uid to student present) that needs to be sent to the database.
