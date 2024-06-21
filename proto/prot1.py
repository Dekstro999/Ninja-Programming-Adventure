import pygame
import os

# Inicializar Pygame
pygame.init()

# Configurar la ventana del juego para que sea redimensionable
screen = pygame.display.set_mode((1366, 768), pygame.RESIZABLE)
pygame.display.set_caption("Juego de Plataforma")
clock = pygame.time.Clock()

# Definir la ruta base correcta
current_path = os.getcwd()
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
player_vel = 35
is_jumping = False
jump_count = 10
resting_frame_count = 0

# Lista de plataformas
platforms = [
    pygame.Rect(100, 500, 200, 20),
    pygame.Rect(300, 400, 200, 20),
    pygame.Rect(500, 300, 200, 20)
]

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
        player_x -= player_vel
        sprite = left_sprites[int(pygame.time.get_ticks() / 100) % num_frames]
    elif keys[pygame.K_d]:
        player_x += player_vel
        sprite = right_sprites[int(pygame.time.get_ticks() / 100) % num_frames]
    else:
        sprite = resting_sprites[resting_frame_count // 3 % num_frames]
        resting_frame_count += 1

    if keys[pygame.K_w] and not is_jumping:
        is_jumping = True

    # Actualizar la posición del jugador
    if is_jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jumping = False
            jump_count = 10

    # Dibujar el fondo de la pantalla
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Dibujar las plataformas
    for platform in platforms:
        screen.blit(platform_img, platform)

    # Dibujar el sprite en la pantalla
    screen.blit(sprite, (player_x, player_y))

    pygame.display.flip()

# Salir del juego
pygame.quit()
