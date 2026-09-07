# Redago

**Polish spelling, punctuation and capitalisation correction — and, unusually
for a grammar checker, an explanation of every change it makes.**

Polish is a hard target for automated correction: rich inflection, free word
order, and comma rules that depend on clause structure rather than on any
surface cue. Redago attacks it with a short pipeline of specialised correctors
rather than one large model, and exposes the result as a web app that shows the
user *what* changed and *why*.

---

## How it works

Text passes through a chain of correctors, each responsible for one class of
error. Each stage is a `BaseCorrector` with a single `correct(text) -> str`
method, so the chain is a list and the order is a configuration choice:

```
raw text  →  SimpleCorrector  →  OrtCorrector  →  CommaCorrector  →  corrected text
              rules             mT5 seq2seq       token classification
```

| Stage | Approach | What it fixes |
| --- | --- | --- |
| `SimpleCorrector` | deterministic rules | sentence segmentation, capitalisation after a full stop, missing terminal punctuation, spacing |
| `OrtCorrector` | fine-tuned **mT5**, run as sequence-to-sequence with an `<ort>` task prefix | spelling and orthography, sentence by sentence |
| `CommaCorrector` | fine-tuned **BERT** used as a **token classifier** | comma placement |

The comma stage is the interesting one. Instead of asking a generative model to
rewrite the sentence and hoping it does not change anything else, it strips
every existing comma and then labels each token with "a comma follows / does
not follow" — punctuation restoration as sequence labelling. The model can only
insert commas, so it cannot silently corrupt the rest of the text, and its
output is directly auditable.

Splitting the work this way also means the cheap deterministic fixes never
reach a model at all, and each stage can be retrained, benchmarked and swapped
independently.

---

## Explaining the corrections

`POST /correct-with-reason` aligns the input with the output word by word and
labels every difference, so the frontend can highlight each change with its
cause instead of presenting an opaque rewrite:

```jsonc
{
  "tokenized_text": [
    { "text": "poszedłem",  "corrected": "Poszedłem",  "reason": ["case_changed"] },
    { "text": "do",         "corrected": "do",         "reason": ["ok"] },
    { "text": "sklepu",     "corrected": "sklepu,",    "reason": ["comma_inserted"] },
    { "text": "ktury",      "corrected": "który",      "reason": ["spelling_changed"] }
  ]
}
```

Recognised reasons: `case_changed`, `comma_inserted`, `comma_removed`,
`period_inserted`, `period_removed`, `spelling_changed`, `ok`.

`POST /correct` returns just the corrected string when the explanation is not
needed.

---

## Repository layout

```
redago_core/          the correction pipeline: BaseCorrector, the three correctors, the chain
redago_backend/       Litestar API - /correct, /correct-with-reason, the diff-and-label logic
redago_web/           React + TypeScript + Vite + Chakra UI client
redago_model/         training code: comma_model (token classification), ort_model (mT5)
redago_data_loader/   builds the training corpus from the Wolne Lektury public-domain book API
redago_tests/         accuracy harnesses for the comma and spelling correctors
```

### Building the corpus

`redago_data_loader` pulls public-domain Polish literature from the
[Wolne Lektury](https://wolnelektury.pl) API, filtered by genre, and prepares
it for training. For the comma model that means taking correctly punctuated
sentences, removing the commas, and keeping the original as the label — the
corpus supervises itself, so no manual annotation was needed.

### Measuring it

`redago_tests` holds two harnesses that take correctly written sentences,
damage them in the specific way a corrector is supposed to repair, and check
whether the model restores the original. Sentences the model gets wrong are
written out for inspection, which is how the failure cases were found.

---

## Running it

```sh
export HUGGINGFACE_TOKEN=...   # access to the fine-tuned models
export MODEL_NAME=...          # comma model on the Hugging Face Hub
export ORT_MODEL_NAME=...      # orthography model on the Hugging Face Hub

docker compose up --build      # API on :31416, web client on :80
```

Without Docker:

```sh
pip install -r requirements.txt
PYTHONPATH=. litestar --app redago_backend.app:app run     # API
cd redago_web && yarn && yarn dev                          # client
```

Retraining, corpus building and the accuracy harnesses are separate entry
points:

```sh
python redago_data_loader/api_loader.py                    # fetch and prepare books
python redago_model/comma_model/data.py <input> [output]   # build the comma dataset
python redago_model/comma_model/train-model.py             # fine-tune the comma model
python redago_tests/comma_efficiency_tester/main.py        # measure comma accuracy
```

---

## Stack

Python 3, PyTorch and Hugging Face Transformers for the comma model,
TensorFlow for the mT5 orthography model, `datasets` and scikit-learn for
training, Litestar and uvicorn for the API, React 18 with TypeScript, Vite and
Chakra UI for the client, Docker Compose for the whole thing.

## Authors

Built by **Marcin** ([@ack2406](https://github.com/ack2406)) — the
correction pipeline and correctors, the training pipeline, the corpus loader,
the Litestar API and the accuracy harnesses — with
**Maciej** ([@Birband](https://github.com/Birband)).
