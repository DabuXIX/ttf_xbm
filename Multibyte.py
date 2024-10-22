import freetype
import os

# Converts a FreeType bitmap into XBM format with fixed width and height.
# Handles any width by packing bits into multiple bytes when needed.
def bitmap_to_xbm(char, bitmap, max_width, height):
    xbm_data = []
    
    # Each byte will contain 8 bits, so calculate the number of bytes per row
    bytes_per_row = (max_width + 7) // 8  # Ceiling division to account for full byte

    print(f"Processing character: {char}")
    print(f"Bitmap dimensions: {bitmap.width}x{bitmap.rows} (width x height)")
    print(f"Max width: {max_width}, Target height: {height}, Bytes per row: {bytes_per_row}")

    for row in range(min(height, bitmap.rows)):  # Limit to specified height
        row_data = [0] * bytes_per_row  # Initialize row with zeros
        
        for col in range(min(max_width, bitmap.width)):  # Limit to max_width
            byte_index = col // 8  # Determine the byte index for this column
            bit_index = col % 8    # Determine which bit in the byte to set

            # Set bit if pixel in bitmap is non-zero
            if bitmap.buffer[row * bitmap.pitch + col] > 0:
                row_data[byte_index] |= (1 << bit_index)
        
        xbm_data.extend(row_data)
        print(f"Row {row}: {row_data}")  # Print row data for debugging

    # Pad remaining rows to maintain fixed height
    while len(xbm_data) < bytes_per_row * height:
        xbm_data.append(0)

    return xbm_data

# Writes XBM data to a file in XBM format.
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
def convert_ttf_to_xbm(ttf_path, char_list, width=7, height=13):
    print(f"Loading font from: {ttf_path}")
    face = freetype.Face(ttf_path)
    face.set_pixel_sizes(0, height)  # Set the height and calculate width based on it
    
    for char in char_list:
        print(f"\nConverting character: {char}")
        face.load_char(char)
        bitmap = face.glyph.bitmap

        # Use the actual glyph width or constrain to max_width (width parameter)
        actual_width = min(bitmap.width, width)

        print(f"Actual glyph width: {bitmap.width}, Adjusted to: {actual_width}")

        # Convert bitmap to XBM format with fixed width and height
        xbm_data = bitmap_to_xbm(char, bitmap, actual_width, height)

        # Write the XBM data to a file
        write_xbm_file(char, xbm_data, actual_width, height)

if __name__ == "__main__":
    # Path to the TTF font file
    ttf_path = r"C:\Users\theda\OneDrive\Desktop\ttf_testuing\Courier.ttf"

    # Characters to convert
    char_list = "J"

    # Convert characters to XBM with larger dimensions (14x13 for example)
    convert_ttf_to_xbm(ttf_path, char_list, width=14, height=13)
