import user_interface as ui
import fingerprint_registeration as fr
import data_to_upload as dtu
import fingerprint_validation as fv
import pygame
import sys
import time

def main():

    pygame.init()
    lcd_screen = pygame.display.set_mode((ui.WIDTH, ui.HEIGHT))
    pygame.display.set_caption("ATTENDANCE SYSTEM")

    register=ui.Button(0,120,ui.WIDTH//2,ui.HEIGHT//4,ui.BLUE,"Register new fingerprint")
    validate=ui.Button(405,120,ui.WIDTH//2,ui.HEIGHT//4,ui.GREEN,"Take Attendance")
    upload=ui.Button(0,245,ui.WIDTH//2,ui.HEIGHT//4,ui.YELLOW,"Upload Attendance")
    log_off=ui.Button(405,245,ui.WIDTH//2,ui.HEIGHT//4,ui.RED,"Log Off")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if register.rect.collidepoint(pos):
                    if ui.initial_admin_authentication(ui.CHECK_AUTHENTICATION_EVENT,ui.ADMIN_FINGERPRINT_DATA):
                        fr.main()
                    else:
                        main()
                elif validate.rect.collidepoint(pos):
                    if ui.main():
                        fv.main()
                        dtu.main()
                    else:
                        main()
                elif upload.rect.collidepoint(pos):
                    dtu.main()  
                elif log_off.rect.collidepoint(pos):
                    sys.exit() if fv.show_confirmation_dialog() else main()   

                    
        current_date = time.strftime("%d-%m-%Y ")
        current_time = time.strftime("%H:%M:%S ")
        ui.lcd_screen.fill(ui.BLACK)               
        font = pygame.font.Font(None, 36)
        text_date = font.render(current_date, True, ui.WHITE)
        ui.lcd_screen.blit(text_date, (10, 8))
        text_time = font.render(current_time, True, ui.WHITE)
        ui.lcd_screen.blit(text_time, (698, 8))
        clock.tick(1)

        font = pygame.font.Font('jura.ttf', 40)
        txt1 = font.render("MAIN MENU", True, ui.WHITE)
        txt_rect1 = txt1.get_rect(center=(ui.WIDTH//2, 50))
        lcd_screen.blit(txt1, txt_rect1)
        register.draw()
        validate.draw()
        upload.draw()
        log_off.draw()
        pygame.display.update()

if __name__ == '__main__':
    main()
