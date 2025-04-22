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
wid_div = wid//2
hei_div = hei//2

Xspeed_circle = float(input('\nСкорость шарика\n'
                            '(к приеру: для экрана размером 1280 на 900\n'
                            'лучше используйте скорость 1-5): '))
old_speed = Xspeed_circle
Yspeed_circle = Xspeed_circle
Xcircle = wid_div
Ycircle = hei_div
accelerat = float(input('\nНа сколько ускорется игра при сборе монеты\n'
                        '(можно писать числа с плавающей точкой): '))
max_coins = int(input('\nМаксимальное количество монет\n'
                      '(будет рандомное колличество монет от 0 до...): '))
if wid < hei:
    size = wid // 20
else:
    size = hei // 20

bgWid, bgHei = pyg.image.load(main_dir + '/background.jpg').get_size()
scale_width = wid / bgWid
scale_height = hei / bgHei
#min выводит минимальное значение из данных
scale_factor = min(scale_width, scale_height)
bgWid = int(bgWid * scale_factor)
bgHei = int(bgHei * scale_factor)

kol_vo_coin = random.randint(0, max_coins)
score = 0

coin_sprite = transform_img(main_dir + '/coin_sprite.png', (size, size))
circle_sprite = transform_img(main_dir + '/circle_sprite.png', (size, size))
background_sprite = transform_img((main_dir + '/background.jpg'), (bgWid, bgHei))
bgX = (wid - bgWid) // 2
bgY = (hei - bgHei) // 2
pyg.display.set_caption('PING_COIN_GAME')
scrn = pyg.display.set_mode((wid, hei), pyg.NOFRAME)

coins = [(random.randint(bgX, bgX+bgWid-size), random.randint(bgY, bgY+bgHei-size)) for i in range(kol_vo_coin)]
run = 'game'

while True:
    keys = pyg.key.get_pressed()
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()
        elif event.type == pyg.KEYDOWN:
            if event.key == pyg.K_ESCAPE:
                pyg.quit()
                sys.exit()
    if run == 'game':
        if keys[pyg.K_r]:
            score = 0
            Xcircle = wid_div
            Ycircle = hei_div
            Yspeed_circle = Xspeed_circle = old_speed
            kol_vo_coin = random.randint(0, max_coins)
            coins = [(random.randint(bgX, bgX + bgWid - size), random.randint(bgY, bgY + bgHei - size)) for i in range(kol_vo_coin)]
        scrn.fill((0, 0, 0))
        scrn.blit(background_sprite, (bgX, bgY))
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
        if Xcircle > bgX+bgWid - size or Xcircle < bgX or Ycircle > bgY+bgHei - size or Ycircle < bgY:
            run = 'gameover'
        elif score == kol_vo_coin:
            run = 'win'

    elif run == 'gameover':
        scrn.fill((0,0,0))
        print_text(size*2, 'GAME-OVER! :(', (255, 0, 0), wid_div, hei_div, scrn)
        if keys[pyg.K_r]:
            score = 0
            Xcircle = wid_div
            Ycircle = hei_div
            Yspeed_circle = Xspeed_circle = old_speed
            kol_vo_coin = random.randint(0, max_coins)
            coins = [(random.randint(bgX, bgX + bgWid - size), random.randint(bgY, bgY + bgHei - size)) for i in range(kol_vo_coin)]
            run = 'game'
    elif run == 'win':
        scrn.fill((0,0,0))
        print_text(size*2, 'YOU WIN! :)', (0, 255, 255), wid_div, hei_div, scrn)
        if keys[pyg.K_r]:
            score = 0
            Xcircle = wid_div
            Ycircle = hei_div
            Yspeed_circle = Xspeed_circle = old_speed
            kol_vo_coin = random.randint(0, max_coins)
            coins = [(random.randint(bgX, bgX + bgWid - size), random.randint(bgY, bgY + bgHei - size)) for i in range(kol_vo_coin)]
            run = 'game'
    pyg.time.Clock().tick(120)
    pyg.display.flip()
