from grove.grove_ledbar import GroveLedBar

ledBar = GroveLedBar(22,0)

def showStatus(colour):
	if colour == "green":
		ledBar.set_level(3)
	elif colour == "yellow":
		ledBar.set_level(6)
	elif colour == "red":
		lebBar.set_level(10)
(CampusConnect) pi@raspi03:~/CampusConnect/src/main $ find ~/grove.py -name "*led*" -o -name "*my9221*"
/home/pi/grove.py/grove/grove_led.py
/home/pi/grove.py/grove/led
/home/pi/grove.py/grove/led/one_led_ws2812.py
/home/pi/grove.py/grove/led/one_led.py
/home/pi/grove.py/grove/grove_ryb_led_button.py
/home/pi/grove.py/grove/grove_ws2813_rgb_led_strip.py
/home/pi/grove.py/grove/grove_oled_display_128x64.py
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/grove_led.py
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/__pycache__/grove_led.cpython-313.pyc
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/__pycache__/grove_ws2813_rgb_led_strip.cpython-313.pyc
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/__pycache__/grove_ryb_led_button.cpython-313.pyc
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/__pycache__/grove_oled_display_128x64.cpython-313.pyc
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/led
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/led/one_led_ws2812.py
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/led/__pycache__/one_led_ws2812.cpython-313.pyc
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/led/__pycache__/one_led.cpython-313.pyc
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/led/one_led.py
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/grove_ryb_led_button.py
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/grove_ws2813_rgb_led_strip.py
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/grove/grove_oled_display_128x64.py
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/pip/_internal/distributions/__pycache__/installed.cpython-313.pyc
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/pip/_internal/distributions/installed.py
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/pip/_vendor/rich/__pycache__/styled.cpython-313.pyc
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/pip/_vendor/rich/styled.py
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/pygments/lexers/__pycache__/compiled.cpython-313.pyc
/home/pi/grove.py/CampusConnect/lib/python3.13/site-packages/pygments/lexers/compiled.py
/home/pi/grove.py/CampusConnect/bin/grove_led
/home/pi/grove.py/CampusConnect/bin/grove_ryb_led_button
/home/pi/grove.py/CampusConnect/bin/grove_ws2813_rgb_led_strip
/home/pi/grove.py/CampusConnect/bin/grove_oled_display_128x64
/home/pi/grove.py/build/lib/grove/grove_led.py
/home/pi/grove.py/build/lib/grove/led
/home/pi/grove.py/build/lib/grove/led/one_led_ws2812.py
/home/pi/grove.py/build/lib/grove/led/one_led.py
/home/pi/grove.py/build/lib/grove/grove_ryb_led_button.py
/home/pi/grove.py/build/lib/grove/grove_ws2813_rgb_led_strip.py
/home/pi/grove.py/build/lib/grove/grove_oled_display_128x64.py

(CampusConnect) pi@raspi03:~/CampusConnect/src/main $ find ~/grove.py -name "*.py" | xargs grep -l "MY9221\|LedBar\|ledbar"
grep: /home/pi/grove.py: Es un directorio
(CampusConnect) pi@raspi03:~/CampusConnect/src/main $ pip3 search grove |grep -i led
ERROR: XMLRPC request failed [code: -32500]
RuntimeError: PyPI no longer supports 'pip search' (or XML-RPC search). Please use https://pypi.org/search (via a browser) instead. See https://warehouse.pypa.io/api-reference/xml-rpc.html#deprecated-methods for more information.
