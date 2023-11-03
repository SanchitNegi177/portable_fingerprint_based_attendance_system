import pygame
import sys
import json
import time
from cryptography.fernet import Fernet
from pyfingerprint.pyfingerprint import PyFingerprint

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
BLUE=(0,0,255)
GREEN=(0,225,0)
YELLOW=(168,137,5)
BUTTON_COLOR = (50, 50, 50)
ACTIVE_COLOR = GREEN
WIDTH, HEIGHT = 800, 480
BUTTON_SIZE = 50
BUTTON_PADDING = 10

# Initialize the fingerprint sensor
fingerprint = PyFingerprint('/dev/ttyUSB0', 57600)

# Button class
class Button:
    def __init__(self, x, y, width, height, color, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.active = False
        self.label = label
        self.enabled = True

    def toggle_color(self):
        self.active = not self.active
        self.color = ACTIVE_COLOR if self.active else BUTTON_COLOR

    def draw(self):
        pygame.draw.rect(lcd_screen, self.color, self.rect)
        font = pygame.font.Font(None, 32)
        text = font.render(self.label, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        lcd_screen.blit(text, text_rect)

    def draw_on_surface(self,surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 32)
        text = font.render(self.label, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
        

def Display_text(TXT,TXXT, COLOR, duration_sec):
    font = pygame.font.Font(None, 38)
    txt1 = font.render(TXT, True, COLOR)
    txt_rect1 = txt1.get_rect(center=(WIDTH // 2, HEIGHT//2 -25))
    txt2 = font.render(TXXT, True, COLOR)
    txt_rect2 = txt2.get_rect(center=(WIDTH // 2, HEIGHT//2 +20))
    lcd_screen.blit(txt1, txt_rect1)
    lcd_screen.blit(txt2, txt_rect2)
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
                sys.exit()
            elif event.type == display_timer_event:
                timer_expired = True


def display_text(TXT, COLOR, duration_sec):
    font = pygame.font.Font(None, 38)
    txt = font.render(TXT, True, COLOR)
    txt_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    lcd_screen.blit(txt, txt_rect)
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
                sys.exit()
            elif event.type == display_timer_event:
                timer_expired = True

# Create buttons
buttons = []
button_labels = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2", "E1", "E2",
                 "F1", "F2", "G1", "G2", "H1", "H2", "I1", "I2", "J1", "J2"]

num_columns = 4
button_width = (WIDTH - (num_columns + 1) * BUTTON_PADDING) // num_columns
button_height = BUTTON_SIZE
x, y = BUTTON_PADDING, BUTTON_PADDING + 10  # Offset for title
for label in button_labels:
    button = Button(x, y, button_width, button_height, BUTTON_COLOR, label)
    buttons.append(button)
    x += button_width + BUTTON_PADDING
    if x + button_width > WIDTH:
        x = BUTTON_PADDING
        y += button_height + BUTTON_PADDING

# Create number buttons (0 to 9)
number_buttons = []
for i in range(10):
    number_button = Button(0, 240, BUTTON_SIZE, BUTTON_SIZE, BUTTON_COLOR, str(i))
    number_buttons.append(number_button)


def initial_admin_authentication(CHECK_AUTHENTICATION_EVENT,ADMIN_FINGERPRINT_DATA):    # 1st admin authentiaction
    lcd_screen.fill(BLACK)
    failed_attempts = 0
    auth_successful = False  
    
    while not auth_successful and failed_attempts < 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == CHECK_AUTHENTICATION_EVENT:
                if failed_attempts < 3:  
                    TXT = "Place admin finger to authenticate"
                    lcd_screen.fill(BLACK)
                    display_text(TXT, WHITE,2)


                    while not fingerprint.readImage():
                        pass
                        
                    fingerprint.convertImage(1)
                    result = fingerprint.searchTemplate()
                    
                    if result[0] >=0:
                        TXT = "Admin Authenticated!"
                        lcd_screen.fill(BLACK)
                        display_text(TXT, GREEN,1.2)
                        print(TXT)
                        auth_successful = True
                        return True
                    else:
                        failed_attempts += 1
                        TXT = "Authentication failed"
                        TXXT = f"Failed Attempts: {failed_attempts}"
                        lcd_screen.fill(BLACK)
                        Display_text(TXT, TXXT, RED,1.2)
                        print(TXT + TXXT)
    
    return admin_password_authentication()


def admin_password_authentication():                # Alternate admin login
    failed_attempts = 3
    while 1:
        lcd_screen.fill(BLACK)
        TXT="Enter admin PIN:"
        correct_password=[0,0,0,0]
        password=get_admin_input_values(TXT,4)
        print(TXT)
        print(password)
        if password == correct_password:
            TXT = "Admin Authenticated!"
            lcd_screen.fill(BLACK)
            display_text(TXT, GREEN,1.2)
            print(TXT)
            return True
        elif failed_attempts==0:
            lcd_screen.fill(BLACK)
            Display_text(f"Authentication Failed !","Returning to main menu",RED,2)
            return False
        else:
            failed_attempts-=1
            TXT = "Incorrect Password "
            TXXT = f"Attempts Left: {failed_attempts+1}"
            lcd_screen.fill(BLACK)
            Display_text(TXT, TXXT, RED,1.2)
            print(TXT + TXXT)


def get_admin_input_sections():

    for button in buttons:
        button.color=BUTTON_COLOR
        
    # Create a "Submit" button for sections
    submit_button = Button(200, 400,  120, 50, BLUE, "Submit")
    quit_button = Button(500, 400, 120, 50, RED, "Quit")

    lcd_screen.fill(BLACK)  # Clear the screen
    font = pygame.font.Font('jura.ttf', 38)
    title_text = font.render("Select Sections:", True, WHITE)  
    title_rect = title_text.get_rect(center=(WIDTH // 2, 30))
    lcd_screen.blit(title_text, title_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = pygame.mouse.get_pos()

                    if quit_button.rect.collidepoint(pos):
                        import main_menu as mm
                        import fingerprint_validation as fv
                        if fv.show_confirmation_dialog() :
                            mm.main()
                    elif submit_button.rect.collidepoint(pos):
                        # Clear the screen
                        lcd_screen.fill(WHITE)
                        pygame.display.update()

                        # Check if any buttons are active
                        
                        selected_buttons= [button.label for button in buttons if button.active]

                        if not selected_buttons:
                            TXT="No section is selected"
                            print(TXT)
                            lcd_screen.fill(BLACK)
                            display_text(TXT,RED,1.2)
                        else:
                            return selected_buttons,current_date,current_time

                    for button in buttons:
                        if button.rect.collidepoint(pos):
                            button.toggle_color()

        lcd_screen.fill(BLACK)  # Clear the screen
        # Align buttons in rows and columns
        # num_rows = len(buttons) // num_columns + 1
        for i, button in enumerate(buttons):
            row = i // num_columns
            col = i % num_columns
            x = BUTTON_PADDING + col * (button_width + BUTTON_PADDING)
            y = BUTTON_PADDING + 65 + row * (button_height + BUTTON_PADDING)
            button.rect = pygame.Rect(x, y, button_width, button_height)
            button.draw()

        submit_button.draw()
        quit_button.draw()
        lcd_screen.blit(title_text, title_rect)

        current_date = time.strftime("%d-%m-%Y ")
        current_time = time.strftime("%H:%M:%S ")
        font = pygame.font.Font(None, 36)
        text_date = font.render(current_date, True, WHITE)
        lcd_screen.blit(text_date, (10, 8))
        text_time = font.render(current_time, True, WHITE)
        lcd_screen.blit(text_time, (698, 8))
        pygame.time.Clock().tick(30)
        pygame.display.flip()


def get_admin_input_values(TITLE,N):
    # Clear the value list
    value_list = []
    values_display_rect = pygame.Rect(50, 65, WIDTH-100, 50)
    value_list_text = ""

    value_list.clear()
    value_list_text = " ".join(map(str, value_list))

   
    lcd_screen.fill(BLACK)  # Clear the screen
    font = pygame.font.Font('jura.ttf', 38)
    title_text = font.render(TITLE, True, WHITE)  
    title_rect = title_text.get_rect(center=(WIDTH // 2, 30))
    lcd_screen.blit(title_text, title_rect)
    pygame.display.update()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    if quit_button.rect.collidepoint(pos):
                        import main_menu as mm
                        import fingerprint_validation as fv
                        if fv.show_confirmation_dialog():
                            mm.main() 
                    elif submit_button.rect.collidepoint(pos):
                        if len(value_list) != N:
                            # Clear the screen
                            lcd_screen.fill(WHITE)
                            pygame.display.update()
                            lcd_screen.fill(BLACK)
                            TXT=f"You must select {N} values"
                            display_text(TXT,RED,1.2)
                        else:
                            return value_list

                    for number_button in number_buttons:
                        if number_button.rect.collidepoint(pos):
                            if len(value_list) < N:
                                value_list.append(int(number_button.label))
                                value_list_text = " ".join(map(str, value_list))

                    if clear_button.rect.collidepoint(pos):
                        value_list.clear()
                        value_list_text = " ".join(map(str, value_list))
        lcd_screen.fill(BLACK)  

        # Calculate the number of rows and columns for buttons
        num_rows = 2  
        num_columns = 3  
        button_width = (WIDTH - (num_columns + 1) * BUTTON_PADDING) // num_columns
        button_height = BUTTON_SIZE
        x, y = -252, 140  

        for number_button in number_buttons:
            if len(value_list) < N:
                number_button.rect = pygame.Rect(x, y, button_width, button_height)
                # number_button.draw()
                x += button_width + BUTTON_PADDING
                if x + button_width + BUTTON_PADDING > WIDTH:
                    x = BUTTON_PADDING
                    y += button_height + BUTTON_PADDING
                number_button.draw()
        number_buttons[0].rect=pygame.Rect(x+BUTTON_PADDING+button_width, y, button_width, button_height)
        if len(value_list) < N:
            number_buttons[0].draw()


        current_date = time.strftime("%d-%m-%Y ")
        current_time = time.strftime("%H:%M:%S ")
        font = pygame.font.Font(None, 36)
        text_date = font.render(current_date, True, WHITE)
        lcd_screen.blit(text_date, (10, 8))
        text_time = font.render(current_time, True, WHITE)
        lcd_screen.blit(text_time, (698, 8))
        pygame.time.Clock().tick(30)


        lcd_screen.blit(title_text, title_rect)
        submit_button = Button(350, 400, 120, 50, GREEN, "Submit")
        quit_button = Button(600, 400, 120, 50, RED, "Quit")
        clear_button = Button(100, 400, 120, 50, BLUE, "Clear")
        submit_button.draw()
        clear_button.draw()  
        quit_button.draw()

        # Draw the value list label and text
        
        pygame.draw.rect(lcd_screen, WHITE, values_display_rect)
        font = pygame.font.Font(None, 36)
        value_list_text_surface = font.render(value_list_text, True, BLACK)
        value_list_text_rect = value_list_text_surface.get_rect(center=values_display_rect.center)
        lcd_screen.blit(value_list_text_surface, value_list_text_rect)

        pygame.display.update()


# Initialize Pygame
pygame.init()
lcd_screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 40)
pygame.display.set_caption("Attendance Tracking")


CHECK_AUTHENTICATION_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(CHECK_AUTHENTICATION_EVENT, 1000)
ADMIN_FINGERPRINT_DATA = b'HI'
# MAIN
def main():
    
    if not fingerprint.verifyPassword():
            TXT="Fingerprint sensor initialization failed!"
            display_text(TXT,RED,1.5)
            raise ValueError(TXT)


    if initial_admin_authentication(CHECK_AUTHENTICATION_EVENT,ADMIN_FINGERPRINT_DATA):
        selected_sections,current_date,current_time = get_admin_input_sections()
        if selected_sections:
            selected_values = get_admin_input_values("Type Subject Code:",3)
            if selected_values:
                print("Selected Sections:", selected_sections)
                print("Selected Values:", selected_values)
                print("time:",current_time)
                print("Date:",current_date)
                with open("data_to_upload.json", "w") as file:
                    data={"Date":current_date,"Time":current_time,"Sections":selected_sections,"Subject_Code":selected_values}
                    json.dump(data, file)
        return True            
    else:
        return False

if __name__ == '__main__':
    main()
