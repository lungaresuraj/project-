import replicate
import os
from dotenv import get_key
from PIL import Image
from io import BytesIO
import requests
from datetime import datetime

# ✅ Load and set Replicate API key
replicate_api_key = get_key(".env", "Replicate_API_Key")
os.environ["REPLICATE_API_TOKEN"] = replicate_api_key

def GenerateImages(prompt: str):
    try:
        print(f"[Replicate] Generating image for prompt: {prompt}")

        # ✅ Correct model name
        output = replicate.run(
            "stability-ai/sdxl",  # ← no spaces, correct name
            input={"prompt": prompt}
        )

        if not output or not isinstance(output, list):
            print("[Replicate] No image returned.")
            return

        image_url = output[0]
        img_data = requests.get(image_url).content

        # ✅ Save image
        os.makedirs("Data", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        safe_prompt = prompt.replace(" ", "_")
        img_path = f"Data/{safe_prompt}_{timestamp}.png"

        with open(img_path, "wb") as f:
            f.write(img_data)

        # ✅ Show image
        image = Image.open(BytesIO(img_data))
        image.show()

        # ✅ Save path for GUI
        os.makedirs("Frontend/Files", exist_ok=True)
        with open("Frontend/Files/GeneratedImagePath.txt", "w") as f:
            f.write(img_path)

        print(f"[Replicate] Image saved to: {img_path}")

    except Exception as e:
        print(f"[ImageGeneration Error] {e}")
