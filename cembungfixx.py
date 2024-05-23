import pygame
from pygame import gfxdraw
from subprocess import call

pygame.init()
# Inisialisasi ukuran canvas
canvas = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)
# Membuat judul window
pygame.display.set_caption("Simulasi Cermin Cembung")
clock = pygame.time.Clock()

def open_cembung():
    call(["python", "cembungfixx.py"])

# RGB
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
WHITE = (255,255,255)
YELLOW = (255,255,224)
CYAN = (0,255,255)
MAGENTA = (255, 0, 255)


# Transform koordinat 
def cv_coor(x, y):
    # Kuadran ke 2
    x = canvas.get_width() // 2 + x * -1
    y = canvas.get_height() // 2 + y * -1
    return x, y

# Fungsi menggambar garis
def draw_dda_line(canvas, x1, y1, x2, y2, r, g, b):
    # hitung perubahan pada sumbu x dan y
    dx = x2 - x1
    dy = y2 - y1

    # Tentukan jumlah langkah
    panjang_garis = max(abs(dx), abs(dy))
    
    if panjang_garis != 0:
        # Hitung penambahan per langkah
        x_increment = dx / panjang_garis
        y_increment = dy / panjang_garis
    else:
        x_increment = y_increment = 0

    # Inisialisasi titik awal
    x, y = x1, y1

    # Inisialisasi warna
    warna = (r, g, b)

    # Gambar garis
    for _ in range(int(panjang_garis)):
        canvas.set_at((int(x), int(y)), warna)
        x += x_increment
        y += y_increment

# Fungsi menggambar lingkaran
def draw_dda_circle(canvas, x, y, radius, r, g, b):
    for i in range(int(x - radius), int(x + radius + 1)):
        for j in range(int(y - radius), int(y + radius + 1)):
            if (i - x) ** 2 + (j - y) ** 2 <= radius ** 2:
                canvas.set_at((i, j), (r, g, b))

# Fungsi menghitung gradien
def gradien(x1, y1, x2, y2):
    try:
        m = (y2 - y1) / (x2 - x1)
    except ZeroDivisionError:
        m = float('inf')  # Menangani kasus ketika pembagian dengan nol (garis vertikal)
    return m

def persamaan(x1, y1, x2, y2, panjang):
    m = gradien(x1, y1, x2, y2)
    y = y2 + m * (panjang - x2)
    return panjang, y

# Menghitung perbesaran cermin cembung
def perbesaran_cermin_cembung(s_aks, s):
    if s != 0:
        magnifikasi = s_aks/s  # Perbesaran cermin cembung umumnya positif
    else:
        magnifikasi = float('inf')  # Atur magnifikasi menjadi tak terbatas jika pembagian dengan nol terjadi
    return magnifikasi


FONT = pygame.font.Font(None, 24)


def draw_text(teks, x, y):
    text = FONT.render(teks, False, RED)
    text_pos = text.get_rect(centerx=x, centery=y - 15)
    canvas.blit(text, text_pos)

# Fungsi untuk menggambar tombol
def draw_button(surface, color, x, y, width, height, text):
    pygame.draw.rect(surface, color, (x, y, width, height))
    
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    surface.blit(text_surface, text_rect)



scale_factor = 1.0

# Menentukan action gerak
def move():
    global jarak_benda, tinggi_benda, titik_fokus, scale_factor
    # Aksi tekan
    keys = pygame.key.get_pressed()

    # # Ambil aksi
    # mouse = pygame.mouse.get_pressed()
    # mouse_pos = pygame.mouse.get_pos()

    if keys[pygame.K_RIGHT]:
        jarak_benda -= 0.5
    if keys[pygame.K_LEFT]:
        jarak_benda += 0.5
    if keys[pygame.K_UP]:
        tinggi_benda += 0.5
        scale_factor += 0.01
    if keys[pygame.K_DOWN]:
        tinggi_benda -= 0.5
        scale_factor -= 0.01

    if keys[pygame.K_RCTRL]:
        titik_fokus -= 1
    if keys[pygame.K_RSHIFT]:
        titik_fokus += 1

    # if mouse[0] and not InputBox.check_mouse_col():
    #     jarak_benda = (mouse_pos[0] - canvas.get_width() // 2) * -1
    #     tinggi_benda = (mouse_pos[1] - canvas.get_height() // 2) * -1


def cek_inputnya(inputnya):
    events = pygame.event.get()

    for event in events:
        # Aksi tekan mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Cek collisionnya
            if inputnya["rect"].collidepoint(event.pos):
                inputnya["active"] = not inputnya["active"]
            else:
                inputnya["active"] = False

        # Aksi kalau tekan keyboard
        if event.type == pygame.KEYDOWN:
            # Input aktif atau tidak
            if inputnya["active"]:
                # Misalkan tombol enter
                if event.key == pygame.K_RETURN:
                    try:
                        inputnya["nilai"] = int(inputnya["text"])
                    except:
                        inputnya["nilai"] = 100
                        inputnya["text"] = str(inputnya["nilai"])
                    inputnya["active"] = False
                    inputnya["change"] = True
                # Kalau tombol backspace
                elif event.key == pygame.K_BACKSPACE:
                    inputnya["text"] = inputnya["text"][:-1]
                # Kalau tombol sembarang
                else:
                    inputnya["text"] += event.unicode
    return inputnya


jarak_benda = 301 
tinggi_benda = 52
titik_fokus = 153


class InputBox:
    all_input_box = []

    def __init__(self, x, y, w, h, value):
        self.rect = pygame.Rect(x, y, w, h)
        self.value = value
        self.text = str(value)
        self.active = False
        self.change = False
        self.all_input_box.append(self)

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        try:
                            self.value = int(self.text)
                        except:
                            self.value = 100
                        self.active = False
                        self.change = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode

    def draw(self):
        if self.active:
            text_obj = FONT.render(str(self.text), False, GREEN)
        else:
            self.text = str(self.value)
            text_obj = FONT.render(str(self.text), False, RED)
        canvas.blit(text_obj, (self.rect.x, self.rect.y))

    def check_collisions(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            return True

    @classmethod
    def check_mouse_col(cls):
        if cls.all_input_box:
            for box in cls.all_input_box:
                if box.check_collisions():
                    return True


jaraknya = InputBox(0, 0, 100, 24, jarak_benda)
tingginya = InputBox(0, 0, 100, 24, tinggi_benda)
titik_fokusnya = InputBox(0, 0, 100, 24, titik_fokus)


# Main loop
def main():
    global jarak_benda, tinggi_benda, titik_fokus, tinggi_bayangan, scale_factor
    run = True

    while run:
    # Clear layar
        canvas.fill(WHITE)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

        jaraknya.handle_event(events)
        tingginya.handle_event(events)
        titik_fokusnya.handle_event(events)

        # Jarak benda
        if jaraknya.change:
            jarak_benda = jaraknya.value
            jaraknya.change = False
        else:
            jaraknya.value = abs(jarak_benda)

        # Tinggi Benda
        if tingginya.change:
            tinggi_benda_lama = tinggi_benda
            tinggi_benda = tingginya.value
            tingginya.change = False
            if tinggi_benda > tinggi_benda_lama:
                tinggi_perubahan = tinggi_benda - tinggi_benda_lama
                perubahan_skala = tinggi_perubahan // 0.5 * 0.01
                scale_factor += perubahan_skala
            elif tinggi_benda < tinggi_benda_lama:
                tinggi_perubahan = tinggi_benda_lama - tinggi_benda
                perubahan_skala = tinggi_perubahan // 0.5 * 0.01
                scale_factor -= perubahan_skala

        else:
            tingginya.value = tinggi_benda

        # Titik_fokus
        if titik_fokusnya.change:
            titik_fokus = titik_fokusnya.value
            titik_fokusnya.change = False
        else:
            titik_fokusnya.value = titik_fokus

        # Buat bayangan
        try:
            jarak_bayangan = ((titik_fokus * jarak_benda) / (jarak_benda - titik_fokus)) * -1
        except:
            jarak_bayangan = 0
        else:
            try:
                tinggi_bayangan = (jarak_bayangan / jarak_benda) * tinggi_benda
            except:
                tinggi_bayangan = 0
    

        # Garis x
        x1, y1 = 0, canvas.get_height() // 2
        x2, y2 = canvas.get_width(), canvas.get_height() // 2
        draw_dda_line(canvas, x1, y1, x2, y2, 255, 0, 0)

        # Garis y
        x1, y1 = canvas.get_width() // 2, 0
        x2, y2 = canvas.get_width() // 2, canvas.get_height()
        draw_dda_line(canvas, x1, y1, x2, y2, 255, 0, 0)

        # Benda
        lebar_body_mobil = 80  * scale_factor 
        tinggi_body_mobil = 40 * scale_factor 
        lebar_body_mobil=abs(lebar_body_mobil)

        x1, y1 = cv_coor(jarak_benda - lebar_body_mobil/1.5, tinggi_benda - tinggi_body_mobil)
        x2, y2 = cv_coor(jarak_benda + lebar_body_mobil/1.5, tinggi_benda - tinggi_body_mobil)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2), 2)  # garis A1

        x1, y1 = cv_coor(jarak_benda + lebar_body_mobil/1.5, tinggi_benda - tinggi_body_mobil)
        x2, y2 = cv_coor(jarak_benda + lebar_body_mobil/1.5, tinggi_benda - tinggi_body_mobil/2)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2), 2)  # garis B1

        x1, y1 = cv_coor(jarak_benda - lebar_body_mobil/1.5, tinggi_benda - tinggi_body_mobil)
        x2, y2 = cv_coor(jarak_benda - lebar_body_mobil/1.5, tinggi_benda - tinggi_body_mobil/2)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2), 2)  # garis B2

        x1, y1 = cv_coor(jarak_benda + lebar_body_mobil/1.5, tinggi_benda - tinggi_body_mobil/2)
        x2, y2 = cv_coor(jarak_benda + lebar_body_mobil/2.5, tinggi_benda - tinggi_body_mobil/2)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2), 2)  # garis A2

        x1, y1 = cv_coor(jarak_benda - lebar_body_mobil/1.5, tinggi_benda - tinggi_body_mobil/2)
        x2, y2 = cv_coor(jarak_benda - lebar_body_mobil/2.5, tinggi_benda - tinggi_body_mobil/2)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2), 2)  # garis A3

        x1, y1 = cv_coor(jarak_benda + lebar_body_mobil/2.5, tinggi_benda - tinggi_body_mobil/2)
        x2, y2 = cv_coor(jarak_benda + lebar_body_mobil/4, tinggi_benda)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2), 2)  # garis C1

        x1, y1 = cv_coor(jarak_benda - lebar_body_mobil/2.5, tinggi_benda - tinggi_body_mobil/2)
        x2, y2 = cv_coor(jarak_benda - lebar_body_mobil/4, tinggi_benda)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2), 2)  # garis C2

        x1, y1 = cv_coor(jarak_benda + lebar_body_mobil/4, tinggi_benda)
        x2, y2 = cv_coor(jarak_benda - lebar_body_mobil/4, tinggi_benda)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2), 2)  # garis A4

        # Menggambar ban mobil
        wheel_radius = 12  * scale_factor # Jari-jari ban mobil
        wheel_radius = abs(wheel_radius)

        x1, y1 = cv_coor(jarak_benda - lebar_body_mobil/5 - wheel_radius, tinggi_body_mobil/3.5)
        draw_dda_circle(canvas, x1, y1, wheel_radius, 0, 0, 200)  # Ban kiri

        x1, y1 = cv_coor(jarak_benda + lebar_body_mobil/5 + wheel_radius, tinggi_body_mobil/3.5)
        draw_dda_circle(canvas, x1, y1, wheel_radius, 0, 0, 200)  # Ban kanan

        # Buat titik_fokus kiri
        x1, y1 = cv_coor(titik_fokus, 0)
        x2, y2 = cv_coor(titik_fokus, 10)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2))
        draw_text("F", x2, y2)

        # Pusat kelengkungan kiri
        x1, y1 = cv_coor(titik_fokus * 2, 0)
        x2, y2 = cv_coor(titik_fokus * 2, 10)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2))
        draw_text("2F", x2, y2)
        
        # Buat titik fokus 1 kanan
        x1, y1 = cv_coor(titik_fokus * -1, 0)
        x2, y2 = cv_coor(titik_fokus * -1, 10)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2))
        draw_text("F", x2, y2)

        # titik fokus 2 kanan
        x1, y1 = cv_coor(titik_fokus * 2 * -1, 0)
        x2, y2 = cv_coor(titik_fokus * 2 * -1, 10)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2))
        draw_text("2F", x2, y2)

        # Tulisan buat input box
        teks = [
            f"Jarak Benda (s) = ",
            f"Tinggi Benda (h) = ",
            f"Titik fokus (f) = ",
            f"Jarak Bayangan (s') = ",
            f"Tinggi Bayangan (h') = ",
        ]
        value = [
            jaraknya,
            tingginya,
            titik_fokusnya,
            (int(jarak_bayangan) * -1),
            (int(tinggi_bayangan) * -1),
        ]

        x1 = canvas.get_width() - 200
        y1 = 80
        # Mengambil 2 list
        for txt, val in zip(teks, value):
            # Eksekusi teks
            teks_obj = FONT.render(txt, False, RED)
            teks_rect = teks_obj.get_rect(topright=(x1, y1))
            canvas.blit(teks_obj, teks_rect)

            # Eksekusi value
            if type(val) == int:
                value_obj = FONT.render(str(val), False, RED)
                canvas.blit(value_obj, (x1, y1))
            else:
                # Ubah posisi rectangle
                val.rect.x, val.rect.y = x1, y1
                val.draw()
            y1 += 24

# Benda
        # Sinar 1 menuju titik y kartesius
        x1, y1 = cv_coor(jarak_benda, tinggi_benda)
        x2, y2 = cv_coor(0, tinggi_benda)
        pygame.draw.line(canvas, RED, (x1, y1), (x2, y2))
        if jarak_benda < 0:
            pygame.draw.line(canvas, RED, (x1, y1), (canvas.get_width(), y2))
        else:
            pygame.draw.line(canvas, RED, (x1, y1), (0, y2))

        x1, y1 = cv_coor(0, tinggi_benda)
        x2, y2 = cv_coor(jarak_bayangan, tinggi_bayangan)
        pygame.draw.line(canvas, RED, (x1, y1), (x2, y2))
        if jarak_bayangan < 0:
            x2, y2 = persamaan(x1, y1, x2, y2, canvas.get_width())
        else:
            x2, y2 = persamaan(x1, y1, x2, y2,  0)
        pygame.draw.line(canvas, RED, (x1, y1), (x2, y2))

        x1, y1 = cv_coor(0, tinggi_bayangan)
        x2, y2 = cv_coor(jarak_benda, tinggi_benda)
        pygame.draw.line(canvas, RED, (x1, y1), (x2, y2))
        if jarak_benda < 0:
            x2, y2 = persamaan(x1, y1, x2, y2,  canvas.get_width())
        else:
            x2, y2 = persamaan(x1, y1, x2, y2,  0)
        pygame.draw.line(canvas, GREEN, (x1, y1), (x2, y2))

        x1, y1 = cv_coor(jarak_benda, tinggi_benda)
        x2, y2 = cv_coor(jarak_bayangan, tinggi_bayangan)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2))
        if jarak_bayangan < 0:
            x2, y2 = persamaan(x1, y1, x2, y2,  canvas.get_width())
        else:
            x2, y2 = persamaan(x1, y1, x2, y2,  0)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2))

        x1, y1 = cv_coor(jarak_benda, tinggi_benda)
        x2, y2 = cv_coor(jarak_bayangan, tinggi_bayangan)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2))
        if jarak_benda < 0:
            x2, y2 = persamaan(x1, y1, x2, y2, canvas.get_width())
        else:
            x2, y2 = persamaan(x1, y1, x2, y2,  0)
        pygame.draw.line(canvas, BLUE, (x1, y1), (x2, y2))

        # Bayangan
        perbesaran = perbesaran_cermin_cembung(jarak_bayangan, jarak_benda)
        lebar_bayangan_mobil = 80 * scale_factor * perbesaran  # lebar bayangan mobil
        tinggi_bayangan_mobil = 40 * scale_factor * perbesaran  # tinggi bayangan mobil
        lebar_bayangan_mobil = abs(lebar_bayangan_mobil)
        
        x1, y1 = cv_coor(jarak_bayangan - lebar_bayangan_mobil/1.5, (tinggi_bayangan) - tinggi_bayangan_mobil)
        x2, y2 = cv_coor(jarak_bayangan + lebar_bayangan_mobil/1.5, (tinggi_bayangan) - tinggi_bayangan_mobil)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2), 2)  # garis A1

        x1, y1 = cv_coor(jarak_bayangan + lebar_bayangan_mobil/1.5, (tinggi_bayangan) - tinggi_bayangan_mobil)
        x2, y2 = cv_coor(jarak_bayangan + lebar_bayangan_mobil/1.5, (tinggi_bayangan) - tinggi_bayangan_mobil/2)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2), 2)  # garis B1

        x1, y1 = cv_coor(jarak_bayangan - lebar_bayangan_mobil/1.5, (tinggi_bayangan) - tinggi_bayangan_mobil)
        x2, y2 = cv_coor(jarak_bayangan - lebar_bayangan_mobil/1.5, (tinggi_bayangan) - tinggi_bayangan_mobil/2)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2), 2)  # garis B2

        x1, y1 = cv_coor(jarak_bayangan + lebar_bayangan_mobil/1.5, (tinggi_bayangan) - tinggi_bayangan_mobil/2)
        x2, y2 = cv_coor(jarak_bayangan + lebar_bayangan_mobil/2.5, (tinggi_bayangan) - tinggi_bayangan_mobil/2)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2), 2)  # garis A2

        x1, y1 = cv_coor(jarak_bayangan - lebar_bayangan_mobil/1.5, (tinggi_bayangan) - tinggi_bayangan_mobil/2)
        x2, y2 = cv_coor(jarak_bayangan - lebar_bayangan_mobil/2.5, (tinggi_bayangan) - tinggi_bayangan_mobil/2)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2), 2)  # garis A3

        x1, y1 = cv_coor(jarak_bayangan + lebar_bayangan_mobil/2.5, tinggi_bayangan - tinggi_bayangan_mobil/2)
        x2, y2 = cv_coor(jarak_bayangan + lebar_bayangan_mobil/4, tinggi_bayangan)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2), 2)  # garis C1

        x1, y1 = cv_coor(jarak_bayangan - lebar_bayangan_mobil/2.5, tinggi_bayangan - tinggi_bayangan_mobil/2)
        x2, y2 = cv_coor(jarak_bayangan - lebar_bayangan_mobil/4, tinggi_bayangan)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2), 2)  # garis C2

        x1, y1 = cv_coor(jarak_bayangan + lebar_bayangan_mobil/4, tinggi_bayangan)
        x2, y2 = cv_coor(jarak_bayangan - lebar_bayangan_mobil/4, tinggi_bayangan)
        pygame.draw.line(canvas, BLACK, (x1, y1), (x2, y2), 2)  # garis A4


        # Menggambar bayangan ban mobil
        perbesaran = perbesaran_cermin_cembung(jarak_bayangan, jarak_benda)
        wheel_radius = 12  * scale_factor * perbesaran # Jari-jari ban mobil
        wheel_radius = abs(wheel_radius)

        x1, y1 = cv_coor(jarak_bayangan - lebar_bayangan_mobil/5 - wheel_radius, tinggi_bayangan - tinggi_bayangan_mobil)
        draw_dda_circle(canvas, x1, y1, wheel_radius, 0, 0, 0)  # Ban kiri

        x1, y1 = cv_coor(jarak_bayangan + lebar_bayangan_mobil/5 + wheel_radius, tinggi_bayangan - tinggi_bayangan_mobil)
        draw_dda_circle(canvas, x1, y1, wheel_radius, 0, 0, 0)  # Ban kanan

        x1, y1 = cv_coor(jarak_bayangan, tinggi_bayangan)
        x2, y2 = cv_coor(0, tinggi_bayangan)
        pygame.draw.line(canvas, GREEN, (x1, y1), (x2, y2))
        if jarak_bayangan < 0:
            pygame.draw.line(canvas, GREEN, (x1, y1), (canvas.get_width(), y1))
        else:
            pygame.draw.line(canvas, GREEN, (x1, y1), (0, y1))
        move()

        pygame.display.flip()





        # Event handler
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # Fungsi untuk menampilkan jendela 1

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
clock.tick(30)
