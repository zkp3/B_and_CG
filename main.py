import sys, pygame as pyg, random

def print_text(size, center:bool, text:str, color, x, y, surface):
    font = pyg.font.Font(None, 36)
    text = font.render(text, 1, color)
    return scrn.blit(text, (x, y))

pyg.init()

wid = 1280
hei = 700
wid_div = wid/2
hei_div = hei/2
pyg.display.set_caption('PING_COIN_GAME')
scrn = pyg.display.set_mode((wid, hei))
Xspeed_circle = float(input('Скорость шарика: '))
Yspeed_circle = Xspeed_circle
Xcircle = wid_div
Ycircle = hei_div
accelerat = float(input('На сколько ускорется игра при сборе монеты: '))
max_coins = int(input('Максимальное количество монет: '))
size = 40
kol_vo_coin = random.randint(0, max_coins)
score = 0

coins = [(random.randint(size, wid - size), random.randint(size, hei - size)) for i in range(kol_vo_coin)]
run = 'game'

while run == 'game':
    keys = pyg.key.get_pressed()
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                run = False
    scrn.fill((0,0,0))
    pyg.draw.circle(scrn, (0,0, 255), (Xcircle, Ycircle), size/2)

    #создаем список coin на основе координат из списка coins
    for coin in coins:
        #координаты именно той монеты, которая сейчас
        Xcoin, Ycoin = coin
        #области в которых находятся объекты
        coin_rect = pyg.Rect(Xcoin, Ycoin, size, size)
        circle_rect = pyg.Rect(Xcircle, Ycircle, size, size)
        pyg.draw.circle(scrn, (255, 255, 0), (Xcoin, Ycoin), size / 2)
        #проверка на касание
        if circle_rect.colliderect(coin_rect):
            score += 1
            #удаление координат монетки, чтобы она больше не рисовалась
            #при следующем повторении цикла
            coins.remove(coin)

    #изменение координат шарика
    Xcircle += Xspeed_circle
    Ycircle += Yspeed_circle
    #изменение скорости на отрицательную при нажатии на кнопки
    if keys[pyg.K_UP]:
        if Yspeed_circle > 0:
            Yspeed_circle = -Yspeed_circle
    elif keys[pyg.K_DOWN]:
        if Yspeed_circle < 0:
            Yspeed_circle = -Yspeed_circle
    if keys[pyg.K_LEFT]:
        if Xspeed_circle > 0:
            Xspeed_circle = -Xspeed_circle
    elif keys[pyg.K_RIGHT]:
        if Xspeed_circle < 0:
            Xspeed_circle = -Xspeed_circle

    #переход к конечному экрану
    if Xcircle > wid or Xcircle < 0 or Ycircle > hei or Ycircle < 0:
        run = 'gameover'
    elif score == kol_vo_coin:
        run = 'win'

    pyg.time.Clock().tick(120)
    pyg.display.flip()

while run == 'gameover':
    keys = pyg.key.get_pressed()
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                run = False
    scrn.fill((0,0,0))
    print_text(90, True, 'GAME-OVER! :(', (255, 0, 0), wid_div, hei_div, scrn)
while run == 'win':
    keys = pyg.key.get_pressed()
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                run = False
    scrn.fill((0,0,0))
    print_text(90, True, 'YOU WIN! :)', (0, 255, 255), wid_div, hei_div, scrn)

pyg.quit()
sys.exit()