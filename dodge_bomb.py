import sys
import random
import pygame as pg



WIDTH, HEIGHT = 1600, 900

delat={
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(+5,0)
}

def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向・縦方向の真理値タプル（True：画面内／False：画面外）
    Rectオブジェクトのleft, right, top, bottomの値から画面内・外を判断する
    """
    yoko,tate = True,True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return (yoko,tate)
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img2 = pg.image.load("ex02/fig/8.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_f = pg.transform.flip(kk_img,True,False)
    kk_imgs = {(+5,0):kk_img_f,  # 右方向のこうかとん
                (+5,-5):pg.transform.rotozoom(kk_img_f,45,1.0),  #右上方向のこうかとん
               (0,-5):pg.transform.rotozoom(kk_img_f,90,1.0),  #上方向のこうかとん
               (+5,+5):pg.transform.rotozoom(kk_img_f,-45,1.0),  #右下方向のこうかとん
               (0,+5):pg.transform.rotozoom(kk_img_f,-90,1.0),  #下方向のこうかとん
               (-5,+5):pg.transform.rotozoom(kk_img,45,1.0),  #左下方向のこうかとん
               (-5,0):kk_img,  # 左方向のこうかとん
               (-5,-5):pg.transform.rotozoom(kk_img,-45,1.0),  #左上方向のこうかとん
                }
    kk_img = kk_imgs[+5,0]
    kk_img2 = pg.transform.rotozoom(kk_img2, 0, 2.0)
    bb_img = pg.Surface((20, 20))   # 練習１：透明のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))  # 練習１：黒い部分を透明にする
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) 
    accs = [a for a in range(1,11)]
    kk_rct= kk_img.get_rect()
    kk_rct.center = 900,400
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
        
    vx = +5
    vy = +5   
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            screen.blit(kk_img2,kk_rct)
            pg.display.update()
            print("ゲームオーバー")
            return
        key_lst = pg.key.get_pressed()
        sum_mv= [0,0]
        for k,tpl in delat.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        screen.blit(bg_img, [0, 0])

        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(sum_mv[0], -sum_mv[1])

        kk_0 = 0
        kk_1 = 0
        for k,mv in delat.items():
            if key_lst[k]:
                kk_0 = kk_0 + mv[0]
                kk_1 = kk_1 + mv[1]
            
            if kk_0 != 0 or kk_1 !=0:
                kk_img=kk_imgs[kk_0,kk_1]
            
        screen.blit(kk_img, kk_rct)
        avx,avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx,avy)

        yoko,tate= check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img,bb_rct)
        bb_rct.move_ip(vx,vy)
        pg.display.update()
        tmr += 50
        clock.tick(10)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()