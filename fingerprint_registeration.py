import json
from cryptography.fernet import Fernet
from pyfingerprint.pyfingerprint import PyFingerprint
import pygame
import user_interface as ui
import main_menu as mm
import fingerprint_validation as fv
import base64

# Initialize the fingerprint sensor
fingerprint = PyFingerprint('/dev/ttyUSB0', 57600)


# Function to enroll a fingerprint
def enroll_fingerprint(enrolled_fingerprints,cipher_suite,uidss=None):
    try:
        ui.lcd_screen.fill(ui.BLACK)
        TXT="Place your finger on the sensor..."
        print(TXT)
        ui.display_text(TXT,ui.WHITE,2)

        while not fingerprint.readImage():
            pass

        fingerprint.convertImage(1)

        TXT="Remove your finger..."
        print(TXT)
        ui.lcd_screen.fill(ui.BLACK)
        ui.display_text(TXT,ui.WHITE,2)

        ui.lcd_screen.fill(ui.BLACK)
        TXT="Place your same finger again..."
        print(TXT)
        ui.display_text(TXT,ui.WHITE,2)

        while not fingerprint.readImage():
            pass
        
        fingerprint.convertImage(2)

        if fingerprint.compareCharacteristics() == 0:
            TXT="Fingerprints do not match."
            TXXT="Try again." 
            ui.lcd_screen.fill(ui.BLACK)
            ui.Display_text(TXT,TXXT,ui.RED,2)
            return
            
        if not uidss:
            uid = ui.get_admin_input_values("Enter UID to enroll",8)
            uid= "".join([str(x) for x in uid])
            print(uid)
        else:
            uid=uidss

        # Check if the UID already exists
        if uid in enrolled_fingerprints and not uidss:
            TXT=f"UID {uid} already exists."
            print(TXT)
            ui.lcd_screen.fill(ui.BLACK)
            ui.display_text(TXT,ui.RED,2)
            return

        fingerprint_data = fingerprint.downloadCharacteristics()
        encrypt_data= cipher_suite.encrypt(bytes(fingerprint_data))
        encrypted_data_base64 = base64.b64encode(encrypt_data).decode()

        if not uidss:
            enrolled_fingerprints[uid]=encrypted_data_base64
        else:
            enrolled_fingerprints[uidss]=encrypted_data_base64
        with open("fingerprints.json", "w") as file:
            json.dump(enrolled_fingerprints, file)

            TXT="Fingerprint enrolled for "
            TXXT=f"student with UID: {uid} successfully!"
        if uidss:
            TXT="Fingerprint Re-enrolled for "
            TXXT=f"student with UID: {uidss} successfully!"
        print(TXT+TXXT)
        ui.lcd_screen.fill(ui.BLACK)
        ui.Display_text(TXT,TXXT,ui.GREEN,2)

    except Exception as e:
        ui.lcd_screen.fill(ui.BLACK)
        ui.display_text("System Error!!!",ui.RED,2)
        print(f"Error: {str(e)}")

# Function to re-roll a fingerprint
def re_enroll_fingerprint(enrolled_fingerprints,cipher_suite):  
    uid=ui.get_admin_input_values("Enter UID to re-enroll",8)
    uid= "".join([str(x) for x in uid])
    if uid in enrolled_fingerprints:
        enroll_fingerprint(enrolled_fingerprints,cipher_suite,uid)
    else:
        ui.lcd_screen.fill(ui.BLACK)
        ui.Display_text(f"Entered UID: {uid}","does not exists",ui.RED,2)


# Function to delete a fingerprint
def delete_fingerprint(enrolled_fingerprints):
    uid=ui.get_admin_input_values("Enter UID to Delete",8)
    uid= "".join([str(x) for x in uid])
    if uid not in enrolled_fingerprints:
        ui.Display_text(f"Enter UID: {uid}","do not exists",ui.RED,2)
    else:
        enrolled_fingerprints.pop(uid)
        with open("fingerprints.json", "w") as file:
            json.dump(enrolled_fingerprints, file)
        ui.lcd_screen.fill(ui.BLACK)
        TXT="Fingerprint deleted for UID"   
        ui.Display_text(TXT,uid,ui.GREEN,1.2)


# Main  loop
def main():
    pygame.display.set_caption("Enrollment Menu")
    # Create a dictionary to store enrolled fingerprints
    enrolled_fingerprints = {}

    key ='NWRmMTk3ZWUwY2RjNjA3NWY4NzQ2NmQyOGRkYzczMmM='
    cipher_suite = Fernet(key)

    try:
        with open("fingerprints.json", "r") as file:
            enrolled_fingerprints = json.load(file)
    except FileNotFoundError:
        enrolled_fingerprints = {}
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        enrolled_fingerprints= {}

    # Create buttons
    enroll_button = ui.Button(200, 120, 120, 80, ui.GREEN, "Enroll")
    re_enroll_button = ui.Button(480, 120, 120, 80, ui.BLUE, "Re-Enroll")
    quit_button = ui.Button(480, 250, 120, 80, ui.RED, "Quit")
    delete_button = ui.Button(200, 250, 120, 80, (218,165,32), "Delete")

    # Check if the sensor is initialized successfully
    if not fingerprint.verifyPassword():
        TXT="Fingerprint sensor initialization failed!"
        ui.lcd_screen.fill(ui.BLACK)
        ui.display_text(TXT,ui.RED,2)
        raise ValueError(TXT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if enroll_button.rect.collidepoint(pos):
                    enroll_fingerprint(enrolled_fingerprints,cipher_suite)
                elif re_enroll_button.rect.collidepoint(pos):
                    re_enroll_fingerprint(enrolled_fingerprints,cipher_suite)
                elif delete_button.rect.collidepoint(pos):
                    delete_fingerprint(enrolled_fingerprints)
                elif quit_button.rect.collidepoint(pos):
                    mm.main() if fv.show_confirmation_dialog() else main()      

        ui.lcd_screen.fill(ui.BLACK)
        enroll_button.draw()
        quit_button.draw()
        re_enroll_button.draw()
        delete_button.draw()
        pygame.display.update()

if __name__ == '__main__':
    main()
