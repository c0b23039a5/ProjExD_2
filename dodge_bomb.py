import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内か外かを判定
    引数:こうかとんRectかばくだんRect
    戻り値:真理値タプル（横方向判定結果、縦方向判定結果）
    """
    yoko, tate = True, True
    if rct.left < 0 or rct.right > WIDTH:
        yoko = False
    if rct.top < 0 or rct.bottom > HEIGHT:
        tate = False
    return (yoko, tate)


def gameover(screen: pg.Surface) ->None:
    bg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bg_img,0,WIDTH)
    bg_rct = bg_img.get_rect()
    go_img = pg.image.load("fig/8.png")
    go_rct = go_img.get_rect()
    font = pg.font.Font(None,80)
    txt = font.render("Game Over",True,(255,255,255))
    screen.blit(bg_rct,[0,0])
    screen.blit(txt,[WIDTH/2,HEIGHT/2])
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface],list[int]]:
    accs = [a for a in range(1,11)]

    return (accs,accs)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bb_img = pg.Surface((20, 20))  # 爆弾用の型のサーフェース
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bg_img = pg.image.load("fig/pg_bg.jpg")
    vx, vy = +5, +5  # 爆弾速度ベクトル
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        if kk_rct.colliderect(bb_rct):
          gameover(screen)  # ゲームオーバー
        screen.blit(bg_img, [0, 0])

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)

        # こうかとんが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_imgs,bb_accs=init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500,9)]
        bb_img=bb_imgs[min(tmr//500,9)]


        for r in range(1,11):
            bb_img = pg.Surface((20*r,20*r))
            pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)

        yoko,tate = check_bound(bb_rct)
        if not yoko:
            avx *= -1
        if not tate:
            vy *= -1

        bb_rct.move_ip(avx, vy)


        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
