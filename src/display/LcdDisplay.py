from grove.display.jhd1802 import JHD1802
lcd = JHD1802()

def updateLcd(text1, text2):
	lcd.setCursor(0, 0)
	lcd.write(text1)
	lcd.setCursor(1, 0)
	lcd.write(text2)
