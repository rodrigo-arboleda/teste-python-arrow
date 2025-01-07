import pygame
import math
import sys
import pandas as pd

# Configurações da janela
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Configurações do alvo
TARGET_X = 700
TARGET_Y = 300
TARGET_RADIUS = 20

# Configurações da flecha
ARROW_RADIUS = 5
GRAVITY = 9.8

# Configurações do obstáculo
OBSTACLE_X = 400
OBSTACLE_Y = 280
OBSTACLE_WIDTH = 10
OBSTACLE_HEIGHT = 80

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulação de Lançamento de Flechas com Obstáculo")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

def launch_arrows(launches):
    """Simula múltiplos lançamentos de flechas com um obstáculo.
    Args:
        launches (list): Lista de tuplas (angle, force) para os lançamentos.
    Returns:
        list: Lista de menores distâncias do centro do alvo que cada flecha chegou.
    """
    # Inicializa as posições e velocidades das flechas
    arrows = []
    for angle, force in launches:
        angle_rad = math.radians(angle)
        velocity_x = force * math.cos(angle_rad)
        velocity_y = -force * math.sin(angle_rad)
        arrows.append({
            "x": 50,
            "y": WINDOW_HEIGHT - 50,
            "vx": velocity_x,
            "vy": velocity_y,
            "hit": False,
            "active": True,
            "min_distance": float('inf')
        })

    running = True
    while running:
        screen.fill((255, 255, 255))

        # Desenha o alvo
        pygame.draw.circle(screen, (255, 0, 0), (TARGET_X, TARGET_Y), TARGET_RADIUS)
        # Desenha o obstáculo
        pygame.draw.rect(screen, (0, 255, 0), (OBSTACLE_X, OBSTACLE_Y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

        running = False
        for arrow in arrows:
            if arrow["active"]:
                running = True
                # Atualiza a posição da flecha
                arrow["x"] += arrow["vx"] * 0.1
                arrow["y"] += arrow["vy"] * 0.1
                arrow["vy"] += GRAVITY * 0.1

                # Verifica se a flecha atingiu o obstáculo
                if (OBSTACLE_X <= arrow["x"] <= OBSTACLE_X + OBSTACLE_WIDTH and 
                    OBSTACLE_Y <= arrow["y"] <= OBSTACLE_Y + OBSTACLE_HEIGHT):
                    arrow["active"] = False

                # Verifica se a flecha atingiu o alvo
                distance_to_target = math.hypot(arrow["x"] - TARGET_X, arrow["y"] - TARGET_Y)
                if distance_to_target <= TARGET_RADIUS:
                    arrow["hit"] = True
                    arrow["active"] = False

                # Atualiza a menor distância ao alvo
                arrow["min_distance"] = min(arrow["min_distance"], distance_to_target)

                # Verifica se a flecha saiu da tela
                if arrow["x"] > WINDOW_WIDTH or arrow["y"] > WINDOW_HEIGHT:
                    arrow["active"] = False

            # Desenha a flecha mesmo se ela não estiver ativa
            pygame.draw.circle(screen, (0, 0, 255), (int(arrow["x"]), int(arrow["y"])), ARROW_RADIUS)

        # Atualiza a tela
        pygame.display.flip()
        clock.tick(60)

        # Eventos do Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    pygame.display.flip()

    # Retorna a lista de menores distâncias
    return [arrow["min_distance"] for arrow in arrows]

def next_gen(launches, results):
    

# Exemplo de uso
if __name__ == "__main__":
    launches = [
        (23, 40), (44, 48), (54, 44), (28, 38), (39, 56),
        (56, 36), (53, 48), (39, 40), (31, 48), (22, 48),
        (33, 40), (15, 44), (17, 57), (29, 39), (35, 57),
        (73, 36), (52, 57), (25, 59), (31, 41), (73, 48),
        (22, 40), (71, 47), (70, 32), (45, 100), (65, 55),
        (61, 43), (59, 39), (25, 35), (26, 33), (49, 42),
        (42, 102), (39, 36), (61, 1001), (21, 55), (40, 43),
        (71, 67), (48, 36), (32, 59), (61, 300), (30, 58),
        (19, 32), (24, 47), (55, 53), (37, 402), (55, 44),
        (23, 51), (28, 50), (16, 320), (24, 506), (41, 55)
    ]

    results = launch_arrows(launches)
    print("Menores distâncias ao centro do alvo:", results)
