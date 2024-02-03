from PIL import Image, ImageDraw, ImageFont
import imagehash


def word2hash(word, font_path="fonts/unifont-15.1.04.otf", font_size=25):
    # Load a font. Use a default PIL font if font_path is not provided.
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        # Fallback to a default font if no path is provided
        font = ImageFont.load_default()

    # Create a dummy image to calculate text dimensions accurately
    dummy_img = Image.new('RGB', (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)

    # Draw the text on the dummy image to calculate its bounding box
    dummy_draw.text((0, 0), word, font=font, fill=(0, 0, 0))
    bbox = dummy_draw.textbbox((0, 0), word, font=font)

    # Calculate text width and height from the bounding box
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # Create an actual image with a white background, dynamically sized
    img = Image.new('RGB', (text_width + 20, text_height + 20), color=(255, 255, 255))
    d = ImageDraw.Draw(img)

    # Draw the text on the actual image, centered
    d.text((10, 10), word, fill=(0, 0, 0), font=font)
    # Compute image hash using imagehash library
    hash_value = imagehash.average_hash(img)

    # Return the hash as a hexadecimal string
    return hash_value


class WordHasher:
    def __init__(self):
        self.hashes = {}

    def get_word_hash(self, word):
        try:
            return self.hashes[word]
        except KeyError:
            hashed_word = word2hash(word, font_path="fonts/unifont-15.1.04.otf")
            self.hashes.update({word: hashed_word})
            return hashed_word


if __name__ == "__main__":
    wh = WordHasher()
    print(wh.get_word_hash("helo"))
