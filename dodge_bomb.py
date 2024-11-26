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
    """
    ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表示し，泣いているこうかとん画像を貼り付ける関数
    引数:screen
    戻り値:なし
    """
    bg_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bg_img,0,pg.Rect(0,0,WIDTH, HEIGHT))
    bg_rct = bg_img.get_rect()
    go_img = pg.image.load("fig/8.png")
    go_rct = go_img.get_rect()
    font = pg.font.Font(None,80)
    txt = font.render("Game Over",True,(255,255,255))
    screen.blit(bg_img,[0,0])
    screen.blit(txt,[WIDTH/2,HEIGHT/2])
    go_rct.move_ip((200,HEIGHT/2))
    screen.blit(go_img,go_rct)

    pg.display.update()
    time.sleep(5)
    return


def init_bb_imgs() -> tuple[list[pg.Surface],list[int]]:
    """
    サイズの異なる爆弾Surfaceを要素としたリストと加速度リスト
    引数:なし
    戻り値:タプル（リスト[爆弾の大きさでサーフェース]、リスト[加速度]）
    """
    accs = [a for a in range(1,11)]
    bb_accs=[]

    for r in range(1,11):
        bb_img = pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_img.set_colorkey((0, 0, 0))
        bb_accs+=[bb_img]

    return (bb_accs,accs)

def get_kk_img(sum_mv:tuple[int,int])-> pg.Surface:
    """
    移動量の合計値タプルに対応する向きの画像Surfaceを返す
    引数:移動量の合計値タプル
    戻り値:飛ぶ方向にむかっているこうかとん画像
    """
    tmp_angle=[0,False,False]
    if sum_mv[0] > 0:
        tmp_angle=[0,1,0]
    if sum_mv[0] < 0:
        tmp_angle=[0,0,0]
    if sum_mv[1] > 0:
        tmp_angle=[90,0,0]
    if sum_mv[1] < 0:
        tmp_angle=[-90,0,0]

    if sum_mv[0] < 0 and sum_mv[1] > 0:
        tmp_angle=[45,0,0]
    if sum_mv[0] > 0 and sum_mv[1] > 0:
        tmp_angle=[45,1,0]
    if sum_mv[0] < 0 and sum_mv[1] < 0:
        tmp_angle=[-45,0,0]
    if sum_mv[0] > 0 and sum_mv[1] < 0:
        tmp_angle=[-45,1,0]
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), tmp_angle[0], 0.9)
    kk_img = pg.transform.flip(kk_img, tmp_angle[1], tmp_angle[2])
    return kk_img



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    tmr = 0
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bb_imgs,bb_accs=init_bb_imgs()
    bb_img=bb_imgs[min(tmr//500,9)]  # 爆弾用の型のサーフェース
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bg_img = pg.image.load("fig/pg_bg.jpg")
    vx, vy = +5, +5  # 爆弾速度ベクトル
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()

    cache_overscreen=[False,False]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        bb_img=bb_imgs[min(tmr//500,9)]  # 爆弾用の型のサーフェース

        if kk_rct.colliderect(bb_rct):
          gameover(screen)  # ゲームオーバー
          return
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

        kk_img = get_kk_img((0,0))
        kk_img=get_kk_img(tuple(sum_mv))

        screen.blit(kk_img, kk_rct)


        yoko,tate = check_bound(bb_rct)
        if not yoko and not cache_overscreen[0]:
            vx *= -1
            cache_overscreen[0]=True
        else:
            cache_overscreen[0]=False
        if not tate and not cache_overscreen[1]:
            vy *= -1
            cache_overscreen[1]=True
        else:
            cache_overscreen[1]=False


        avx = vx*bb_accs[min(tmr//500,9)]
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
