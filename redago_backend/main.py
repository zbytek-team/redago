import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, pipeline

import schemas

load_dotenv()


app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained(
    "Birband/comma-bert", use_auth_token=os.getenv("HUGGINGFACE_TOKEN"))

pipe = pipeline("ner", "Birband/comma-bert", aggregation_strategy="none",
                use_auth_token=os.getenv("HUGGINGFACE_TOKEN"))


def interpret(sentence) -> str:
    """
    Interpret the results from the NER model.
    The model returns a list of dictionaries with the following structure:
    {
        'word': 'string',
        'score': float,
        'entity': 'string',
        'index': int,
        'start': int,
        'end': int
    }

    The function will return a string with the commas in the correct place.
    """

    setComma = False
    sentence2 = []
    skipFirst = True
    lastWord = None

    for word in sentence:
        if skipFirst:
            skipFirst = False
            lastWord = word
            sentence2.append(word['word'])
            continue

        if lastWord['entity'] == 'LABEL_1' or setComma == True:
            setComma = True
            if word['start'] == lastWord['end']:
                sentence2.append(word['word'])
            else:
                sentence2.append(',')
                sentence2.append(word['word'])
                setComma = False
        else:
            sentence2.append(word['word'])

        lastWord = word
    return tokenizer.convert_tokens_to_string(sentence2)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/corrector/")
async def corrector(sentences: schemas.Sentences):
    """
    Corrects the sentences passed in the request body.
    Remove the commas from the sentences to then add them in the correct place.
    """

    corrected_sentences = pipe(sentences.text.replace(",", ""))

    interpreted_results = interpret(corrected_sentences)

    return {"corrected_sentences": interpreted_results}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
