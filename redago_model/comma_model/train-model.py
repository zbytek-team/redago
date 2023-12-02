import logging
import sys

import numpy as np
import numpy.ma as ma
from datasets import Dataset
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from tqdm import tqdm
from transformers import (
    AutoTokenizer,
    BertForTokenClassification,
    DataCollatorForTokenClassification,
    Trainer,
    TrainingArguments,
)

from data import load

logging.basicConfig(level=logging.INFO)

MODEL_NAME = "dkleczek/bert-base-polish-cased-v1"
BATCH_SIZE = 4

TRAINING_SET_RATIO = 0.8
PROCESSED_DIR = "processed"

TRAINING_ARGS = TrainingArguments(
    output_dir=f"models/bert-comma",
    evaluation_strategy="steps",
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    gradient_accumulation_steps=1,
    num_train_epochs=9,
    adafactor=False,
    learning_rate=2e-5,
    warmup_steps=10000,
    weight_decay=0.0088,
    adam_epsilon=6e-08,
    lr_scheduler_type="cosine",
    report_to=["tensorboard"],
    logging_first_step=True,
    logging_steps=100,
    save_steps=100000,
    save_total_limit=10,
    seed=17,
)


def tokenize(data: list[str], stride: int = 0):
    """
    Tokenize data and add labels

    Args:
        data (list[str]): list of data
        stride (int, optional): stride for tokenization. Defaults to 0.
    """

    tokenizer_settings = {
        "is_split_into_words": True,
        "return_offsets_mapping": True,
        "padding": False,
        "truncation": True,
        "stride": stride,
        "max_length": 512,
        "return_overflowing_tokens": True,
    }

    tokenized_inputs = tokenizer(data[0], **tokenizer_settings)

    # add labels
    labels = []
    for document in tokenized_inputs.encodings:
        doc_encoded_labels = []

        for word_id in document.word_ids:
            if word_id is None:
                doc_encoded_labels.append(-100)
            else:
                label = data[1][word_id]
                doc_encoded_labels.append(int(label))

        labels.append(doc_encoded_labels)

    tokenized_inputs["labels"] = labels

    return tokenized_inputs


def to_dataset(data: list[str], stride: int = 0):
    """
    Convert tokenized data to dataset

    Args:
        data (list[str]): list of tokenized data
        stride (int, optional): stride for tokenization. Defaults to 0.
    """

    labels, token_type_ids, input_ids, attention_masks = [], [], [], []

    for item in tqdm(data):
        result = tokenize(item, stride=stride)

        labels += result["labels"]
        token_type_ids += result["token_type_ids"]
        input_ids += result["input_ids"]
        attention_masks += result["attention_mask"]

    return Dataset.from_dict(
        {
            "labels": labels,
            "token_type_ids": token_type_ids,
            "input_ids": input_ids,
            "attention_mask": attention_masks,
        }
    )


## metrics
def compute_metrics_sklearn(pred):
    """
    Compute metrics for sklearn
    """

    mask = np.less(pred.label_ids, 0)
    labels = ma.masked_array(pred.label_ids, mask).compressed()
    preds = ma.masked_array(pred.predictions.argmax(-1), mask).compressed()

    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average="binary"
    )
    acc = accuracy_score(labels, preds)

    return {
        "f1": f1,
        "precision": precision,
        "recall": recall,
        "accuracy": acc,
    }


if __name__ == "__main__":
    # if argument given, change processed dir
    if len(sys.argv) > 1:
        PROCESSED_DIR = sys.argv[1]

    # load data
    train_data, val_data = load(PROCESSED_DIR, TRAINING_SET_RATIO)

    # tokenize data
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    logging.info("Tokenizing training data")
    tokenized_dataset_train = to_dataset(train_data, stride=100)
    del train_data

    logging.info("Tokenizing validation data")
    tokenized_dataset_val = to_dataset(val_data)
    del val_data

    # train model
    model = BertForTokenClassification.from_pretrained(MODEL_NAME, num_labels=2)

    data_collator = DataCollatorForTokenClassification(tokenizer)

    trainer = Trainer(
        model,
        TRAINING_ARGS,
        train_dataset=tokenized_dataset_train,
        eval_dataset=tokenized_dataset_val,
        data_collator=data_collator,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics_sklearn,
    )

    trainer.train()
    trainer.save_model("models/bert-comma-final")
