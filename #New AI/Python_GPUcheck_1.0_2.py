import torch
print("CUDA available:", torch.cuda.is_available())
print("Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")

import transformers
import datasets
import peft
import accelerate
import bitsandbytes
print("All libraries loaded successfully!")
