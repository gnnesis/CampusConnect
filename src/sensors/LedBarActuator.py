from grove.grove_ledbar import GroveLedBar
ledBar = GroveLedBar(22,0)

def showStatus(colour):
	if colour == "green":
		ledBar.set_level(3)
	elif colour == "yellow":
		ledBar.set_level(6)
	elif colour == "red":
		lebBar.set_level(10)
