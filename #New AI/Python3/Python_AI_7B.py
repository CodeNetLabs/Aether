import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from tqdm import tqdm

# Load model and tokenizer
model_id = "mistralai/Mistral-7B-Instruct-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    load_in_4bit=True,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Prepare for LoRA fine-tuning
model = prepare_model_for_kbit_training(model)
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# Load training data
if not os.path.exists("trainingdata"):
    raise FileNotFoundError("The file 'trainingdata' was not found.")

with open("trainingdata", "r", encoding="utf-8") as f:
    raw_data = f.read()

# Split into Q&A pairs
examples = []
for pair in raw_data.strip().split("\n\n"):
    if pair.strip() == "":
        continue
    lines = pair.strip().split("\n")
    if len(lines) < 2:
        continue
    question = lines[0].replace("Q: ", "")
    answer = lines[1].replace("A: ", "")
    full_text = f"### Question:\n{question}\n\n### Answer:\n{answer}"
    examples.append({"text": full_text})

# Convert to Hugging Face Dataset
dataset = Dataset.from_list(examples)

# Tokenize
def tokenize(example):
    return tokenizer(example["text"], truncation=True, padding="max_length", max_length=512)

tokenized_dataset = dataset.map(tokenize)

# Training arguments
training_args = TrainingArguments(
    output_dir="./mistral-lora-output",
    per_device_train_batch_size=1,
    num_train_epochs=1,
    logging_steps=10,
    save_strategy="no",
    report_to="none"
)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Progress bar trainer
class ProgressTrainer(Trainer):
    def train(self, *args, **kwargs):
        print("Starting training...\n")
        for _ in tqdm(range(len(tokenized_dataset)), desc="Training Progress"):
            super().train(*args, **kwargs)
            break  # real trainer handles all epochs internally
        return super().train(*args, **kwargs)

trainer = ProgressTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=data_collator
)

# Train model
trainer.train()

# Save model
model.save_pretrained("mistral-lora-trained")
tokenizer.save_pretrained("mistral-lora-trained")

# Chat with the model
print("\nTraining complete! You can now chat with your AI. Type 'exit' to stop.")
model.eval()
while True:
    user_input = input("\nYou: ")
    if user_input.strip().lower() == "exit":
        break

    input_text = f"### Question:\n{user_input}\n\n### Answer:\n"
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=100, pad_token_id=tokenizer.eos_token_id)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = reply.split("### Answer:\n")[-1].strip()
    print(f"AI: {answer}")
