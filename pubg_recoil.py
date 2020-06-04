import pyautogui as pg
import time, win32api, winsound, random, os
from threading import Thread

def is_pressed(key_code):
    base_state = win32api.GetKeyState(key_code)
    while True:
        current_state = win32api.GetKeyState(key_code)
        
        if current_state != base_state:
            return True
        time.sleep(0.001)

# 0 => off
# 1 => on
switch, shift_y = 0, 0

def no_recoil():
    global switch, shift_y
    shift_y = int(input('Enter shift amount >>> '))
    base_state = win32api.GetKeyState(0x01)
    now = 0

    while True:
        if not switch:
            continue
        try:
            current_state = win32api.GetKeyState(0x01)
            
            if current_state != base_state:
                base_state = current_state
                if current_state < 0:
                    now = 1
                else:
                    now = 0
            print(f"{['IDLE', 'PLAY'][now]}")
            print(f'{switch}')
            print(f'{shift_y}')
            time.sleep(0.001)
            if now:
                x, y = pg.position()
                pg.moveTo(x, y + shift_y, duration=0)
        except KeyboardInterrupt:
            print('\nNo Recoil terminated!')
            no_recoil()
        os.system('CLS')


# Switcher
def switcher():
    global switch, shift_y

    base_state = win32api.GetKeyState(0xC0)
    base_up = win32api.GetKeyState(0x26)
    base_down = win32api.GetKeyState(0x28)
    while True:
        current_state = win32api.GetKeyState(0xC0)
        current_up = win32api.GetKeyState(0x26)
        current_down = win32api.GetKeyState(0x28)
        
        if current_state != base_state:
            base_state = current_state
            switch = current_state
            winsound.PlaySound('done.wav', winsound.SND_ASYNC | winsound.SND_ALIAS)
        
        if current_up != base_up:
            base_up = current_up
            if 0 <= shift_y < 14:
                shift_y += 1
        
        if current_down != base_down:
            base_down = current_down
            if 0 <= shift_y < 15:
                shift_y = abs(shift_y - 1)
            
        time.sleep(0.2)
 
if __name__ == '__main__':
    Thread(target=no_recoil).start()
    Thread(target=switcher).start()
