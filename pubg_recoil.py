import pyautogui as pg
import time, win32api
import random

def no_recoil():
    shift_y = int(input('Enter shift amount >>> '))
    base_state = win32api.GetKeyState(0x01)
    now = 0

    while True:
        try:
            current_state = win32api.GetKeyState(0x01)
            
            if current_state != base_state:
                base_state = current_state
                if current_state < 0:
                    now = 1
                else:
                    now = 0
            print('\r' + ['Idle     ', 'Shooting!'][now], end='\r')
            time.sleep(0.001)
            if now:
                x, y = pg.position()
                pg.moveTo(x, y + shift_y, duration=0)
        except KeyboardInterrupt:
            print('\nNo Recoil terminated!')
            no_recoil()

if __name__ == '__main__':
    no_recoil()
