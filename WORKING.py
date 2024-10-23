import freetype
import os
import numpy as np
from PIL import Image

# Converts a FreeType bitmap into XBM format with fixed width and height.
def bitmap_to_xbm(char, bitmap, forced_width, forced_height):
    # Convert the bitmap buffer to a numpy array
    bitmap_array = np.array(bitmap.buffer, dtype=np.uint8).reshape(bitmap.rows, bitmap.width)

    # Create a PIL image from the bitmap array
    img = Image.fromarray(bitmap_array)

    # Resize the image to the forced width and height using high-quality resampling (LANCZOS)
    img_resized = img.resize((forced_width, forced_height), Image.Resampling.LANCZOS)

    # Convert the resized image back to a numpy array
    resized_array = np.array(img_resized)

    # Apply thresholding to remove anti-aliasing artifacts and ensure binary image
    threshold_value = 128  # Midpoint threshold between black and white
    binary_array = (resized_array > threshold_value).astype(np.uint8)

    # Clean up the bitmap to remove stray pixels
    cleaned_array = cleanup_image(binary_array)

    # Each byte will contain 8 bits, so calculate the number of bytes per row
    bytes_per_row = (forced_width + 7) // 8

    xbm_data = []
    for row in range(forced_height):
        row_data = [0] * bytes_per_row  # Initialize row with zeros (padding if needed)
        for col in range(forced_width):
            byte_index = col // 8  # Determine the byte index for this column
            bit_index = col % 8    # Determine which bit in the byte to set

            # Set bit if pixel in cleaned array is non-zero
            if cleaned_array[row, col] > 0:
                row_data[byte_index] |= (1 << bit_index)

        xbm_data.extend(row_data)

    return xbm_data

# Cleanup function to remove isolated pixels based on their neighbors.
def cleanup_image(bitmap_array):
    # Define the size of the character bitmap
    rows, cols = bitmap_array.shape
    
    # Create a copy of the bitmap to store cleaned data
    cleaned_bitmap = np.copy(bitmap_array)
    
    # Neighbor offsets for 8-connected pixels (left, right, up, down, and diagonals)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),  # Top-left, Top, Top-right
        (0, -1),           (0, 1),   # Left,        Right
        (1, -1), (1, 0), (1, 1)      # Bottom-left, Bottom, Bottom-right
    ]
    
    # Tolerance threshold: minimum number of neighbors a pixel needs to remain
    threshold = 2
    
    # Iterate over the bitmap and check for isolated pixels
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            if bitmap_array[row, col] > 0:  # Only process non-zero pixels
                # Count the number of non-zero neighboring pixels
                neighbor_count = 0
                for offset in neighbor_offsets:
                    neighbor_row = row + offset[0]
                    neighbor_col = col + offset[1]
                    if bitmap_array[neighbor_row, neighbor_col] > 0:
                        neighbor_count += 1
                
                # If the pixel has fewer neighbors than the threshold, remove it
                if neighbor_count < threshold:
                    cleaned_bitmap[row, col] = 0

    return cleaned_bitmap

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
def convert_ttf_to_xbm(ttf_path, char_list, forced_width=None, forced_height=13):
    print(f"Loading font from: {ttf_path}")
    face = freetype.Face(ttf_path)
    face.set_pixel_sizes(0, forced_height)  # Set the height and calculate width based on it
    
    for char in char_list:
        print(f"\nConverting character: {char}")
        face.load_char(char)
        bitmap = face.glyph.bitmap

        # If forced_width is provided, override the natural glyph width
        actual_width = forced_width if forced_width else bitmap.width

        print(f"Actual glyph width: {bitmap.width}, Adjusted to: {actual_width}")

        # Convert bitmap to XBM format with fixed width and height
        xbm_data = bitmap_to_xbm(char, bitmap, actual_width, forced_height)

        # Write the XBM data to a file
        write_xbm_file(char, xbm_data, actual_width, forced_height)

if __name__ == "__main__":
    # Path to the TTF font file
    ttf_path = r"C:\Users\theda\OneDrive\Desktop\ttf_testuing\TimesNewRoman.ttf"

    # Characters to convert
    char_list = "B"

    # Convert characters to XBM with forced width (e.g., 14 pixels wide) and height (e.g., 28 pixels tall)
    convert_ttf_to_xbm(ttf_path, char_list, forced_width=22, forced_height=39)
