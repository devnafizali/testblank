# Download image function
from datetime import datetime
import datefinder
async def download_image(page, url, file_path):
    try:
        response = await page.evaluate(
            """async (url) => {
                const response = await fetch(url);
                const arrayBuffer = await response.arrayBuffer();
                return Array.from(new Uint8Array(arrayBuffer));
            }""",
            url
        )

        # Convert the list to bytes and write to the file
        with open(file_path, 'wb') as file:
            file.write(bytes(response))
    except Exception as error:
        print("Error downloading image:", error)

# Find mobile number function
def convert_suffix_to_number(input_string):
    # Define a dictionary to map multipliers to their corresponding values
    multiplier_mapping = {'K': 1000, 'M': 1000000, 'B': 1000000000}

    # Remove unnecessary words
    cleaned_string = input_string.replace('likes', '').replace('followers', '').replace('following', '').strip()

    # Extract numerical part and multiplier (if any)
    if cleaned_string[-1] in multiplier_mapping:
        multiplier = multiplier_mapping[cleaned_string[-1]]
        numeric_part = cleaned_string[:-1]
    else:
        multiplier = 1
        numeric_part = cleaned_string

    # Convert the numerical part to an integer and apply the multiplier
    try:
        result = int(float(numeric_part) * multiplier)
        return result
    except ValueError:
        print("Invalid input format. Unable to extract a valid number.")
        return None

def extract_date_from_text(text):
    matches = datefinder.find_dates(text)
    for match in matches:
        return match.strftime("%d %B %Y")
    return None

    for suffix, multiplier in suffix_multipliers.items():
        if suffix in value_str:
            numeric_part = float(value_str.replace(suffix, ''))
            return int(numeric_part * multiplier)

    # If no matching suffix is found, return the original value as an integer
    return int(value_str)
def get_categories(texts):
    contains_dot = any("·" in text for text in texts)
    new_texts = []
    if contains_dot:
        for text in texts:
            if "·" in text and text:
                split_text = text.split("·")
                # Remove the first index
                split_text = split_text[1:]
                # Trim leading and trailing spaces
                split_text = [word.strip() for word in split_text]
                new_texts.append(split_text)
    return new_texts
def convert_to_epoch(date_str):
    try:
        # Try parsing with comma
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
        # If parsing with comma fails, try without comma
        date_obj = datetime.strptime(date_str, "%B %d %Y")

    # Convert datetime object to epoch format
    epoch_time = int(date_obj.timestamp())
    return epoch_time
