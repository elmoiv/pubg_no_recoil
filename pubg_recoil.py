import pyautogui as pg
import time, win32api, winsound, random
from threading import Thread

switch, shift_y = 0, 0

def no_recoil():
    global switch, shift_y
    shift_y = int(input('Enter shift amount >>> '))
    base_state = win32api.GetKeyState(0x01)
    now = 0

    while True:

        # Displayed text conf
        state_t = ['IDLE', 'SHOOTING'][now].center(10)
        switch_t = ['OFF', 'ON '][switch].center(7)
        shift_y_t = str(shift_y).center(6)
        print('\r', state_t, switch_t, shift_y_t, end='\r', sep='|')

        # If paused then skip
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

    base_state = win32api.GetKeyState(0xC0)
    base_up = win32api.GetKeyState(0x26)
    base_down = win32api.GetKeyState(0x28)
    
    while True:
        current_state = win32api.GetKeyState(0xC0)
        current_up = win32api.GetKeyState(0x26)
        current_down = win32api.GetKeyState(0x28)
        
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
