import pyautogui as pg
import time, win32api, winsound, random, os
from threading import Thread

# Record changes in shift
HIST = 0
def save_cfg():
    global HIST
    if shift_y != HIST:
        HIST = shift_y
        with open('pubg_recoil.cfg', 'w') as cfg:
            cfg.write(str(HIST))

# Getting saved value
shift_y = 0
if os.path.exists('pubg_recoil.cfg'):
    shift_y = int(open('pubg_recoil.cfg', 'r').read())

GETKEY = win32api.GetKeyState
switch = 0

def no_recoil():
    base_state = GETKEY(0x01)
    now = 0

    while True:
        
        # Record changes
        save_cfg()
        
        # Displayed text conf
        state_t = ['IDLE', 'SHOOTING'][now].center(10)
        switch_t = ['OFF', 'ON '][switch].center(7)
        shift_y_t = str(shift_y).center(6)
        print('\r', state_t, switch_t, shift_y_t, end='\r', sep='|')

        # If paused then skip
        if not switch:
            continue
        try:
            current_state = GETKEY(0x01)
            
            if current_state != base_state:
                base_state = current_state
                if current_state < 0:
                    now = 1
                else:
                    now = 0

            # Small delay to prevent eating thread
            time.sleep(0.001)
            
            # Shifting vs recoil
            if now:
                x, y = pg.position()
                pg.moveTo(x, y + shift_y, duration=0)
        
        except KeyboardInterrupt:
            print('\nNo Recoil terminated!')
            no_recoil()

# Hotkeys configurator
def switcher():
    global switch, shift_y

    base_state = GETKEY(0xC0)
    base_up = GETKEY(0x26)
    base_down = GETKEY(0x28)
    
    while True:
        current_state = GETKEY(0xC0)
        current_up = GETKEY(0x26)
        current_down = GETKEY(0x28)
        
        # Pause/Resume script
        if current_state != base_state:
            base_state = current_state
            switch = 1 if current_state else 0                
            winsound.PlaySound('done.wav', winsound.SND_ASYNC | winsound.SND_ALIAS)
        
        # Increase Recoil shift
        if current_up != base_up:
            base_up = current_up
            if -1 < shift_y < 25:
                shift_y += 1
        
        # Decrease Recoil shift
        if current_down != base_down:
            base_down = current_down
            if 0 < shift_y < 26:
                shift_y = abs(shift_y - 1)
            
        time.sleep(0.2)
 
if __name__ == '__main__':
    # Threading functions to allow live customization
    Thread(target=no_recoil).start()
    Thread(target=switcher).start()
