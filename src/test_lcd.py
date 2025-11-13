import time
from display.lcd_display import LCDDisplay

lcd = LCDDisplay(i2c_address=0x27)

try:
    messages = ["Hola!", "Poco ruido :)", "Ruido alto!"]
    while True:
        for msg in messages:
            lcd.show_message(msg)
            time.sleep(2)
except KeyboardInterrupt:
    lcd.clear()
    print("Prueba terminada")
