cmake_minimum_required(VERSION 3.12)

# Pull in SDK (must be before project)
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(project_console C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

if (PICO_SDK_VERSION_STRING VERSION_LESS "1.3.0")
    message(FATAL_ERROR "Raspberry Pi Pico SDK version 1.3.0 (or later) required. Your version is ${PICO_SDK_VERSION_STRING}")
endif()

set(PROJECT_CONSOLE_PATH ${PROJECT_SOURCE_DIR})

# Initialize the SDK
pico_sdk_init()

if (TARGET tinyusb_device)
        add_executable(ppu
                ppu.c
        )

        # pull in common dependencies
        target_link_libraries(ppu hardware_spi pico_stdlib)

        # enable usb output, disable uart output
        pico_enable_stdio_usb(ppu 1)
        pico_enable_stdio_uart(ppu 0)

        # create map/bin/hex file etc.
        pico_add_extra_outputs(ppu)
elseif(PICO_ON_DEVICE)
    message(WARNING "not building hello_usb because TinyUSB submodule is not initialized in the SDK")
endif()

add_compile_options(-Wall
        -Wno-format          # int != int32_t as far as the compiler is concerned because gcc has int32_t as long int
        -Wno-unused-function # we have some for the docs that aren't called
        -Wno-maybe-uninitialized
        )
