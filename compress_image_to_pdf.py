import os
from PIL import Image
import io

# Constants
INPUT_FOLDER = "/Users/aashishpoudel/Downloads/Piano"
TEMP_FOLDER = "/Users/aashishpoudel/Downloads/Piano/temp"
OUTPUT_PDF = "/Users/aashishpoudel/Downloads/Piano/temp/output.pdf"
MAX_SIZE_KB = 500
MAX_BYTES = MAX_SIZE_KB * 1024

# Create temp folder if not exists
os.makedirs(TEMP_FOLDER, exist_ok=True)

def compress_image(input_path, output_path, max_bytes):
    img = Image.open(input_path).convert("RGB")
    quality = 95
    step = 5

    while quality > 5:
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        size = buffer.tell()
        if size <= max_bytes:
            with open(output_path, "wb") as f:
                f.write(buffer.getvalue())
            return True
        quality -= step

    # Final fallback to lowest quality
    img.save(output_path, format="JPEG", quality=5)
    return False

# Step 1: Compress images. If compression not needed, please comment below.
compressed_images = []
for filename in os.listdir(INPUT_FOLDER):
    if filename.lower().endswith(".jpg") or filename.lower().endswith(".jpeg"):
        input_path = os.path.join(INPUT_FOLDER, filename)
        output_path = os.path.join(TEMP_FOLDER, filename)
        success = compress_image(input_path, output_path, MAX_BYTES)
        if success:
            compressed_images.append(output_path)
        else:
            print(f"Warning: {filename} could not be compressed below {MAX_SIZE_KB} KB")

# If already compressed or no need to compress, please enable below.
# compressed_images = [os.path.join(TEMP_FOLDER,file) for file in os.listdir(TEMP_FOLDER) if file.endswith(".jpg")]
# sorted(compressed_images)

# Step 2: Convert to PDF
if compressed_images:
    image_list = [Image.open(path).convert("RGB") for path in compressed_images]
    pdf_path = OUTPUT_PDF
    first_image = image_list[0]
    rest_images = image_list[1:]
    first_image.save(pdf_path, save_all=True, append_images=rest_images)
    print(f"PDF created: {pdf_path}")
else:
    print("No images to convert.")