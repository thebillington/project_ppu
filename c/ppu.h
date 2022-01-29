#ifndef _PPU_H
#define _PPU_H

#include <stdio.h>
#include "pico/stdlib.h"

// Pins
#define LCD_DC_PIN      8
#define LCD_CS_PIN		9
#define LCD_CLK_PIN		10
#define LCD_MOSI_PIN	11
#define LCD_MISO_PIN	12
#define LCD_BKL_PIN     13
#define LCD_RST_PIN		15

// Prototypes
void WriteCommand(uint8_t VH);
void WriteData(uint8_t VH);

#endif