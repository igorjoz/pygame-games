import pygame
from Platforma import Platforma
from Kulka import Kulka
from Klocek import Klocek


SZEROKOSC_EKRANU = 1024
WYSOKOSC_EKRANU = 800
poziom = 0
zycia = 3

pygame.init()
pygame.font.init()

czcionka = pygame.font.SysFont('Comic Sans MS', 24)
ekran = pygame.display.set_mode([SZEROKOSC_EKRANU, WYSOKOSC_EKRANU])
zegar = pygame.time.Clock()
obraz_tla = pygame.image.load("images/background.png")

poziom1 = [[0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
  [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
  [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
  [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

poziom2 = [[0, 0, 1, 2, 3, 3, 2, 1, 0, 0],
  [0, 1, 1, 1, 2, 2, 1, 1, 1, 0],
  [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
  [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
  [0, 0, 2, 0, 0, 0, 0, 2, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 2, 0, 2, 0, 0, 2, 0, 2, 0]]

poziom3 = [[2, 3, 2, 2, 2, 2, 2, 2, 3, 2],
  [2, 1, 3, 1, 1, 1, 1, 3, 1, 2],
  [2, 3, 1, 3, 1, 1, 3, 1, 3, 2],
  [3, 2, 2, 2, 3, 3, 2, 2, 2, 3],
  [0, 0, 2, 2, 3, 3, 2, 2, 0, 0],
  [0, 0, 2, 0, 3, 3, 0, 2, 0, 0],
  [0, 0, 3, 0, 3, 3, 0, 3, 0, 0]]

klocki = pygame.sprite.Group()

def dodaj_klocki():
    wczytany_poziom = None
    if poziom == 0:
        wczytany_poziom = poziom1
    if poziom == 1:
        wczytany_poziom = poziom2
    if poziom == 2:
        wczytany_poziom = poziom3
 
    for i in range(10):
        for j in range(7):
            if wczytany_poziom[j][i] != 0:
                klocek = Klocek(32+i*96, 32+j*48, wczytany_poziom[j][i])
                klocki.add(klocek)
dodaj_klocki()

platforma = Platforma()
kulka = Kulka()

gra_dziala = True
while gra_dziala:
    for zdarzenie in pygame.event.get():
        if zdarzenie.type == pygame.KEYDOWN:
            if zdarzenie.key == pygame.K_ESCAPE:
                gra_dziala = False
        elif zdarzenie.type == pygame.QUIT:
            gra_dziala = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        platforma.ruszaj_platforma(-1)
    if keys[pygame.K_d]:
        platforma.ruszaj_platforma(1)

    if len(klocki.sprites()) == 0:
        poziom += 1
    if poziom >= 3:
        break
    kulka.zresetuj_pozycje()
    platforma.zresetuj_pozycje()
    dodaj_klocki()

    kulka.aktualizuj(platforma, klocki)

    if kulka.przegrana:
        zycia -= 1
        if zycia <= 0:
            break
        kulka.zresetuj_pozycje()
        platforma.zresetuj_pozycje()

    klocki.update()
    platforma.aktualizuj()

    ekran.blit(obraz_tla, (0,0))     # 1. zmiana kolejności - wyświetlenie obrazu najpierw, a dopiero później klocków na nim 

    for brick in klocki:
        ekran.blit(brick.obraz, brick.pozycja)

    ekran.blit(platforma.obraz_platformy, platforma.pozycja)
    ekran.blit(kulka.obraz_kulki, kulka.pozycja)

    tekst1 = czcionka.render(f'Poziom: {poziom + 1}', False, (255, 0, 255))    # 2. wyswietlenie nr poziomu
    tekst2 = czcionka.render(f'Życia: {zycia}', False, (0, 255, 0)) 
    ekran.blit(tekst1, (20, 20))                                               # 3. poziom sobie wyświetlam po lewej
    ekran.blit(tekst2, (SZEROKOSC_EKRANU - 120, 20))                           #    życia przeniosłam na prawo

    pygame.display.flip()
    zegar.tick(30)

pygame.quit()