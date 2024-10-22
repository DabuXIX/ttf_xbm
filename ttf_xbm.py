import freetype
import os

# Converts a FreeType bitmap into XBM format with fixed width and height.
# Limits both the width (max_width) and height to specified values (7x13 by default).
# Each row is processed by checking pixel values, and bits are set accordingly.
def bitmap_to_xbm(char, bitmap, max_width, height):
    xbm_data = []
    
    for row in range(min(height, bitmap.rows)):  # Limit to specified height
        byte = 0
        for col in range(min(max_width, bitmap.width)):  # Limit to max_width
            # Set bit if pixel in bitmap is non-zero
            if bitmap.buffer[row * bitmap.pitch + col] > 0:
                byte |= (1 << col)
        xbm_data.append(byte)

    # Pad remaining rows to maintain fixed height
    while len(xbm_data) < height:
        xbm_data.append(0)

    return xbm_data

# Writes XBM data to a file in XBM format.
# The output includes metadata like width and height, followed by the bitmap data
# formatted as an array of hex values, with up to 12 bytes per line for readability.
def write_xbm_file(char, xbm_data, width, height, output_dir=r"C:\Users\theda\OneDrive\Desktop\ttf_testuing\output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_name = os.path.join(output_dir, f"{char}.xbm")
    with open(file_name, "w") as f:
        f.write(f"#define {char}_width {width}\n")
        f.write(f"#define {char}_height {height}\n")
        f.write(f"static char {char}_bits[] = {{\n")

        # Write bytes in XBM format with max 12 bytes per line for readability
        for i, byte in enumerate(xbm_data):
            f.write(f"0x{byte:02x}")
            if i < len(xbm_data) - 1:
                f.write(", ")
            if (i + 1) % 12 == 0:  # Limit line length to 12 bytes for readability
                f.write("\n")
        f.write("\n};\n")

    print(f"XBM file for '{char}' saved as {file_name}.")

# Converts TTF characters to XBM format with specified width and height.
# Loads the font from ttf_path and converts each character in char_list into a bitmap,
# constraining the dimensions to the given width and height, then writes them to XBM files.
def convert_ttf_to_xbm(ttf_path, char_list, width=7, height=13):
    face = freetype.Face(ttf_path)
    face.set_pixel_sizes(0, height)  # Set the height and calculate width based on it
    
    for char in char_list:
        face.load_char(char)
        bitmap = face.glyph.bitmap

        # Use the actual glyph width or constrain to max_width (7)
        actual_width = min(bitmap.width, width)

        # Convert bitmap to XBM format with fixed width and height
        xbm_data = bitmap_to_xbm(char, bitmap, actual_width, height)

        # Write the XBM data to a file
        write_xbm_file(char, xbm_data, actual_width, height)

if __name__ == "__main__":
    # Path to the TTF font file
    ttf_path = r"C:\Users\theda\OneDrive\Desktop\ttf_testuing\Courier.ttf"

    # Characters to convert
    char_list = "J"

    # Convert characters to XBM with 7x13 dimensions
    convert_ttf_to_xbm(ttf_path, char_list, width=7, height=13)
