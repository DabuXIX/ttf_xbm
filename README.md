# README: TTF to XBM Converter (Windows)

## Requirements:
- GCC (via MinGW or similar)
- FreeType library (installed via MSYS2 or similar)
- TTF font file

## How to Compile:
1. Open a terminal (e.g., MSYS2) and run:
```bash
gcc -o ttf_to_xbm ttf_to_xbm.c -I/usr/include/freetype2 -lfreetype
