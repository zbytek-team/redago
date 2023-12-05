import tensorflow as tf
from datasets import load_dataset
from transformers import TFMT5ForConditionalGeneration, MT5Tokenizer, DataCollatorForSeq2Seq
from tensorflow.keras.optimizers import Adam


tokenizer = MT5Tokenizer.from_pretrained("google/mt5-small")
model = TFMT5ForConditionalGeneration.from_pretrained("google/mt5-small")

dataset = load_dataset("csv", data_files="data/human_annotators_common_errors_10K.csv", delimiter=";;")
dataset = dataset["train"].shuffle()

def preprocess_data(data):
    padding = "max_length"
    max_length = 20

    inputs = data["text"]
    targets = data["expected"]

    model_inputs = tokenizer(inputs, max_length=max_length, padding=padding, truncation=True)
    labels = tokenizer(targets, max_length=max_length, padding=padding, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

print(preprocess_data(dataset[0]))

train_dataset = dataset.map(preprocess_data, batched=True, desc="Processing dataset")


# data_collator = DataCollatorForSeq2Seq(
#     tokenizer=tokenizer,
#     model=model,
#     label_pad_token_id=tokenizer.pad_token_id,
#     pad_to_multiple_of=64,
#     return_tensors="np"
# )

# tf_train_dataset = model.prepare_tf_dataset(
#     train_dataset,
#     collate_fn=data_collator,
#     batch_size=8,
#     shuffle=True
# )

# model.compile(optimizer=Adam(learning_rate=3e-5))
# early_stopping = tf.keras.callbacks.EarlyStopping(monitor="loss", patience=3)
# model.fit(tf_train_dataset, epochs=10, callbacks=[early_stopping])
# model.save_pretrained("model")