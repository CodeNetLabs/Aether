import torch

def check_gpu():
    if not torch.cuda.is_available():
        print("❌ No CUDA-enabled GPU detected.")
        return

    num_gpus = torch.cuda.device_count()
    print(f"✅ CUDA is available. Detected {num_gpus} GPU(s).\n")

    for i in range(num_gpus):
        gpu_name = torch.cuda.get_device_name(i)
        total_mem = torch.cuda.get_device_properties(i).total_memory / (1024 ** 3)
        print(f"GPU {i}: {gpu_name}")
        print(f"   Memory: {total_mem:.2f} GB")
        print(f"   Device ID: {torch.cuda.device(i)}\n")

    current_device = torch.cuda.current_device()
    print(f"🎯 Active device: {torch.cuda.get_device_name(current_device)}")

if __name__ == "__main__":
    check_gpu()
