import time
from RPLCD.i2c import CharLCD

# Configuración de la pantalla Grove 16x2 LCD
lcd = CharLCD('PCF8574', 0x27, cols=16, rows=2)  # dirección I2C común: 0x27

try:
    messages = ["Hola!", "Poco ruido :)", "Ruido alto!"]
    while True:
        for msg in messages:
            lcd.clear()          # limpiar pantalla antes de escribir
            lcd.write_string(msg)  # mostrar mensaje
            time.sleep(2)

except KeyboardInterrupt:
    lcd.clear()  # limpiar pantalla al salir
    print("Prueba terminada")
