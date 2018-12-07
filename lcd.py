# -*- coding: utf-8 -*-

import sys
sys.path.append("lcd_I2C/lib")
import lcddriver

# on initialise lcd
lcd = lcddriver.lcd()

# on reinitialise lcd
lcd.lcd_clear()

#
lcd.lcd_display_string("   Hello world !", 1)
lcd.lcd_display_string("Lüpke FooBar@€ßü", 2)
