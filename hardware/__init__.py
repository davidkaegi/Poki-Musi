
def get_hardware(use_desktop):
    if use_desktop:
        import hardware.desktop as desktop
        return desktop
    else:
        import hardware.rpi as rpi
        return rpi

KEY_UP = 0
KEY_RIGHT = 1
KEY_DOWN = 2
KEY_LEFT = 3
KEY_ESCAPE = 4
KEY_RESET = 5
KEY_SKIP = 6
