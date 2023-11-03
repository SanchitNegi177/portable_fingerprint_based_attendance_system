from cryptography.fernet import Fernet
from pyfingerprint.pyfingerprint import PyFingerprint
import user_interface as ui
import main_menu as mm
import base64
import json
import pygame
import time

SURFACE_WIDTH=800
SURFACE_HEIGHT=350

# Initialize the fingerprint sensor
fingerprint = PyFingerprint('/dev/ttyUSB0', 57600)
quit_button=ui.Button(350,380,120,50,ui.RED,"Quit")
surface = pygame.Surface((SURFACE_WIDTH, SURFACE_HEIGHT))
current_date=""
current_time=""
 # Create a set to store verified UIDs 
verified_uids = set()

def show_confirmation_dialog():
    ui.lcd_screen.fill(ui.BLACK)
    confirmation_dialog = pygame.Surface((440, 220))
    upper_screen = pygame.Surface((800, 480))
    confirmation_dialog_rect = confirmation_dialog.get_rect(center=(ui.WIDTH // 2, ui.HEIGHT // 2))
    font = pygame.font.Font("jura.ttf", 38)
    text = font.render("Do you want to quit?", True, ui.WHITE)
    font = pygame.font.Font(None, 36)
    text_rect = text.get_rect(center=(confirmation_dialog.get_width() // 2, 30))
    yes_button = ui.Button(235, 250, 120, 50, ui.GREEN, "YES")
    no_button = ui.Button(440, 250, 120, 50, ui.RED, "NO")
    confirmation_dialog.fill(ui.BUTTON_COLOR)
    confirmation_dialog.blit(text, text_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if yes_button.rect.collidepoint(pos):
                    return True
                elif no_button.rect.collidepoint(pos):
                    return False
                elif not confirmation_dialog_rect.collidepoint(pos):
                    return False
                
        ui.lcd_screen.blit(confirmation_dialog, confirmation_dialog_rect)
        yes_button.draw()
        no_button.draw()
        pygame.display.update()


def display_text_on_surface(txt, color, duration_sec, TXXT=None):
    global is_paused
    ui.lcd_screen.fill(ui.BLACK)
    font = pygame.font.Font(None, 38)
    if TXXT:
        txt1 = font.render(txt, True, color)
        txt_rect1 = txt1.get_rect(center=(SURFACE_WIDTH // 2,ui.HEIGHT // 2 - 35))
        txt2 = font.render(TXXT, True, color)
        txt_rect2 = txt2.get_rect(center=(SURFACE_WIDTH // 2, ui.HEIGHT // 2 + 10))
        ui.lcd_screen.blit(txt1, txt_rect1)
        ui.lcd_screen.blit(txt2, txt_rect2)
    else:
        text = font.render(txt, True, color)
        text_rect = text.get_rect(center=(SURFACE_WIDTH // 2, ui.HEIGHT // 2 -10))
        ui.lcd_screen.blit(text, text_rect)
    
    btn()
    date_time(ui.lcd_screen)
    pygame.display.update()

    # Create a timer event to control the display duration
    display_timer_event = pygame.USEREVENT + 2
    pygame.time.set_timer(display_timer_event, int(duration_sec * 1000))  # Convert seconds to milliseconds

    # Wait for the timer event
    timer_expired = False
    while not timer_expired:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == display_timer_event:
                timer_expired = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if quit_button.rect.collidepoint(pos):
                    mm.main() if show_confirmation_dialog() else main()      


def btn():
    quit_button.draw()
    pygame.display.update()


def date_time(screen):
    current_date = time.strftime("%d-%m-%Y ")
    current_time = time.strftime("%H:%M:%S ")
    font = pygame.font.Font(None, 36)
    text_date = font.render(current_date, True, ui.WHITE)
    text_time = font.render(current_time, True, ui.WHITE)
    screen.blit(text_date, (10, 8))
    screen.blit(text_time, (698, 8)) 
    pygame.display.update()
    pygame.time.Clock().tick(1)


# Function to verify a fingerprint and store the UID if matched
def verify_fingerprint(verified_uids,enrolled_fingerprints,cipher_suite):
    try:
        TXT="Place your finger on the sensor..."
        print(TXT)
        display_text_on_surface(TXT,ui.WHITE,2 )
         
        while not fingerprint.readImage() :
            pos = pygame.mouse.get_pos()
            if quit_button.rect.collidepoint(pos):
                return    

        fingerprint.convertImage(1)
        captured_template = fingerprint.downloadCharacteristics()

        for uid, value in enrolled_fingerprints.items():
            fingerprint.uploadCharacteristics(2,list(value))
            if fingerprint.compareCharacteristics() != 0:
                if uid not in verified_uids:
                    verified_uids.add(uid)
                    TXT="Attendance marked of student UID:"
                    TXXT=f"{uid}"
                    print(TXT)
                    display_text_on_surface(TXT,ui.GREEN,1,TXXT ) 
                    
                else:
                    TXT="Attendance already marked for UID: "
                    TXXT=uid
                    print(TXT, TXXT)
                    display_text_on_surface(TXT,ui.BLUE,0.5 ,TXXT)  
     
                return

        TXT="Fingerprint not recognized."
        print(TXT)         
        display_text_on_surface(TXT,ui.RED,0.5 )
         
    except Exception as e:
        ui.lcd_screen.fill(ui.BLACK)
        display_text_on_surface("ERROR!!!",ui.WHITE,2,f"{(e)}")
        print(f"Error: {str(e)}")


def main():
    key ='NWRmMTk3ZWUwY2RjNjA3NWY4NzQ2NmQyOGRkYzczMmM='
    cipher_suite = Fernet(key)

    # Load the enrolled fingerprints (Encryted templates)
    try:
        with open("fingerprints.json", "r") as file:
            loaded_fingerprint_base64 = json.load(file)
    except FileNotFoundError:
        loaded_fingerprint_base64 = {}
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        loaded_fingerprint_base64 = {}

    enrolled_data = {uid: base64.b64decode(data) for uid, data in loaded_fingerprint_base64.items()}
    enrolled_fingerprints = {uid: bytes(cipher_suite.decrypt(decrpt)) for uid, decrpt in enrolled_data.items()}

    # Check if the sensor is initialized successfully
    if not fingerprint.verifyPassword():
        TXT="Fingerprint sensor initialization failed!"
        ui.lcd_screen.fill(ui.BLACK)
        ui.display_text(TXT,ui.RED,2)
        raise ValueError("Fingerprint sensor initialization failed!")

    clock = pygame.time.Clock()
    
    while True:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if quit_button.rect.collidepoint(pos):
                    mm.main() if show_confirmation_dialog() else main()      

          
        verify_fingerprint(verified_uids,enrolled_fingerprints,cipher_suite)

        # After verifying all fingerprints, save the verified UIDs to a file
        with open("verified_uids.json", "w") as file:
            json.dump(list(verified_uids), file)
        
        surface.fill(ui.BLACK)
        pygame.display.update()
        global current_time,current_date
        date_time(surface)
        pygame.display.update()
        btn()
        ui.lcd_screen.blit(surface, (0,0))
        pygame.display.update()

        
if __name__ == '__main__':
    main()
