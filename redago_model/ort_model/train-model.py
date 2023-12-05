import tensorflow as tf
from datasets import load_dataset
from transformers import TFMT5ForConditionalGeneration, MT5Tokenizer, DataCollatorForSeq2Seq
from tensorflow.keras.optimizers import Adam

DATA_PATH = "YOUR_DATA_PATH"

tokenizer = MT5Tokenizer.from_pretrained("google/mt5-small", legacy=False)
model = TFMT5ForConditionalGeneration.from_pretrained("google/mt5-small")

dataset = load_dataset("csv", data_files=DATA_PATH, delimiter=";;")
dataset = dataset["train"].shuffle(seed=17)

def preprocess_data(data):
    padding = "max_length"
    max_length = 100

    inputs = data["text"]
    targets = data["expected"]

    model_inputs = tokenizer(inputs, max_length=max_length, padding=padding, truncation=True)
    labels = tokenizer(targets, max_length=max_length, padding=padding, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

train_dataset = dataset.map(preprocess_data, batched=True, desc="Processing dataset")

data_collator = DataCollatorForSeq2Seq(
    tokenizer=tokenizer,
    model=model,
    label_pad_token_id=tokenizer.pad_token_id,
    pad_to_multiple_of=25,
    return_tensors="np"
)

tf_train_dataset = model.prepare_tf_dataset(
    train_dataset,
    collate_fn=data_collator,
    batch_size=4,
    shuffle=True
)

dataset_len = tf_train_dataset.cardinality().numpy()
val_quantity = int(dataset_len * 0.2)
print(f"all: {dataset_len} train: {dataset_len - val_quantity} val: {val_quantity}")

val_dataset_tmp = tf_train_dataset.take(val_quantity)
train_dataset_tmp = tf_train_dataset.skip(val_quantity)

model.compile(optimizer=Adam(learning_rate=3e-5), metrics=['accuracy'])
early_stopping = tf.keras.callbacks.EarlyStopping(monitor="loss", patience=3)
hist = model.fit(train_dataset_tmp, epochs=1, callbacks=[early_stopping], validation_data=val_dataset_tmp)
model.save_pretrained("/model")