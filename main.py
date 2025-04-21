import sys, pygame as pyg, random, os
main_dir = os.path.dirname(__file__)

def print_text(size, text:str, color, x, y, surface):
    font = pyg.font.Font(None, size)
    text = font.render(text, 1, color)
    xyText = text.get_rect(center=(x, y))
    return scrn.blit(text, (xyText))

def transform_img(path:str, new_size):
    new_imgX, new_imgY = new_size
    img = pyg.image.load(path)
    img = pyg.transform.scale(img, (new_imgX, new_imgY))
    return img

pyg.init()

display_info = pyg.display.Info()
wid = display_info.current_w
hei = display_info.current_h
wid_div = wid/2
hei_div = hei/2

Xspeed_circle = float(input('Скорость шарика: '))
Yspeed_circle = Xspeed_circle
Xcircle = wid_div
Ycircle = hei_div
accelerat = float(input('На сколько ускорется игра при сборе монеты: '))
max_coins = int(input('Максимальное количество монет: '))
if wid < hei:
    size = wid // 20
else: size = hei // 20

kol_vo_coin = random.randint(0, max_coins)
score = 0

coin_sprite = transform_img(main_dir + '/coin_sprite.png', (size, size))
circle_sprite = transform_img(main_dir + '/circle_sprite.png', (size, size))
background_sprite = transform_img((main_dir + '/background.jpg'), (wid, hei))

pyg.display.set_caption('PING_COIN_GAME')
scrn = pyg.display.set_mode((wid, hei), pyg.NOFRAME)

coins = [(random.randint(0, wid - size), random.randint(0, hei - size)) for i in range(kol_vo_coin)]
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
    scrn.blit(background_sprite, (0,0))
    scrn.blit(circle_sprite, (Xcircle, Ycircle))

    #создаем список coin на основе координат из списка coins
    for coin in coins:
        #координаты именно той монеты, которая сейчас
        Xcoin, Ycoin = coin
        #области в которых находятся объекты
        coin_rect = pyg.Rect(Xcoin, Ycoin, size, size)
        circle_rect = pyg.Rect(Xcircle, Ycircle, size, size)
        scrn.blit(coin_sprite, (Xcoin, Ycoin))
        #проверка на касание
        if circle_rect.colliderect(coin_rect):
            score += 1
            Xspeed_circle += -accelerat if Xspeed_circle < 0 else accelerat
            Yspeed_circle += -accelerat if Yspeed_circle < 0 else accelerat
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
    print_text(size*2, 'GAME-OVER! :(', (255, 0, 0), wid_div, hei_div, scrn)
    pyg.time.Clock().tick(120)
    pyg.display.flip()
while run == 'win':
    keys = pyg.key.get_pressed()
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            run = False
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                run = False
    scrn.fill((0,0,0))
    print_text(size*2, 'YOU WIN! :)', (0, 255, 255), wid_div, hei_div, scrn)
    pyg.time.Clock().tick(120)
    pyg.display.flip()
pyg.quit()
sys.exit()
