# -*- coding: utf-8 -*-

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Robotics Inc, and all authors'
__license__   = 'All Rights Reserved'


# 外部プログラムの読み込み
# =============================================================================
from wiringpi import *


# 定数定義・初期化処理
# =============================================================================
RIGHT_WHEEL_PIN = 12
LEFT_WHEEL_PIN  = 13

wiringPiSetupGpio()
pinMode(RIGHT_WHEEL_PIN, PWM_OUTPUT)
pinMode(LEFT_WHEEL_PIN, PWM_OUTPUT)
pwmSetMode(PWM_MODE_MS)
pwmSetRange(1024) # 1024 => 2^10 => 10[bit]に精度を設定
pwmSetClock(375)  # 基本周波数が50[Hz]となるように、基準周波数21.6[MHz]を分周
                  # { (21.6 x 10^6) / (1024 x 375) => 50[Hz] }


# 独自命令の定義
# =============================================================================
def forward():
    pwmWrite(RIGHT_WHEEL_PIN, 512) # 512 / 1024 => 50%出力
    pwmWrite(LEFT_WHEEL_PIN, 512)  # 512 / 1024 => 50%出力


def stop():
    pwmWrite(RIGHT_WHEEL_PIN, 0)   # 0 / 1024 => 0%出力
    pwmWrite(LEFT_WHEEL_PIN, 0)    # 0 / 1024 => 0%出力


def right():
    pwmWrite(RIGHT_WHEEL_PIN, 768) # 768 / 1024 => 75%出力
    pwmWrite(LEFT_WHEEL_PIN, 256)  # 256 / 1024 => 25%出力


def left():
    pwmWrite(RIGHT_WHEEL_PIN, 256) # 256 / 1024 => 25%出力
    pwmWrite(LEFT_WHEEL_PIN, 768)  # 768 / 1024 => 75%出力


# トップレベル・スクリプトの定義
# =============================================================================
if __name__ == '__main__':
    from time import sleep

    while True:
        forward(); sleep(2)
        stop();    sleep(2)

        right();   sleep(2)
        stop();    sleep(2)

        left();    sleep(2)
        stop();    sleep(2)
