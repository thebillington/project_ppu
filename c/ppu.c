#include "ppu.h"
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/spi.h"

int main(void) {
    // -------- Pico Setup --------
    // Initialize chosen serial port
    stdio_init_all();

    sleep_ms(5000);

    printf("stdio initialised\n");

    // Initialize DC pin high
    gpio_init(LCD_DC_PIN);
    gpio_set_dir(LCD_DC_PIN, GPIO_OUT);
    gpio_put(LCD_DC_PIN, 1);

    // Initialize CS pin high
    gpio_init(LCD_CS_PIN);
    gpio_set_dir(LCD_CS_PIN, GPIO_OUT);
    gpio_put(LCD_CS_PIN, 1);

    // Initialize BKL pin high
    gpio_init(LCD_BKL_PIN);
    gpio_set_dir(LCD_BKL_PIN, GPIO_OUT);
    gpio_put(LCD_BKL_PIN, 1);

    // Initialize RST pin high
    gpio_init(LCD_RST_PIN);
    gpio_set_dir(LCD_RST_PIN, GPIO_OUT);
    gpio_put(LCD_RST_PIN, 1);

    // Setup hardware spi pins
    gpio_set_function(LCD_CLK_PIN, GPIO_FUNC_SPI);
    gpio_set_function(LCD_MOSI_PIN, GPIO_FUNC_SPI);
    gpio_set_function(LCD_MISO_PIN, GPIO_FUNC_SPI);

    printf("pins initialised\n");

    // Initiate spi and report baud
    unsigned int baud;
    baud = spi_init(spi1, 4000000);
    printf("Baud: %u\n", baud);

    printf("spi initialised\n");

    // -------- END Pico Setup --------

    // -------- LCD Setup --------

    // Reset LCD
    gpio_put(LCD_RST_PIN, 1);
    sleep_ms(5);
    gpio_put(LCD_RST_PIN, 0);
    sleep_ms(15);
    gpio_put(LCD_RST_PIN, 1);
    sleep_ms(15);

    // Pull chip select low to enable
    gpio_put(LCD_CS_PIN, 0);

    // Command: Display Inversion ON
    WriteCommand(0x21);

    // Command: Power Control 3
    WriteCommand(0xC2);
    WriteData(0x33);

    // Command: VCOM Control
    WriteCommand(0xC5);
    WriteData(0x00);
    WriteData(0x1E);
    WriteData(0x80);

    //Command: Frame Rate Control
    WriteCommand(0xB1);
    WriteData(0xB0);

    // Command: Memory Access Control
    WriteCommand(0x36);
    WriteData(0x28);

    // Command: Interface Pixel Format 
    WriteCommand(0x3A);
    WriteData(0x55);

    // Command: Sleep OUT
    WriteCommand(0x11);
    sleep_ms(120);

    // Command: Display ON
    WriteCommand(0x29);

    gpio_put(LCD_CS_PIN, 1);

    // -------- END LCD Setup --------

    gpio_put(LCD_CS_PIN, 0);

    // gpio_put(LCD_DC_PIN, 0);
    // spi_write_blocking(spi1, 0x2A, 1);

    // gpio_put(LCD_DC_PIN, 1);
    // spi_write_blocking(spi1, 0x00, 1);
    // spi_write_blocking(spi1, 0x00, 1);
    // spi_write_blocking(spi1, 0x00, 1);
    // spi_write_blocking(spi1, 0xEF, 1);

    // gpio_put(LCD_DC_PIN, 0);
    // spi_write_blocking(spi1, 0x2B, 1);

    // gpio_put(LCD_DC_PIN, 1);
    // spi_write_blocking(spi1, 0x00, 1);
    // spi_write_blocking(spi1, 0x00, 1);
    // spi_write_blocking(spi1, 0x01, 1);
    // spi_write_blocking(spi1, 0x3F, 1);

    // gpio_put(LCD_DC_PIN, 0);
    // spi_write_blocking(spi1, 0x2C, 1);

    // gpio_put(LCD_DC_PIN, 1);
    // unsigned int i;
    // for (i = 0; i < 76800; i++) {
    //     spi_write_blocking(spi1, 0x00, 1);
    //     spi_write_blocking(spi1, 0x00, 1);
    //     spi_write_blocking(spi1, 0xFF, 1);
    //     spi_write_blocking(spi1, 0xFF, 1);
    // }

    gpio_put(LCD_DC_PIN, 0);
    spi_write_blocking(spi1, 0x0A, 1);

    uint8_t rx_data;
    gpio_put(LCD_DC_PIN, 1);
    spi_write_read_blocking(spi1,0x00,&rx_data,1);
    printf("%x", rx_data);

    spi_read_blocking(spi1, 0x00, &rx_data, 1);
    printf("%x", rx_data);

    gpio_put(LCD_CS_PIN, 1);



    printf("\n--------\nloop\n--------\n");
    while(true) {
        sleep_ms(1000);
    }

    return 0;
}

void WriteCommand(uint8_t VH) {
    // Set DC low for command
    gpio_put(LCD_DC_PIN, 0);
    spi_write_blocking(spi1, &VH, 1);
}

void WriteData(uint8_t VH) {
    // Set DC high for data
    gpio_put(LCD_DC_PIN, 1);
    spi_write_blocking(spi1, &VH, 1);
}