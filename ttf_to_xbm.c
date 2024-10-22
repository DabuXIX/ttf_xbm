#include <ft2build.h>
#include FT_FREETYPE_H
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MAX_WIDTH 7   // Width
#define MAX_HEIGHT 13 // Fixed height 

// Function to write XBM data to a file
void write_xbm_file(char character, uint8_t *xbm_data, int width, int height) {
    char file_name[20];
    sprintf(file_name, "%c.xbm", character);

    FILE *file = fopen(file_name, "w");
    if (!file) {
        perror("Failed to open file");
        return;
    }

    fprintf(file, "#define %c_width %d\n", character, width);
    fprintf(file, "#define %c_height %d\n", character, height);
    fprintf(file, "static unsigned char %c_bits[] = {\n", character);

    // Write the bitmap as hex data
    for (int i = 0; i < height; ++i) {
        fprintf(file, "  0x%02x", xbm_data[i]);
        if (i < height - 1)
            fprintf(file, ", ");
        if ((i + 1) % 12 == 0)  // Limit number of items per line
            fprintf(file, "\n");
    }

    fprintf(file, "\n};\n");
    fclose(file);

    printf("XBM file for '%c' saved as %s\n", character, file_name);
}

// Constrained version: force 7-bit width using MAX_WIDTH
void bitmap_to_xbm_constrained(FT_Bitmap *bitmap, uint8_t *xbm_data, int max_width) {
    for (int row = 0; row < MAX_HEIGHT; ++row) {
        uint8_t byte = 0;
        for (int col = 0; col < max_width; ++col) {
            if (row < bitmap->rows && col < bitmap->width) {
                int pixel_index = row * bitmap->pitch + col;
                if (bitmap->buffer[pixel_index] > 0) {
                    byte |= (1 << col);  // Set the bit for each pixel
                }
            }
        }
        xbm_data[row] = byte;
    }
}



int main() {
    FT_Library ft;
    FT_Face face;

    // Initialize FreeType
    if (FT_Init_FreeType(&ft)) {
        fprintf(stderr, "Could not init FreeType library\n");
        return 1;
    }

    // Load font
    if (FT_New_Face(ft, "/mnt/c/Users/theda/onedrive/desktop/ttf_testuing/TimesNewRoman.ttf", 0, &face)) {
        fprintf(stderr, "Could not open font\n");
        return 1;
    }

    // Set font size to match desired height
    FT_Set_Pixel_Sizes(face, 0, MAX_HEIGHT);

    // Characters to convert
    char characters[] = "I";

    for (int i = 0; i < sizeof(characters) - 1; ++i) {
        char character = characters[i];

        // Load glyph
        if (FT_Load_Char(face, character, FT_LOAD_RENDER)) {
            fprintf(stderr, "Could not load character '%c'\n", character);
            continue;
        }

        // Get the glyph's bitmap
        FT_Bitmap *bitmap = &face->glyph->bitmap;

        // Prepare XBM data for the constrained version
        uint8_t xbm_data_constrained[MAX_HEIGHT] = {0};
        int output_width_constrained = MAX_WIDTH;  // Use constrained width (7 bits)

        // Constrained version
        bitmap_to_xbm_constrained(bitmap, xbm_data_constrained, output_width_constrained);
        write_xbm_file(character, xbm_data_constrained, output_width_constrained, MAX_HEIGHT);
    }

    // Clean up FreeType
    FT_Done_Face(face);
    FT_Done_FreeType(ft);

    return 0;
}
