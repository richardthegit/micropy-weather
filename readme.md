Weather
=======

Very basic weather display on the ultrawide 284x76 Estar Dyn display.

# Fonts

The ST7789 display driver doesn't use the standard framebuffer rendering system due to the excessive memory required for a full frame of color data, and as such uses custom rendering code. 

The driver repo provides various tools for generating bitmaps from fonts and images.

[](https://github.com/russhughes/st7789_mpy)

For example, so render out a font use:

    cd <repo>/utils
    create_venv.py
    activate.py
    python write_font_converter.py <ttf font> 40 -s "0123456789m:" > <output module>

