import sys, pygame as pyg, random, os, settings
pyg.init()
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

main_dir = os.path.dirname(__file__)

old_speed = Yspeed_circle = Xspeed_circle = settings.speed_circle
accelerat = settings.accelerat
max_coins = settings.max_coins

display_info = pyg.display.Info()
wid = display_info.current_w
hei = display_info.current_h

#середина экрана
wid_div = wid // 2
hei_div = hei // 2

#получение размеров обоев и изменение их размеров
if wid < hei:
    size = wid // 20
else:
    size = hei // 20

bgWid, bgHei = pyg.image.load(main_dir + '/background.png').get_size()
scale_width = wid / bgWid
scale_height = hei / bgHei
scale_factor = min(scale_width, scale_height)
bgWid = int(bgWid * scale_factor)
bgHei = int(bgHei * scale_factor)

#нач. координаты шарика
Xcircle = wid_div
Ycircle = hei_div

#подстраивание максимальных значений под размер экрана, чтобы игрок не мог выставлять слишком большие
max_speed = scale_factor*13
max_accelerat = scale_factor * 2
max_max_coins = int(scale_factor * 150)

#генерирация рандомного количества монет
kol_vo_coin = random.randint(0, max_coins)

#трансформация
coin_sprite = transform_img(main_dir + '/coin_sprite.png', (size, size))
circle_sprite = transform_img(main_dir + '/circle_sprite.png', (size, size))
background_sprite = transform_img((main_dir + '/background.png'), (bgWid, bgHei))

bgX, bgY = (wid - bgWid) // 2, (hei - bgHei) // 2

#генерирация рандомных координат для определённого количества монет
coins = [(random.randint(bgX, bgX+bgWid-size), random.randint(bgY, bgY+bgHei-size)) for i in range(kol_vo_coin)]
#создание пустых переменных
score = m_menu_delay = settings_delay = string_number = 0

#создание окна
pyg.display.set_caption('B&CG')
scrn = pyg.display.set_mode((wid, hei), pyg.NOFRAME)

#music
music_path = main_dir + '/music.mp3'
pyg.mixer.music.load(music_path)
pyg.mixer_music.play(-1)
m_menu_rgb = (255, 0, 0)
run = 'menu'
print('start game loop...')
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

            if event.key == pyg.K_LSHIFT or event.key == pyg.K_RSHIFT:
                score = 0
                Xcircle = wid_div
                Ycircle = hei_div
                Yspeed_circle = Xspeed_circle = old_speed
                kol_vo_coin = random.randint(0, max_coins)
                coins = [(random.randint(bgX, bgX + bgWid - size), random.randint(bgY, bgY + bgHei - size)) for i in range(kol_vo_coin)]
                timeTextReset = 0
                run = 'menu'
                string_number = 0
                print('run = menu')

            if run == 'menu':
                if string_number > 0 and event.key == pyg.K_UP:
                    string_number -= 1
                elif string_number < 3 - 1 and event.key == pyg.K_DOWN:
                    string_number += 1
                if string_number == 0:
                    if event.key == pyg.K_RETURN:
                        run = 'game'
                        print('run = game')
                if string_number == 1:
                    if event.key == pyg.K_RETURN:
                        run = 'settings'
                        string_number = 0
                        print('run = settings')
                elif string_number == 2:
                    if event.key == pyg.K_RETURN:
                        print('Exit...')
                        pyg.quit()
                        sys.exit()
            if run == 'settings':
                if string_number > 0 and event.key == pyg.K_UP:
                    string_number -= 1
                elif string_number < 3 - 1 and event.key == pyg.K_DOWN:
                    string_number += 1
    #для мигающих разными цветами надписей
    if m_menu_delay > 0:
        m_menu_delay -= 1
    elif m_menu_delay == 0:
        if m_menu_rgb == (255, 0, 0):
            m_menu_rgb = (0, 255, 0)
        elif m_menu_rgb == (0, 255, 0):
            m_menu_rgb = (0, 0, 255)
        elif m_menu_rgb == (0, 0, 255):
            m_menu_rgb = (255, 0, 0)
        m_menu_delay = 5

    #запуск меню
    if run == 'menu':
        scrn.fill((0, 0, 0))
        scrn.blit(background_sprite, (bgX, bgY))
        print_text(size * 2, 'SHIFT-MENU', (m_menu_rgb), wid_div, hei_div - size * 5, scrn)
        if string_number == 0:
            print_text(size * 2, 'START', (255, 255, 0), wid_div, hei_div - size * 2.5, scrn)
            print_text(size * 2, 'SETTINGS', (255, 255, 255), wid_div, hei_div, scrn)
            print_text(size * 2, 'ESC-EXIT', (255, 255, 255), wid_div, hei_div + size * 2.5, scrn)
        elif string_number == 1:
            print_text(size * 2, 'START', (255, 255, 255), wid_div, hei_div - size * 2.5, scrn)
            print_text(size * 2, 'SETTINGS', (255, 255, 0), wid_div, hei_div, scrn)
            print_text(size * 2, 'ESC-EXIT', (255, 255, 255), wid_div, hei_div + size * 2.5, scrn)
        else:
            print_text(size * 2, 'START', (255, 255, 255), wid_div, hei_div - size * 2.5, scrn)
            print_text(size * 2, 'SETTINGS', (255, 255, 255), wid_div, hei_div, scrn)
            print_text(size * 2, 'ESC-EXIT', (255, 255, 0), wid_div, hei_div + size * 2.5, scrn)
    #запуск настроек игры
    elif run == 'settings':
        if settings_delay > 0:
            settings_delay -= 1
        scrn.fill((0, 0, 0))
        scrn.blit(background_sprite, (bgX, bgY))
        if keys[pyg.K_LEFT] or keys[pyg.K_RIGHT] or keys[pyg.K_d]:
            file_sett_path = main_dir + '/settings.py'
            file_sett = open(file_sett_path, 'w')
            file_sett.close()
            file_sett = open(file_sett_path, 'w')
            file_sett.write(
                f'speed_circle = {old_speed}\n'
                f'accelerat = {accelerat}\n'
                f'max_coins = {max_coins}\n')
        print_text(size * 2, 'D-DEFAULT', (m_menu_rgb), wid_div, hei_div - size * 4.5, scrn)
        if string_number == 0:
            if keys[pyg.K_LEFT] and settings_delay == 0 and old_speed > 0:
                Yspeed_circle = Xspeed_circle = old_speed = round(old_speed - 0.1, 1)
                settings_delay = 8
            elif keys[pyg.K_RIGHT] and settings_delay == 0 and old_speed < max_speed:
                Yspeed_circle = Xspeed_circle = old_speed = round(old_speed + 0.1, 1)
                settings_delay = 8
            elif keys[pyg.K_d]:
                Yspeed_circle = Xspeed_circle = old_speed = 0.0
            print_text(size * 2, f'BallSpeed:<{(int(old_speed*10))}>', (255, 255, 0), wid_div, hei_div - size * 2.5, scrn)
            print_text(size * 2, f'MaxCoins:<{max_coins}>', (255, 255, 255), wid_div, hei_div, scrn)
            print_text(size * 2, f'Acceleration:<{(int(accelerat*10))}>', (255, 255, 255), wid_div, hei_div + size * 2.5, scrn)

        elif string_number == 1:
            if keys[pyg.K_LEFT] and settings_delay == 0 and max_coins > 0:
                max_coins -= 1
                settings_delay = 8
            elif keys[pyg.K_RIGHT] and settings_delay == 0 and max_coins < max_max_coins:
                max_coins += 1
                settings_delay = 8
            elif keys[pyg.K_d]:
                max_coins = 0
            print_text(size * 2, f'BallSpeed:<{(int(old_speed*10))}>', (255, 255, 255), wid_div, hei_div - size * 2.5, scrn)
            print_text(size * 2, f'MaxCoins:<{max_coins}>', (255, 255, 0), wid_div, hei_div, scrn)
            print_text(size * 2, f'Acceleration:<{(int(accelerat*10))}>', (255, 255, 255), wid_div, hei_div + size * 2.5, scrn)

        else:
            if keys[pyg.K_LEFT] and settings_delay == 0 and accelerat > 0:
                accelerat = round(accelerat - 0.1, 1)
                settings_delay = 8
            elif keys[pyg.K_RIGHT] and settings_delay == 0 and accelerat < max_accelerat:
                accelerat = round(accelerat + 0.1, 1)
                settings_delay = 8
            elif keys[pyg.K_d]:
                accelerat = 0.0
            print_text(size * 2, f'BallSpeed:<{(int(old_speed*10))}>', (255, 255, 255), wid_div, hei_div - size * 2.5, scrn)
            print_text(size * 2, f'MaxCoins:<{max_coins}>', (255, 255, 255), wid_div, hei_div, scrn)
            print_text(size * 2, f'Acceleration:<{(int(accelerat*10))}>', (255, 255, 0), wid_div, hei_div + size * 2.5, scrn)
    #запуск самой игры
    elif run == 'game':
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
                print('coin removed')

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
            print('run = gameover')
        elif score == kol_vo_coin:
            run = 'win'
            print('run = win')

    elif run == 'gameover':
        scrn.fill((0,0,0))
        scrn.blit(background_sprite, (bgX, bgY))
        print_text(size*2, 'GAME-OVER! :(', (255, 0, 0), wid_div, hei_div, scrn)
    elif run == 'win':
        scrn.fill((0,0,0))
        scrn.blit(background_sprite, (bgX, bgY))
        print_text(size*2, 'YOU WIN! :)', (0, 255, 255), wid_div, hei_div, scrn)
    pyg.time.Clock().tick(120)
    pyg.display.flip()
