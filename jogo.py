
import pygame
import random
import math
import sys

pygame.init()

# ==========================================
# CONFIGURACOES
# ==========================================

LARGURA, ALTURA = 1200, 700
FPS = 60

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Banguela Adventure")
RELOGIO = pygame.time.Clock()

BRANCO = (245, 250, 255)
PRETO = (5, 10, 20)
CIANO = (70, 220, 255)
LARANJA = (255, 140, 50)

FONT_TITULO = pygame.font.SysFont("arialblack", 48)
FONT_GRANDE = pygame.font.SysFont("arialblack", 29)
FONT_MEDIA = pygame.font.SysFont("arial", 22, bold=True)
FONT_PEQUENA = pygame.font.SysFont("arial", 17, bold=True)

BIOMAS = [
    {"name": "Ilha de Berk", "sky": (15, 40, 70), "ground": (45, 75, 90), "detail": (90, 200, 230), "boss": "MORTE RUBRA", "boss_color": (190, 65, 48), "boss_hp": 14},
    {"name": "Floresta dos Dragoes", "sky": (10, 45, 35), "ground": (35, 80, 45), "detail": (90, 210, 110), "boss": "GUARDIAO DA MATA", "boss_color": (80, 180, 95), "boss_hp": 16},
    {"name": "Ilha Vulcanica", "sky": (65, 20, 20), "ground": (75, 40, 35), "detail": (255, 100, 35), "boss": "TITAN DE MAGMA", "boss_color": (255, 85, 25), "boss_hp": 18},
    {"name": "Reino Congelado", "sky": (25, 60, 95), "ground": (85, 125, 155), "detail": (160, 235, 255), "boss": "WYRM DE GELO", "boss_color": (100, 210, 255), "boss_hp": 16},
    {"name": "Cavernas de Cristal", "sky": (35, 20, 75), "ground": (60, 45, 90), "detail": (190, 120, 255), "boss": "COLOSSO CRISTALINO", "boss_color": (180, 100, 255), "boss_hp": 17},
    {"name": "Deserto dos Ossos", "sky": (90, 55, 25), "ground": (125, 85, 45), "detail": (250, 200, 105), "boss": "DEVORADOR DAS DUNAS", "boss_color": (215, 155, 75), "boss_hp": 17},
    {"name": "Ilhas Flutuantes", "sky": (30, 55, 100), "ground": (55, 95, 110), "detail": (110, 225, 220), "boss": "SENTINELA DO CEU", "boss_color": (90, 185, 255), "boss_hp": 18},
    {"name": "Mundo Oculto", "sky": (15, 15, 45), "ground": (40, 40, 80), "detail": (130, 110, 255), "boss": "ALFA DAS SOMBRAS", "boss_color": (145, 105, 255), "boss_hp": 20}
]

ESPECIES = [
    ("Nadder Mortal", (65, 170, 210)),
    ("Gronckle", (151, 125, 95)),
    ("Pesadelo Monstruoso", (220, 80, 48)),
    ("Zipera Arrepiante", (90, 205, 155)),
    ("Tambor Trovejante", (95, 105, 145)),
    ("Furia da Luz", (220, 225, 245)),
    ("Pesadelo Voador", (170, 85, 185)),
    ("Gronckle de Pedra", (120, 130, 115))
]

DIFICULDADES = {
    "Facil": {"vidas": 5, "velocidade": 1.2, "dano": 1, "chefe": 1.0},
    "Normal": {"vidas": 4, "velocidade": 1.7, "dano": 1, "chefe": 1.3},
    "Dificil": {"vidas": 3, "velocidade": 2.2, "dano": 1, "chefe": 1.7},
    "Insano": {"vidas": 2, "velocidade": 2.7, "dano": 2, "chefe": 2.1}
}


# ==========================================
# FUNCOES VISUAIS
# ==========================================

def escrever(texto, fonte, cor, posicao):
    imagem = fonte.render(str(texto), True, cor)
    TELA.blit(imagem, imagem.get_rect(center=posicao))


def gradiente(cor1, cor2):
    for y in range(ALTURA):
        t = y / ALTURA
        cor = tuple(
            int(cor1[i] * (1 - t) + cor2[i] * t)
            for i in range(3)
        )
        pygame.draw.line(TELA, cor, (0, y), (LARGURA, y))


def painel(rect, cor=(5, 13, 29), borda=CIANO):
    camada = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(camada, (*cor, 225), camada.get_rect(), border_radius=18)
    pygame.draw.rect(camada, (*borda, 230), camada.get_rect(), 2, border_radius=18)
    TELA.blit(camada, rect.topleft)


def desenhar_botao(rect, nome, mouse, ativo=False):
    hover = rect.collidepoint(mouse)
    cor = (25, 65, 90) if hover or ativo else (12, 28, 48)
    pygame.draw.rect(TELA, cor, rect, border_radius=12)
    pygame.draw.rect(TELA, CIANO if hover or ativo else (65, 100, 125), rect, 2, border_radius=12)
    escrever(nome, FONT_PEQUENA, BRANCO, rect.center)


# ==========================================
# MENU
# ==========================================

def menu():
    indice_bioma = 0
    indice_modo = 0
    indice_dificuldade = 1

    modos = ["Aventura", "Sobrevivencia"]
    dificuldades = list(DIFICULDADES.keys())

    while True:
        mouse = pygame.mouse.get_pos()
        gradiente((5, 12, 31), (17, 40, 62))

        for i in range(70):
            x = (i * 173) % LARGURA
            y = (i * 83) % 330
            pygame.draw.circle(TELA, (120, 160, 195), (x, y), 2)

        escrever("BANGUELA ADVENTURE", FONT_TITULO, BRANCO, (600, 75))
        escrever("ESCOLHA SUA JORNADA", FONT_MEDIA, CIANO, (600, 130))

        bioma = BIOMAS[indice_bioma]

        painel(pygame.Rect(70, 165, 510, 390), borda=bioma["detail"])

        arte = pygame.Rect(95, 190, 460, 220)
        pygame.draw.rect(TELA, bioma["sky"], arte, border_radius=15)

        for i in range(8):
            x = 95 + i * 65
            altura = 80 + (i * 37) % 90
            pygame.draw.polygon(
                TELA, bioma["ground"],
                [(x, 400), (x + 35, 400 - altura), (x + 70, 400)]
            )

        pygame.draw.rect(TELA, bioma["ground"], (95, 380, 460, 30))
        escrever(bioma["name"], FONT_GRANDE, BRANCO, (325, 455))
        escrever("CHEFE: " + bioma["boss"], FONT_PEQUENA, bioma["detail"], (325, 495))
        escrever(f"Bioma {indice_bioma + 1}/8", FONT_PEQUENA, BRANCO, (325, 525))

        anterior = pygame.Rect(105, 435, 48, 45)
        proximo = pygame.Rect(500, 435, 48, 45)

        desenhar_botao(anterior, "<", mouse)
        desenhar_botao(proximo, ">", mouse)

        painel(pygame.Rect(620, 165, 510, 390))

        escrever("MODO DE JOGO", FONT_MEDIA, CIANO, (875, 215))

        botoes_modo = [
            pygame.Rect(665 + i * 210, 245, 195, 52)
            for i in range(2)
        ]

        for i, rect in enumerate(botoes_modo):
            desenhar_botao(rect, modos[i], mouse, i == indice_modo)

        escrever("DIFICULDADE", FONT_MEDIA, CIANO, (875, 340))

        botoes_dificuldade = [
            pygame.Rect(660 + (i % 2) * 220, 370 + (i // 2) * 62, 205, 48)
            for i in range(4)
        ]

        for i, rect in enumerate(botoes_dificuldade):
            desenhar_botao(rect, dificuldades[i], mouse, i == indice_dificuldade)

        iniciar = pygame.Rect(390, 585, 420, 68)
        desenhar_botao(iniciar, "INICIAR AVENTURA", mouse, True)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if anterior.collidepoint(mouse):
                    indice_bioma = (indice_bioma - 1) % len(BIOMAS)

                elif proximo.collidepoint(mouse):
                    indice_bioma = (indice_bioma + 1) % len(BIOMAS)

                elif iniciar.collidepoint(mouse):
                    return bioma, modos[indice_modo], dificuldades[indice_dificuldade]

                for i, rect in enumerate(botoes_modo):
                    if rect.collidepoint(mouse):
                        indice_modo = i

                for i, rect in enumerate(botoes_dificuldade):
                    if rect.collidepoint(mouse):
                        indice_dificuldade = i

        pygame.display.flip()
        RELOGIO.tick(FPS)


# ==========================================
# CENARIO
# ==========================================

def desenhar_fundo(camera, bioma, tempo):
    gradiente(
        bioma["sky"],
        tuple(c // 2 for c in bioma["sky"])
    )

    pygame.draw.circle(TELA, (220, 230, 240), (960, 110), 35)
    pygame.draw.circle(TELA, bioma["sky"], (975, 95), 35)

    for camada in range(3):
        cor = tuple(
            max(0, min(255, c + camada * 10 - 18))
            for c in bioma["ground"]
        )

        pontos = [(0, ALTURA)]
        deslocamento = int(camera * (0.12 + camada * 0.09)) % 170

        for x in range(-170, LARGURA + 170, 170):
            xx = x - deslocamento
            pico = 300 + camada * 62 + math.sin((x + camera * 0.1) * 0.009) * 38
            pontos.append((xx, int(pico)))
            pontos.append((xx + 85, int(pico + 90)))

        pontos.append((LARGURA, ALTURA))
        pygame.draw.polygon(TELA, cor, pontos)

    for i in range(30):
        x = int((i * 97 - camera * 0.22 + tempo * 6) % (LARGURA + 20))
        y = int((i * 53 + math.sin(tempo * 0.025 + i) * 15) % 400)
        pygame.draw.circle(TELA, bioma["detail"], (x, y), 2)


def desenhar_chao(camera, bioma, plataformas):
    pygame.draw.rect(TELA, (13, 20, 30), (0, 585, LARGURA, 115))
    pygame.draw.rect(TELA, bioma["ground"], (0, 585, LARGURA, 12))
    pygame.draw.line(TELA, bioma["detail"], (0, 585), (LARGURA, 585), 3)

    for x in range(-80, LARGURA + 80, 70):
        xx = x - int(camera) % 70
        pygame.draw.line(
            TELA,
            tuple(max(0, c - 18) for c in bioma["ground"]),
            (xx, 600), (xx - 20, 690), 2
        )

    for plataforma in plataformas:
        rect = pygame.Rect(
            plataforma["x"] - camera,
            plataforma["y"],
            plataforma["w"],
            plataforma["h"]
        )

        if rect.right < 0 or rect.left > LARGURA:
            continue

        pygame.draw.rect(TELA, (15, 24, 38), (rect.x, rect.y + 7, rect.w, rect.h), border_radius=8)
        pygame.draw.rect(TELA, bioma["ground"], rect, border_radius=8)
        pygame.draw.rect(TELA, bioma["detail"], (rect.x, rect.y, rect.w, 6), border_radius=4)


# ==========================================
# BANGUELA ANIMADO
# ==========================================

def desenhar_banguela(rect, tempo, invulnerabilidade, andando=False, no_chao=True):

    x, y = rect.x, rect.y

    corpo = (17, 25, 43)
    sombra = (7, 12, 25)
    escamas = (38, 55, 79)
    brilho = (78, 100, 130)

    if invulnerabilidade > 0 and tempo % 8 < 4:
        corpo = (65, 110, 145)

    passo = math.sin(tempo * 0.35) if andando and no_chao else 0
    movimento_corpo = abs(passo) * 3 if andando and no_chao else 0
    movimento_asa = math.sin(tempo * 0.18) * 15

    cauda_movimento = math.sin(tempo * 0.15) * 7 if andando else math.sin(tempo * 0.07) * 3

    pygame.draw.polygon(TELA, sombra, [
        (x + 25, y + 37),
        (x - 25, y + 48 + cauda_movimento),
        (x - 65, y + 38 + cauda_movimento),
        (x - 40, y + 58 + cauda_movimento),
        (x + 32, y + 48)
    ])

    pygame.draw.polygon(TELA, (190, 55, 65), [
        (x - 57, y + 40 + cauda_movimento),
        (x - 78, y + 26 + cauda_movimento),
        (x - 73, y + 52 + cauda_movimento),
        (x - 48, y + 53)
    ])

    asa = [
        (x + 20, y + 29),
        (x - 5, y - 35 - movimento_asa),
        (x + 15, y - 12 - movimento_asa),
        (x + 40, y - 45 - movimento_asa),
        (x + 45, y + 22)
    ]

    pygame.draw.polygon(TELA, sombra, asa)
    pygame.draw.polygon(TELA, (30, 48, 73), asa)

    for ponto in [asa[1], asa[2], asa[3]]:
        pygame.draw.line(TELA, brilho, (x + 20, y + 29), ponto, 2)

    pygame.draw.ellipse(TELA, sombra, (x + 4, y + 22 + movimento_corpo, 65, 35))
    pygame.draw.ellipse(TELA, corpo, (x + 7, y + 16 + movimento_corpo, 60, 35))
    pygame.draw.ellipse(TELA, escamas, (x + 24, y + 35 + movimento_corpo, 35, 14))

    for i in range(4):
        pygame.draw.arc(
            TELA, brilho,
            (x + 25, y + 34 + i * 3 + movimento_corpo, 33, 10),
            0, math.pi, 1
        )

    pygame.draw.polygon(TELA, corpo, [
        (x + 48, y + 27 + movimento_corpo),
        (x + 62, y + 8 + movimento_corpo),
        (x + 73, y + 22 + movimento_corpo),
        (x + 61, y + 43 + movimento_corpo)
    ])

    pygame.draw.ellipse(TELA, sombra, (x + 48, y + 4 + movimento_corpo, 36, 28))
    pygame.draw.ellipse(TELA, corpo, (x + 48, y + 2 + movimento_corpo, 35, 25))
    pygame.draw.ellipse(TELA, corpo, (x + 69, y + 14 + movimento_corpo, 20, 13))
    pygame.draw.ellipse(TELA, brilho, (x + 76, y + 18 + movimento_corpo, 9, 4))

    pygame.draw.polygon(TELA, sombra, [
        (x + 57, y + 7 + movimento_corpo),
        (x + 50, y - 10 + movimento_corpo),
        (x + 67, y + 2 + movimento_corpo)
    ])

    pygame.draw.polygon(TELA, sombra, [
        (x + 72, y + 6 + movimento_corpo),
        (x + 86, y - 8 + movimento_corpo),
        (x + 80, y + 11 + movimento_corpo)
    ])

    pygame.draw.ellipse(TELA, (80, 210, 255), (x + 69, y + 8 + movimento_corpo, 11, 8))
    pygame.draw.circle(TELA, PRETO, (x + 77, y + 12 + int(movimento_corpo)), 3)
    pygame.draw.circle(TELA, BRANCO, (x + 74, y + 10 + int(movimento_corpo)), 2)
    pygame.draw.circle(TELA, PRETO, (x + 86, y + 19 + int(movimento_corpo)), 2)

    for i in range(6):
        px = x + 17 + i * 8
        py = y + 16 + math.sin(i) * 2 + movimento_corpo

        pygame.draw.polygon(TELA, brilho, [
            (px, py + 4), (px + 4, py - 4), (px + 8, py + 4)
        ])

    # PATAS ANIMADAS
    for indice, px in enumerate((x + 23, x + 54)):

        movimento_pata = passo * 7 * (1 if indice == 0 else -1)

        inicio_x = px + movimento_pata
        inicio_y = y + 39 + movimento_corpo

        pygame.draw.line(TELA, sombra, (inicio_x, inicio_y), (inicio_x - 2, y + 53), 7)
        pygame.draw.line(TELA, corpo, (inicio_x, inicio_y), (inicio_x - 2, y + 53), 5)

        for garra in range(3):
            pygame.draw.line(
                TELA, (180, 195, 210),
                (inicio_x - 3 + garra * 3, y + 52),
                (inicio_x - 5 + garra * 3, y + 56),
                2
            )

    pygame.draw.arc(TELA, brilho, (x + 13, y + 20, 45, 22), math.pi, math.tau, 2)


# ==========================================
# DRAGOES INIMIGOS
# ==========================================

def desenhar_dragao(rect, cor):

    x, y = rect.x, rect.y

    escuro = tuple(max(0, c - 55) for c in cor)
    claro = tuple(min(255, c + 45) for c in cor)

    movimento = math.sin(pygame.time.get_ticks() * 0.009 + x) * 10

    pygame.draw.polygon(TELA, escuro, [
        (x + 20, y + 30), (x - 15, y + 42),
        (x - 42, y + 31), (x - 20, y + 48),
        (x + 30, y + 42)
    ])

    asa = [
        (x + 28, y + 28),
        (x - 2, y - 24 - movimento),
        (x + 18, y - 9 - movimento),
        (x + 47, y - 31 - movimento),
        (x + 57, y + 29)
    ]

    pygame.draw.polygon(TELA, escuro, asa)
    pygame.draw.line(TELA, claro, asa[0], asa[1], 2)
    pygame.draw.line(TELA, claro, asa[0], asa[2], 2)
    pygame.draw.line(TELA, claro, asa[0], asa[3], 2)

    pygame.draw.ellipse(TELA, escuro, (x + 3, y + 17, 62, 37))
    pygame.draw.ellipse(TELA, cor, (x + 7, y + 13, 55, 32))
    pygame.draw.ellipse(TELA, claro, (x + 20, y + 32, 35, 12))

    pygame.draw.polygon(TELA, cor, [
        (x + 47, y + 30), (x + 58, y + 9),
        (x + 72, y + 25), (x + 61, y + 42)
    ])

    pygame.draw.ellipse(TELA, escuro, (x + 48, y + 5, 31, 26))
    pygame.draw.ellipse(TELA, cor, (x + 51, y + 5, 28, 22))
    pygame.draw.ellipse(TELA, claro, (x + 70, y + 16, 16, 10))

    pygame.draw.polygon(TELA, escuro, [
        (x + 57, y + 8), (x + 49, y - 7), (x + 66, y + 5)
    ])

    pygame.draw.polygon(TELA, escuro, [
        (x + 72, y + 8), (x + 85, y - 6), (x + 79, y + 13)
    ])

    pygame.draw.ellipse(TELA, (255, 220, 90), (x + 68, y + 10, 9, 7))
    pygame.draw.circle(TELA, PRETO, (x + 74, y + 13), 2)

    for linha in range(2):
        for coluna in range(5):
            px = x + 15 + coluna * 8
            py = y + 22 + linha * 9
            pygame.draw.circle(TELA, claro, (px, py), 2)

    for px in (x + 20, x + 52):
        pygame.draw.line(TELA, escuro, (px, y + 40), (px - 2, y + 53), 6)

        for garra in range(3):
            pygame.draw.line(
                TELA, (220, 220, 220),
                (px - 3 + garra * 3, y + 52),
                (px - 5 + garra * 3, y + 56), 2
            )

    for i in range(5):
        px = x + 16 + i * 9
        pygame.draw.polygon(TELA, escuro, [
            (px, y + 20), (px + 4, y + 8), (px + 8, y + 22)
        ])


# ==========================================
# CHEFE
# ==========================================

def desenhar_chefe(rect, cor, fase, tempo):

    x, y = rect.x, rect.y

    escuro = tuple(max(0, c - 45) for c in cor)
    movimento = math.sin(tempo * 0.045) * 8

    pygame.draw.polygon(TELA, escuro, [
        (x + 35, y + 95), (x - 55, y + 120),
        (x - 100, y + 90), (x - 60, y + 135),
        (x + 65, y + 115)
    ])

    pygame.draw.polygon(TELA, escuro, [
        (x + 55, y + 80), (x - 45, y - 50 - movimento),
        (x + 5, y - 10 - movimento),
        (x + 60, y - 65 - movimento), (x + 105, y + 65)
    ])

    pygame.draw.polygon(TELA, escuro, [
        (x + 125, y + 80), (x + 165, y - 65 - movimento),
        (x + 195, y - 5 - movimento), (x + 220, y + 110)
    ])

    pygame.draw.ellipse(TELA, escuro, (x + 20, y + 40, 160, 105))
    pygame.draw.ellipse(TELA, cor, (x + 30, y + 35, 145, 95))

    for i in range(5):
        pygame.draw.arc(
            TELA, (210, 170, 130),
            (x + 70, y + 65 + i * 12, 80, 35),
            0, math.pi, 2
        )

    pygame.draw.polygon(TELA, cor, [
        (x + 125, y + 75), (x + 150, y + 35),
        (x + 185, y + 65), (x + 165, y + 110)
    ])

    pygame.draw.ellipse(TELA, cor, (x + 135, y + 15, 70, 65))
    pygame.draw.ellipse(TELA, escuro, (x + 185, y + 48, 38, 25))

    pygame.draw.polygon(TELA, escuro, [
        (x + 155, y + 30), (x + 140, y - 20), (x + 172, y + 20)
    ])

    pygame.draw.polygon(TELA, escuro, [
        (x + 185, y + 28), (x + 210, y - 20), (x + 199, y + 40)
    ])

    pygame.draw.ellipse(TELA, (255, 235, 100), (x + 180, y + 35, 17, 12))
    pygame.draw.circle(TELA, PRETO, (x + 190, y + 41), 4)

    for i in range(8):
        px = x + 35 + i * 17
        pygame.draw.polygon(TELA, escuro, [
            (px, y + 48), (px + 8, y + 20), (px + 16, y + 52)
        ])

    if fase >= 2:
        pygame.draw.circle(TELA, (255, 220, 120), (x + 105, y + 85), 80, 2)


# ==========================================
# PARTICULAS
# ==========================================

def criar_particulas(particulas, x, y, cor, quantidade=8):

    for _ in range(quantidade):
        particulas.append({
            "x": float(x),
            "y": float(y),
            "vx": random.uniform(-4, 4),
            "vy": random.uniform(-5, 2),
            "vida": random.randint(15, 35),
            "cor": cor
        })


def atualizar_particulas(particulas):

    for p in particulas[:]:
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        p["vy"] += 0.15
        p["vida"] -= 1

        if p["vida"] <= 0:
            particulas.remove(p)


def desenhar_particulas(particulas, camera):

    for p in particulas:
        pygame.draw.circle(
            TELA,
            p["cor"],
            (int(p["x"] - camera), int(p["y"])),
            max(1, p["vida"] // 10)
        )


# ==========================================
# HUD
# ==========================================

def desenhar_hud(bioma, vidas, pontos, chefe_hp, chefe_max_hp,
                 chefe_ativo, chefe_derrotado, dificuldade, modo):

    painel(pygame.Rect(15, 15, 300, 105), borda=CIANO)

    escrever("BANGUELA ADVENTURE", FONT_MEDIA, BRANCO, (165, 42))
    escrever("Vidas: " + str(vidas), FONT_PEQUENA, (255, 110, 110), (95, 82))
    escrever("Pontos: " + str(pontos), FONT_PEQUENA, BRANCO, (215, 82))
    escrever(dificuldade + " | " + modo, FONT_PEQUENA, CIANO, (165, 104))

    escrever(bioma["name"], FONT_MEDIA, BRANCO, (600, 30))

    if chefe_ativo and not chefe_derrotado:
        painel(pygame.Rect(390, 65, 420, 58), borda=LARANJA)

        escrever(bioma["boss"], FONT_PEQUENA, BRANCO, (600, 82))

        largura = int(370 * max(0, chefe_hp) / chefe_max_hp)

        pygame.draw.rect(TELA, (50, 25, 25), (415, 98, 370, 12), border_radius=5)
        pygame.draw.rect(TELA, (245, 75, 65), (415, 98, largura, 12), border_radius=5)


# ==========================================
# JOGO
# ==========================================

def jogar(bioma, modo, dificuldade):

    config = DIFICULDADES[dificuldade]

    jogador = pygame.Rect(120, 480, 65, 55)

    largura_mundo = 5400
    camera = 0

    plataformas = []

    for x in range(300, largura_mundo - 300, 300):
        if random.random() < 0.72:
            plataformas.append({
                "x": x,
                "y": random.randint(410, 510),
                "w": random.randint(110, 190),
                "h": 20
            })

    espinhos = [
        pygame.Rect(x, 560, 65, 25)
        for x in range(650, largura_mundo - 400, 450)
    ]

    # PONTOS DE APARECIMENTO PROGRESSIVO
    pontos_spawn = []

    for i, x in enumerate(range(520, largura_mundo - 500, 390)):
        especie = ESPECIES[i % len(ESPECIES)]

        pontos_spawn.append({
            "x": x,
            "nome": especie[0],
            "cor": especie[1],
            "feito": False
        })

    inimigos = []

    chefe_x = largura_mundo - 480
    chefe = pygame.Rect(chefe_x, 390, 190, 130)

    chefe_max_hp = max(1, int(bioma["boss_hp"] * config["chefe"]))
    chefe_hp = chefe_max_hp

    chefe_ativo = False
    chefe_derrotado = False
    fase_chefe = 1

    tiros_jogador = []
    tiros_chefe = []
    particulas = []

    vidas = config["vidas"]
    pontos = 0

    velocidade_y = 0
    no_chao = False

    pulos_disponiveis = 2

    direcao = 1
    andando = False

    tempo_tiro = 0
    invulnerabilidade = 0

    tempo = 0
    tempo_sobrevivencia = 0

    while True:

        RELOGIO.tick(FPS)
        tempo += 1

        if modo == "Sobrevivencia":
            tempo_sobrevivencia += 1

        # EVENTOS
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    return None

                # PULO DUPLO
                if evento.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):

                    if pulos_disponiveis > 0:

                        velocidade_y = -13
                        pulos_disponiveis -= 1
                        no_chao = False

                        criar_particulas(
                            particulas,
                            jogador.centerx,
                            jogador.bottom,
                            CIANO,
                            8
                        )

                # ATIRAR
                if evento.key == pygame.K_x and tempo_tiro <= 0:

                    tiro = pygame.Rect(
                        jogador.centerx + direcao * 25,
                        jogador.centery - 5,
                        22, 10
                    )

                    tiros_jogador.append({
                        "rect": tiro,
                        "direcao": direcao
                    })

                    tempo_tiro = 12

        teclas = pygame.key.get_pressed()

        # MOVIMENTACAO
        velocidade = 5
        andando = False

        if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
            velocidade = 7

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogador.x -= velocidade
            direcao = -1
            andando = True

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogador.x += velocidade
            direcao = 1
            andando = True

        jogador.x = max(0, min(jogador.x, largura_mundo - 80))

        # GRAVIDADE
        velocidade_y += 0.65
        velocidade_y = min(velocidade_y, 15)

        antigo_bottom = jogador.bottom
        jogador.y += int(velocidade_y)

        no_chao = False

        # CHAO
        if jogador.bottom >= 585:
            jogador.bottom = 585
            velocidade_y = 0
            no_chao = True
            pulos_disponiveis = 2

        # PLATAFORMAS
        for plataforma in plataformas:

            r = pygame.Rect(
                plataforma["x"], plataforma["y"],
                plataforma["w"], plataforma["h"]
            )

            if (
                jogador.colliderect(r)
                and velocidade_y >= 0
                and antigo_bottom <= r.top + 8
            ):
                jogador.bottom = r.top
                velocidade_y = 0
                no_chao = True
                pulos_disponiveis = 2

        # CAMERA
        camera = max(
            0,
            min(jogador.centerx - LARGURA // 2, largura_mundo - LARGURA)
        )

        # DRAGOES APARECEM PROGRESSIVAMENTE
        for spawn in pontos_spawn:

            if not spawn["feito"]:

                distancia = spawn["x"] - jogador.centerx

                if -80 <= distancia <= 560:

                    altura_inicial = random.randint(240, 470)

                    inimigos.append({
                        "rect": pygame.Rect(
                            spawn["x"],
                            altura_inicial,
                            70, 50
                        ),
                        "nome": spawn["nome"],
                        "cor": spawn["cor"],
                        "velocidade": config["velocidade"],
                        "vida": 2,

                        # VOO INDIVIDUAL
                        "altura_base": altura_inicial,
                        "amplitude": random.randint(35, 95),
                        "fase_voo": random.uniform(0, math.pi * 2),
                        "velocidade_voo": random.uniform(0.025, 0.065)
                    })

                    spawn["feito"] = True

        # INIMIGOS VOANDO EM ALTURAS DIFERENTES
        for inimigo in inimigos[:]:

            r = inimigo["rect"]

            distancia = abs(jogador.centerx - r.centerx)

            # Perseguicao horizontal
            if distancia < 520:

                if r.centerx < jogador.centerx:
                    r.x += int(inimigo["velocidade"])

                elif r.centerx > jogador.centerx:
                    r.x -= int(inimigo["velocidade"])

            # Movimento vertical independente
            inimigo["fase_voo"] += inimigo["velocidade_voo"]

            movimento = math.sin(
                inimigo["fase_voo"]
            ) * inimigo["amplitude"]

            r.y = int(
                inimigo["altura_base"] + movimento
            )

            # Limites de voo
            r.y = max(150, min(r.y, 525))

            # Colisao com Banguela
            if r.colliderect(jogador) and invulnerabilidade <= 0:

                vidas -= 1
                invulnerabilidade = 80

                criar_particulas(
                    particulas,
                    jogador.centerx,
                    jogador.centery,
                    (255, 90, 80)
                )

        # ESPINHOS
        for espinho in espinhos:

            if jogador.colliderect(espinho) and invulnerabilidade <= 0:

                vidas -= 1
                invulnerabilidade = 80
                jogador.y -= 35
                velocidade_y = -5

                criar_particulas(
                    particulas,
                    jogador.centerx,
                    jogador.bottom,
                    LARANJA
                )

        # TIROS DO JOGADOR
        if tempo_tiro > 0:
            tempo_tiro -= 1

        for tiro in tiros_jogador[:]:

            r = tiro["rect"]
            r.x += tiro["direcao"] * 12

            if r.right < camera or r.left > camera + LARGURA:
                tiros_jogador.remove(tiro)
                continue

            acertou = False

            for inimigo in inimigos[:]:

                if r.colliderect(inimigo["rect"]):

                    inimigo["vida"] -= 1
                    acertou = True

                    criar_particulas(
                        particulas,
                        inimigo["rect"].centerx,
                        inimigo["rect"].centery,
                        inimigo["cor"]
                    )

                    if inimigo["vida"] <= 0:
                        inimigos.remove(inimigo)
                        pontos += 100

                    break

            if acertou:
                tiros_jogador.remove(tiro)
                continue

            if chefe_ativo and not chefe_derrotado and r.colliderect(chefe):

                chefe_hp -= 1
                tiros_jogador.remove(tiro)

                criar_particulas(
                    particulas,
                    chefe.centerx,
                    chefe.centery,
                    bioma["boss_color"]
                )

        # CHEFE
        if jogador.centerx >= chefe_x - 350:
            chefe_ativo = True

        if chefe_ativo and not chefe_derrotado:

            fase_chefe = 1

            if chefe_hp <= chefe_max_hp * 0.65:
                fase_chefe = 2

            if chefe_hp <= chefe_max_hp * 0.30:
                fase_chefe = 3

            chefe.y = 390 + int(math.sin(tempo * 0.045) * 28)

            intervalo = max(25, 85 - fase_chefe * 18)

            if tempo % intervalo == 0:
                tiros_chefe.append(
                    pygame.Rect(chefe.left - 25, chefe.centery, 25, 12)
                )

            if chefe_hp <= 0:

                chefe_derrotado = True
                pontos += 1000

                criar_particulas(
                    particulas,
                    chefe.centerx,
                    chefe.centery,
                    bioma["boss_color"],
                    35
                )

        # TIROS DO CHEFE
        for tiro in tiros_chefe[:]:

            tiro.x -= 7 + fase_chefe * 2

            if tiro.right < camera:
                tiros_chefe.remove(tiro)
                continue

            if tiro.colliderect(jogador) and invulnerabilidade <= 0:

                vidas -= config["dano"]
                invulnerabilidade = 80
                tiros_chefe.remove(tiro)

                criar_particulas(
                    particulas,
                    jogador.centerx,
                    jogador.centery,
                    (255, 100, 80)
                )

        # VITORIA
        if chefe_derrotado and jogador.centerx >= largura_mundo - 100:
            return "vitoria", pontos, vidas, tempo_sobrevivencia

        if modo == "Aventura" and jogador.centerx >= largura_mundo - 100 and not chefe_derrotado:
            jogador.centerx = largura_mundo - 120

        if modo == "Sobrevivencia" and tempo_sobrevivencia >= FPS * 180:
            return "vitoria", pontos, vidas, tempo_sobrevivencia

        if invulnerabilidade > 0:
            invulnerabilidade -= 1

        if vidas <= 0:
            return "derrota", pontos, vidas, tempo_sobrevivencia

        # DESENHO DO MUNDO
        desenhar_fundo(camera, bioma, tempo)
        desenhar_chao(camera, bioma, plataformas)

        # ESPINHOS
        for espinho in espinhos:

            x = espinho.x - camera

            if -100 < x < LARGURA + 100:

                pygame.draw.polygon(
                    TELA, (180, 55, 50),
                    [(x, 585), (x + 30, 550), (x + 65, 585)]
                )

        # INIMIGOS
        for inimigo in inimigos:

            r = inimigo["rect"].copy()
            r.x -= camera

            if -100 < r.x < LARGURA + 100:

                desenhar_dragao(r, inimigo["cor"])

                if abs(jogador.centerx - inimigo["rect"].centerx) < 520:
                    escrever(
                        inimigo["nome"],
                        FONT_PEQUENA,
                        BRANCO,
                        (r.centerx, r.y - 15)
                    )

        # CHEFE
        if chefe_ativo and not chefe_derrotado:

            chefe_tela = chefe.copy()
            chefe_tela.x -= camera

            desenhar_chefe(
                chefe_tela,
                bioma["boss_color"],
                fase_chefe,
                tempo
            )

        # TIROS
        for tiro in tiros_jogador:

            r = tiro["rect"].copy()
            r.x -= camera

            pygame.draw.ellipse(TELA, CIANO, r)
            pygame.draw.circle(TELA, BRANCO, r.center, 3)

        for tiro in tiros_chefe:

            r = tiro.copy()
            r.x -= camera

            pygame.draw.ellipse(TELA, LARANJA, r)

        # BANGUELA
        jogador_tela = jogador.copy()
        jogador_tela.x -= camera

        desenhar_banguela(
            jogador_tela,
            tempo,
            invulnerabilidade,
            andando,
            no_chao
        )

        # PARTICULAS
        atualizar_particulas(particulas)
        desenhar_particulas(particulas, camera)

        # HUD
        desenhar_hud(
            bioma,
            vidas,
            pontos,
            chefe_hp,
            chefe_max_hp,
            chefe_ativo,
            chefe_derrotado,
            dificuldade,
            modo
        )

        escrever(
            "A/D ou SETAS: mover | ESPACO: pular 2x | X: atirar | SHIFT: correr | ESC: menu",
            FONT_PEQUENA,
            BRANCO,
            (600, 675)
        )

        if chefe_derrotado:

            painel(
                pygame.Rect(410, 145, 380, 65),
                borda=(100, 255, 150)
            )

            escrever(
                "CHEFE DERROTADO! AVANCE!",
                FONT_MEDIA,
                (130, 255, 170),
                (600, 178)
            )

        pygame.display.flip()


# ==========================================
# TELA FINAL
# ==========================================

def tela_final(resultado, pontos, vidas, tempo_sobrevivencia):

    while True:

        mouse = pygame.mouse.get_pos()
        gradiente((5, 10, 25), (20, 35, 65))

        painel(pygame.Rect(300, 145, 600, 410))

        if resultado == "vitoria":
            escrever("VITORIA!", FONT_TITULO, (110, 255, 160), (600, 220))
        else:
            escrever("FIM DE JOGO", FONT_TITULO, (255, 95, 90), (600, 220))

        escrever("Pontuacao: " + str(pontos), FONT_GRANDE, BRANCO, (600, 305))
        escrever("Vidas restantes: " + str(vidas), FONT_MEDIA, BRANCO, (600, 350))

        segundos = tempo_sobrevivencia // FPS

        escrever(
            f"Tempo: {segundos // 60:02}:{segundos % 60:02}",
            FONT_MEDIA,
            CIANO,
            (600, 390)
        )

        novamente = pygame.Rect(420, 445, 360, 55)
        desenhar_botao(novamente, "VOLTAR AO MENU", mouse, True)

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                if novamente.collidepoint(mouse):
                    return

            if evento.type == pygame.KEYDOWN:

                if evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    return

        pygame.display.flip()
        RELOGIO.tick(FPS)


# ==========================================
# INICIO
# ==========================================

def main():

    while True:

        bioma, modo, dificuldade = menu()

        resultado = jogar(bioma, modo, dificuldade)

        if resultado is None:
            continue

        status, pontos, vidas, tempo_sobrevivencia = resultado

        tela_final(
            status,
            pontos,
            vidas,
            tempo_sobrevivencia
        )


if __name__ == "__main__":
    main()
