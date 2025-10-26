import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from PIL import Image
import os
import time
from tqdm import tqdm
import sys

# Check for CUDA and exit if not available
if not torch.cuda.is_available():
    print("CUDA-compatible GPU not found! Please run on a machine with an NVIDIA GPU.")
    sys.exit(1)

# Force usage of GPU
device = torch.device("cuda")

# Initialize progress bar
print("Initializing BLIP-2 AI Image Analyzer (FLAN-T5-XL) on GPU...")
for i in tqdm(range(100), desc="Loading", ncols=100):
    time.sleep(0.02)

# Load image from 'images/' folder
image_folder = 'images'
image_files = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'jpeg', 'png'))]
if not image_files:
    print("No image found in the 'images/' folder!")
    sys.exit(1)

image_path = os.path.join(image_folder, image_files[0])
print(f"Loaded image: {image_files[0]}")

# Load BLIP-2 FLAN-T5-XL model and processor
processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xl").to(device)

# Load and preprocess image
img = Image.open(image_path).convert('RGB')

print("Ready! You can now ask me questions about the image.")

# Initial caption to give a description
initial_prompt = "Describe this image."
inputs = processor(img, initial_prompt, return_tensors="pt")
inputs = {k: v.to(device) for k, v in inputs.items()}
out = model.generate(**inputs, max_new_tokens=100)
caption = processor.decode(out[0], skip_special_tokens=True)
print("Initial description:", caption)

# Main loop
while True:
    user_input = input("You: ").strip()
    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye!")
        break

    prompt = user_input
    inputs = processor(img, prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}
    out = model.generate(**inputs, max_new_tokens=100)
    answer = processor.decode(out[0], skip_special_tokens=True)
    print("AI:", answer)
