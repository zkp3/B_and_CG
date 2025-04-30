import sys, pygame as pyg, random as rnd, os, importlib as ilib

# типа нужно чтобы фотография и main.py были в одной папке.
# Поизменяйте wid и hei. Короче, я сделал чтобы они под размер экрана настраивались,
# с рамкой (то есть они не будут растянуты.
# '/testroom_background1.png' ()должна называться как и
# файл фотографии, которая в одной папке с главным py.

main_dir = os.path.dirname(__file__)
print(os.path.dirname(__file__))

def bg_transf(width, height, bg_path):
    bg = pyg.image.load(bg_path)
    old_bg_wid = bg.get_width()
    old_bg_hei = bg.get_height()
    scrn_ratio = wid / hei
    bg_ratio = old_bg_wid / old_bg_hei

    if bg_ratio > scrn_ratio:
        bg_wid = wid
        bg_hei = wid / bg_ratio
    else:
        bg_hei = hei
        bg_wid = hei * bg_ratio
    bg = pyg.transform.scale(bg, (bg_wid, bg_hei))
    x, y = (width - bg_wid)/2, (height - bg_hei)/2
    return bg, x, y, old_bg_wid, old_bg_hei
def sprite_transf(sprite_path, bg, scale_factor):
    sprite = pyg.image.load(sprite_path)
    bg_wid = bg.get_width()
    bg_hei = bg.get_height()
    sprite_wid = sprite.get_width()
    sprite_hei = sprite.get_height()
    sprite_ratio = sprite_wid / sprite_hei
    if (bg_wid / bg_hei) > sprite_ratio:
        sprite_wid = bg_wid * scale_factor
        sprite_hei = sprite_wid / sprite_ratio
    else:
        sprite_hei = bg_hei * scale_factor
        sprite_wid = sprite_hei * sprite_ratio
    sprite = pyg.transform.scale(sprite, (sprite_wid, sprite_hei))
    return sprite


################

fscrn = 1
wid = 1280
hei = 900

#######################3

pyg.init()
wind_nm = 'TEST-ROOM'
pyg.display.set_caption(wind_nm)
if fscrn:
    inf_diply = pyg.display.Info()
    wid = inf_diply.current_w
    hei = inf_diply.current_h
    scrn = pyg.display.set_mode((wid, hei), pyg.FULLSCREEN, pyg.NOFRAME)
elif fscrn == False:
    scrn = pyg.display.set_mode((wid, hei))

#########################################3

wid_div = wid / 2
hei_div = hei / 2
main = 'menu'
test_room_bg_path = main_dir + '/testroom_background.png'
plyrSprite_path = main_dir + '/player_sprite.png'
plyrX = 50
plyrY = 190

#################################
test_room_bg, bg_x, bg_y, old_bg_wid, old_bg_hei = bg_transf(wid, hei, test_room_bg_path)
bg_wid = test_room_bg.get_width()
bg_hei = test_room_bg.get_height()
plyrSprite = sprite_transf(plyrSprite_path, test_room_bg, 0.1)
###################################
while True:
    keys = pyg.key.get_pressed()
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            pyg.quit()
            sys.exit()

    scrn.blit(test_room_bg, (bg_x, bg_y))
    scrn.blit(plyrSprite, (bg_wid / old_bg_wid * plyrX + ((wid-bg_wid)/2), bg_hei / old_bg_hei * plyrY + ((hei-bg_hei)/2)))

    pyg.time.Clock().tick(120)
    pyg.display.flip()
