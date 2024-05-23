import pygame
from subprocess import call

# Ukuran layar
screen_width = 1080
screen_height = 720

white = (255, 255, 255)
black = (0, 0, 0)

# Membuat layar
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("SIMULASI CERMIN")

def open_cekung():
    call(["python", "cekungfixx.py"])

def open_cembung():
    call(["python", "cembungfixx.py"])

# Fungsi utama
def main():
    pygame.init()
    screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)

    # Tombol untuk beralih antara simulasi cermin cekung dan cermin cembung
    button_cermin_cekung = pygame.Rect(200, 307, 220, 55)
    button_cermin_cembung = pygame.Rect(650, 300, 230, 55)


    FONT = pygame.font.Font(None, 40)

    # Teks "SIMULASI CERMIN"
    text_simulasi_cermin = font.render('S I M U L A S I   C E R M I N', True, black)
    text_rect = text_simulasi_cermin.get_rect(center=(screen_width // 2, screen_height // 4))

    text_kelompok_5 = font.render('Kelompok 5', True, black)
    text_rect_kl = text_kelompok_5.get_rect(center=(screen_width // 2, screen_height // 3.2))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Tombol kiri mouse
                    if button_cermin_cekung.collidepoint(event.pos):
                        open_cekung()
                    elif button_cermin_cembung.collidepoint(event.pos):
                        open_cembung()

        screen.fill((255, 255, 255))
        
        # Menggambar tombol
        pygame.draw.rect(screen, (1, 1, 1), button_cermin_cekung)
        pygame.draw.rect(screen, (1, 1, 1), button_cermin_cembung)

        # Menampilkan teks pada tombol
        text_cermin_cekung = font.render('Cermin Cekung', True, (255, 255, 255))
        text_cermin_cembung = font.render('Cermin Cembung', True, (255, 255, 255))
        screen.blit(text_cermin_cekung, (button_cermin_cekung.x + 15, button_cermin_cekung.y + 15))
        screen.blit(text_cermin_cembung, (button_cermin_cembung.x + 15, button_cermin_cembung.y + 15))

      

        # Menampilkan teks "SIMULASI CERMIN"
        screen.blit(text_simulasi_cermin, text_rect)
        screen.blit(text_kelompok_5, text_rect_kl)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
