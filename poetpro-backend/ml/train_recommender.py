import torch
from transformers import (
    BertTokenizer,
    EncoderDecoderModel,
    Trainer,
    TrainingArguments
)
from preprocess import load_and_prepare
from datasets import Dataset

# ----------------------------
# Load dataset
# ----------------------------
df = load_and_prepare("data/Pantun&SyairDataset.csv")
dataset = Dataset.from_pandas(df)

# ----------------------------
# Load tokenizer & model
# ----------------------------
tokenizer = BertTokenizer.from_pretrained("bert-base-multilingual-cased")

model = EncoderDecoderModel.from_encoder_decoder_pretrained(
    "bert-base-multilingual-cased",
    "bert-base-multilingual-cased"
)

model.config.decoder_start_token_id = tokenizer.cls_token_id
model.config.pad_token_id = tokenizer.pad_token_id

# ----------------------------
# Tokenization
# ----------------------------
def tokenize(batch):
    inputs = tokenizer(
        batch["model_input"],
        padding="max_length",
        truncation=True,
        max_length=128
    )

    outputs = tokenizer(
        batch["model_output"],
        padding="max_length",
        truncation=True,
        max_length=128
    )

    inputs["labels"] = outputs["input_ids"]
    return inputs

dataset = dataset.map(tokenize, batched=True)

# ----------------------------
# Training arguments
# ----------------------------
training_args = TrainingArguments(
    output_dir="./pantun_syair_recommender",
    learning_rate=5e-5,
    per_device_train_batch_size=2,
    num_train_epochs=5,
    save_total_limit=2,
    logging_steps=10,
    save_steps=500,
    fp16=torch.cuda.is_available()
)

# ----------------------------
# Trainer
# ----------------------------
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

# ----------------------------
# Train
# ----------------------------
trainer.train()

# Save model
model.save_pretrained("./pantun_syair_recommender")
tokenizer.save_pretrained("./pantun_syair_recommender")
