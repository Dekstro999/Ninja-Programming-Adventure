import pygame
import os

# Inicializar Pygame
pygame.init()

# Configuración de la ventana del juego para que sea redimensionable
screen = pygame.display.set_mode((1366, 768), pygame.RESIZABLE)
pygame.display.set_caption("Juego de Plataforma")
clock = pygame.time.Clock()

# Verificar la ruta de trabajo actual
current_path = os.getcwd()
print(f"Ruta de trabajo actual: {current_path}")

# Definir la ruta base correcta
base_path = os.path.join(current_path, "proto")

# Cargar imágenes del fondo y las plataformas
background_path = os.path.join(base_path, "png", "BG.png")
background = pygame.image.load(background_path).convert()

platform_img_path = os.path.join(base_path, "png", "Tile (2).png")
platform_img = pygame.image.load(platform_img_path)

num_sprites = 8
num_frames = 9

# Función para cargar los sprites
def cargar_sprites(tipo, invertir=False):
    sprites = []
    for j in range(num_frames):
        frame_num = j + 1
        frame_path = os.path.join(base_path, "assets", f"{tipo}__{frame_num}.png")
        
        # Imprimir la ruta para verificar
        print(f"Cargando imagen: {frame_path}")
        
        try:
            frame = pygame.image.load(frame_path).convert_alpha()
        except FileNotFoundError:
            print(f"Error: No se encuentra el archivo {frame_path}")
            pygame.quit()
            exit()
        
        frame = pygame.transform.scale(frame, (int(frame.get_width() * 0.4), int(frame.get_height() * 0.4)))  # Escala la imagen al 40%
        if invertir:
            frame = pygame.transform.flip(frame, True, False)  # Invierte horizontalmente la imagen si es necesario
        sprites.append(frame)
    return sprites

# Cargar el sprite de reposo
resting_sprites = cargar_sprites("Idle")

# Cargar el sprite de movimiento hacia la izquierda
left_sprites = cargar_sprites("Run", invertir=True)

# Cargar el sprite de movimiento hacia la derecha
right_sprites = cargar_sprites("Run")

# Posición y velocidad del jugador
player_x = 400
player_y = 500
player_vel = 5  # Velocidad reducida en comparación con el primer código
is_jumping = False
jump_count = 10
resting_frame_count = 0

# Lista de plataformas
platforms = [
    pygame.Rect(100, 500, 200, 20),
    pygame.Rect(300, 400, 200, 20),
    pygame.Rect(500, 300, 200, 20)
]

# Clase Player del primer código
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.y_vel = -10  # Ajusta la velocidad de salto según tus necesidades
            self.is_jumping = True

    def move_left(self):
        self.x_vel = -player_vel

    def move_right(self):
        self.x_vel = player_vel

    def stop_moving(self):
        self.x_vel = 0

    def update(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        # Aplicar gravedad
        if self.y_vel < 10:  # Ajusta la velocidad de caída según tus necesidades
            self.y_vel += 0.3  # Ajusta la gravedad según tus necesidades
        else:
            self.y_vel = 10

        # Colisiones con las plataformas
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.y_vel > 0:
                    self.rect.y = platform.y - self.rect.height
                    self.is_jumping = False
                    self.y_vel = 0

# Crear una instancia del jugador
player = Player(player_x, player_y, 50, 50)

# Bucle principal del juego
running = True
while running:
    clock.tick(30)

    # Eventos del juego
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            background = pygame.transform.scale(background, (event.w, event.h))

    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()

    # Actualizar la posición del jugador
    if keys[pygame.K_a]:
        player.move_left()
        sprite = left_sprites[int(pygame.time.get_ticks() / 100) % num_frames]
    elif keys[pygame.K_d]:
        player.move_right()
        sprite = right_sprites[int(pygame.time.get_ticks() / 100) % num_frames]
    else:
        player.stop_moving()
        sprite = resting_sprites[resting_frame_count // 3 % num_frames]
        resting_frame_count += 1

    if keys[pygame.K_w]:
        player.jump()

    # Actualizar la posición del jugador
    player.update()

    # Dibujar el fondo de la pantalla
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Dibujar las plataformas
    for platform in platforms:
        screen.blit(platform_img, platform)

    # Dibujar el sprite en la pantalla
    screen.blit(sprite, (player.rect.x, player.rect.y))

    pygame.display.flip()

# Salir del juego
pygame.quit()
