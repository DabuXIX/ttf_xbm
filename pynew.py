import freetype
import os

# Converts a freetype bitmap into XBM format with fixed width and height.
# Limits both the width (max.width) and height to specified values (7x13 by default).
# Each row is processed by checking pixel values, and bits are set accordingly.
def simple_to_xbm(char, bitmap, max_width, height):
    xbm_data = []
    
    for row in range(height, bitmap.rows):
        byte = 0
        bit_count = 0
        
        for col in range(min(max_width, bitmap.width)):
            # Check if pixel in bitmap is non-zero
            if bitmap.buffer[row * bitmap.width + col]:
                byte |= (1 << bit_count)  # Set the bit if the pixel is on
            
            bit_count += 1
            
            # When we have accumulated 8 bits, append the byte
            if bit_count == 8:
                xbm_data.append(byte)
                byte = 0  # Reset for the next byte
                bit_count = 0
        
        # Handle remaining bits if the width is not a multiple of 8
        if bit_count > 0:
            xbm_data.append(byte)
    
    # Padding rows to a fixed height if necessary
    while len(xbm_data) < height:
        xbm_data.append(0)
    
    return xbm_data


# Write XBM data to a file in XBM format, with up to 12 bytes per line for readability.
def write_xbm_file(char, xbm_data, width, height, output_dir):
    file_name = os.path.join(output_dir, f"{char}.xbm")

    with open(file_name, "w") as f:
        f.write(f"#define {char}_width {width}\n")
        f.write(f"#define {char}_height {height}\n")
        f.write(f"static char {char}_bits[] = {{\n")

        # Write bytes into XBM format, with 12 bytes per line for readability.
        for i, byte in enumerate(xbm_data):
            f.write(f"0x{byte:02x}, ")
            if (i + 1) % 12 == 0:
                f.write("\n")

        f.write("};\n")

    print(f"XBM file for {char} saved as {file_name}")


# Converts TTF characters to XBM format with a specified width and height.
def convert_ttf_to_xbm(ttf_path, char_list, max_width=7, height=13):
    face = freetype.Face(ttf_path)
    face.set_pixel_sizes(max_width, height)  # Set height and calculate width based on it

    for char in char_list:
        face.load_char(char)
        bitmap = face.glyph.bitmap

        # Use the actual glyph width or constrain to max_width
        actual_width = min(bitmap.width, max_width)

        # Convert bitmap to XBM format with fixed width and height
        xbm_data = simple_to_xbm(char, bitmap, actual_width, height)

        # Write XBM data to file
        write_xbm_file(char, xbm_data, actual_width, height)


if __name__ == "__main__":
    # Path to the TTF font file
    ttf_path = r"/path/to/your/font.ttf"  # Update this to your font file path

    # Characters to convert
    char_list = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Convert characters to XBM with 7x13 dimensions
    convert_ttf_to_xbm(ttf_path, char_list, max_width=7, height=13)