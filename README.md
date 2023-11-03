# portable_fingerprint_based_attendance_system
# portable_fingerprint_based_attendance_system
This repo contains code to build a portable fingerprint-based attendance system using Raspberry Pi.
When I created this project, I used R307 fingerprint sensor connected to a Rasberry Pi model b+ with a TTL converter.
This project features a graphical user interface (GUI) that allows teachers to accurately record students' attendance without the possibility of false or fake attendance records.
This project provides various options like  enroll, re-enroll, and delete fingerprints. It also has options for taking attendance and then sending it to a cloud server.
This project uses library like pygame library for GUI, pyfingerprint library for registering and verifying fingerprints,fernet library for encrypting and decrypting fingerprint data, sql-connecter library for sending data to a sql database.
