from PIL import Image
import argparse
from colorama import Fore, Back, Style
import streamlit as st

ASCII_CHARS = "@%#*+=-:. "

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))

def to_grayscale(image):
    return image.convert("L")

def map_pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_str = "".join(ASCII_CHARS[pixel // 25] for pixel in pixels)
    return ascii_str

def convert_image_to_ascii(image_path, output_width=100, colored=False):
    try:
        if isinstance(image_path, str):
            image = Image.open(image_path)
        else:
            image = Image.open(image_path).convert("RGB")
        image = resize_image(image, output_width)
        grayscale_image = to_grayscale(image)
        ascii_str = map_pixels_to_ascii(grayscale_image)
        ascii_lines = [ascii_str[i:i+output_width] for i in range(0, len(ascii_str), output_width)]
        if colored:
            ascii_lines_colored = apply_color(image, ascii_lines)
            return "\n".join(ascii_lines_colored)
        return "\n".join(ascii_lines)
    except Exception as e:
        return f"Error: {e}"

def apply_color(image, ascii_lines):
    image = image.resize((len(ascii_lines[0]), len(ascii_lines)))
    pixels = image.getdata()
    colored_lines = []
    for y, line in enumerate(ascii_lines):
        colored_line = ""
        for x, char in enumerate(line):
            r, g, b = pixels[y * len(line) + x][:3]
            colored_line += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
        colored_lines.append(colored_line)
    return colored_lines

def save_ascii_to_file(ascii_art, file_name="ascii_art.txt"):
    with open(file_name, "w") as file:
        file.write(ascii_art)

def cli_interface():
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("image_path", type=str, help="Path to the image file.")
    parser.add_argument("--width", type=int, default=100, help="Output width of the ASCII art.")
    parser.add_argument("--color", action="store_true", help="Enable colored ASCII output.")
    parser.add_argument("--output", type=str, default="ascii_art.txt", help="File to save the ASCII art.")
    args = parser.parse_args()
    ascii_art = convert_image_to_ascii(args.image_path, args.width, args.color)
    print(ascii_art)
    save_ascii_to_file(ascii_art, args.output)
    print(f"ASCII art saved to {args.output}")

def streamlit_app():
    st.title("Image to ASCII Art")
    uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    width = st.slider("Output Width", min_value=50, max_value=300, value=100, step=10)
    colored = st.checkbox("Enable Colored ASCII Output")
    if uploaded_file:
        ascii_art = convert_image_to_ascii(uploaded_file, width, colored)
        st.text("ASCII Art Output:")
        st.text(ascii_art)
        st.download_button(label="Download ASCII Art", data=ascii_art, file_name="ascii_art.txt", mime="text/plain")

if __name__ == "__main__":
    streamlit_app()
