from PIL import Image, ImageDraw, ImageFont

def load_ttf_font(ttf_file, size):
    """Load a TTF font and set the size."""
    return ImageFont.truetype(ttf_file, size)

def render_character_to_bitmap(font, character, grid_size, scale_factor=2):
    """Render a character into a bitmap, resize it, and center it in the grid."""
    # Create a high-resolution image first, respecting dynamic grid_size
    high_res_size = (grid_size[0] * scale_factor, grid_size[1] * scale_factor)
    high_res_image = Image.new('1', high_res_size, color=1)  # Blank white high-res image (1-bit)
    draw = ImageDraw.Draw(high_res_image)

    # Draw the character in the high-res image
    draw.text((0, 0), character, font=font, fill=0)  # Black text (0)

    # Get the bounding box of the character
    bbox = high_res_image.getbbox()  # Returns the non-white (ink) area
    if bbox:
        # Crop to the non-white area to remove extra white space
        cropped_image = high_res_image.crop(bbox)

        # Resize the cropped image to fit into the provided grid size (width, height)
        scaled_image = cropped_image.resize(grid_size, Image.LANCZOS)

        # Center the scaled image in a blank grid of the specified size
        centered_image = Image.new('1', grid_size, color=1)  # Blank grid of dynamic width and height
        x_offset = (grid_size[0] - scaled_image.width) // 2
        y_offset = (grid_size[1] - scaled_image.height) // 2
        centered_image.paste(scaled_image, (x_offset, y_offset))

        return centered_image
    else:
        # If no bounding box is found (character is blank), return a blank image
        return Image.new('1', grid_size, color=1)

def image_to_bitmap_data(image):
    """Convert the PIL image into a monochrome bitmap suitable for C header files."""
    bitmap_data = []
    
    for y in range(image.height):
        byte = 0
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            if pixel == 0:  # Black pixel
                byte |= (1 << (image.width - 1 - x))  # Set the corresponding bit based on width
        bitmap_data.append(byte)
    
    return bitmap_data

def write_c_header(output_file, char_code, bitmap_data, grid_width, grid_height):
    """Write the bitmap data into a C header format."""
    with open(output_file, 'a') as header_file:
        header_file.write(f"#define char_{char_code}_width {grid_width}\n")
        header_file.write(f"#define char_{char_code}_height {grid_height}\n")
        header_file.write(f"static unsigned char char_{char_code}_bits[] = {{\n")
        
        hex_values = [f"0x{byte:02x}" for byte in bitmap_data]
        header_file.write(f"   {', '.join(hex_values)}\n")
        header_file.write("};\n\n")

def generate_c_header(ttf_file, output_file, characters, grid_size):
    """Generate a C header file with bitmap data for the specified characters."""
    
    # Start with a reasonable font size, larger than the grid height since we will scale down
    target_font_size = grid_size[1] * 2  # Make sure the font size is based on grid height
    
    font = load_ttf_font(ttf_file, size=target_font_size)  # Load the TTF font with the larger size
    
    for char in characters:
        image = render_character_to_bitmap(font, char, grid_size)
        if image is not None:
            bitmap_data = image_to_bitmap_data(image)
            write_c_header(output_file, ord(char), bitmap_data, grid_size[0], grid_size[1])
        else:
            print(f"Character '{char}' could not be processed.")

if __name__ == "__main__":
    # Path to the TTF file
    ttf_file = r"C:\Users\theda\Downloads\CourierNew.ttf"
    
    # Path to output C header file
    output_file = r"C:\Users\theda\Downloads\out_test2.h"
    
    # Characters to generate
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Adjustable grid size (dynamically set width and height)
    grid_size = (7, 14)  # Change width and height as needed
    
    # Generate the C header file
    generate_c_header(ttf_file, output_file, characters, grid_size)
