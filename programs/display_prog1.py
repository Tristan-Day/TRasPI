from gfxhat import lcd
for line in range(0,60,20):
    for bar in range(0,128):
        lcd.set_pixel(bar,line,1)
lcd.show()
