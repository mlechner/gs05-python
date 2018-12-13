# -*- coding: utf-8 -*-

import lcd_I2C.lib.lcddriver as lcddriver


class Lcd:
    def __init__(self, *args, **kwargs):
        self.lcd = lcddriver.lcd()
        self.lcd.lcd_clear()

    def display_record(self, record, this=None):
        if this:
            try:
                if this.timestampout:
                    self.lcd.lcd_display_string((this.now.strftime("%d.%m.%y %H:%M")).ljust(16), this.timestampout)
                    self.lcd.lcd_write(lcddriver.LCD_RETURNHOME)
                    self.lcd.lcd_write(lcddriver.LCD_BLINKOFF)
                if this.deviceid:
                    self.lcd.lcd_display_string(("%(id)s:%(ld)s|%(hd)s|%(echo)s" % ({
                        "id": record.deviceid,
                        "ld": record.lowdose,
                        "hd": record.highdose,
                        "echo": record.echo})).ljust(16), this.valueout)
                else:
                    self.lcd.lcd_display_string(("ld %(ld)s | hd %(hd)s" % ({
                        "ld": record.lowdose,
                        "hd": record.highdose})).ljust(16), this.valueout)
                self.lcd.lcd_write(lcddriver.LCD_RETURNHOME)
                self.lcd.lcd_write(lcddriver.LCD_BLINKOFF)
            except RuntimeError:
                print("Runtime Error: Could not write to LCD.")
        else:
            print("this is missing: Could not write to LCD.")
