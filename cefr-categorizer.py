from gpt4all import GPT4All
from tqdm import tqdm
import signal
import os

input_file_path = "tatoeba.tsv"

model = GPT4All(
    model_name="mistral-7b-instruct-v0.1.Q4_0.gguf",
    model_path="/Users/koenig/Library/Application Support/nomic.ai/GPT4All",
)


def handler(signum, frame):
    # Close all open files
    for file in files.values():
        try:
            file.close()
        except OSError:
            pass
    exit(1)


signal.signal(signal.SIGINT, handler)

# Example list of sentences to categorize
sentences_to_categorize = [
    "This is a simple sentence.",
    "The cat is on the mat.",
    "Generate this lexicon for myself and I.",
]

levels = ["A1", "A2", "B1", "B2", "C1", "C2"]
files = {level: open(f"./generated/{level}.txt", "w") for level in levels}

# Open the file and process it line by line
with open(input_file_path, "r") as input_file, model.chat_session(
    system_prompt="You are a system responsible for classifying sentences into CEFR levels. Be concise and accurate."
):

    line_count = sum(1 for line in input_file)
    print("The file has", line_count, "lines")
    input_file.seek(0)

    # for line in tqdm(input_file, total=line_count, desc="Processing"):
    for line in input_file:
        parts = line.split("\t")
        sentence = parts[2].strip()

        response = model.generate(
            prompt=f"What cefr level is the sentence {sentence}? Base it only off vocabular. Names shouldn't matter for the level. Only give me the level (A1-C2), no further information",
            temp=0,
        )

        response = response.strip()
        if response in levels:
            print(f"[{response}] {sentence}")
            files[response].write(f"{sentence}\n")
        else:
            print(f"Error: {response} not in {levels}")

for file in files.values():
    file.close()
