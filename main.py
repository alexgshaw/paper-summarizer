import openai
import os
from tqdm import tqdm
from time import sleep
import argparse

openai.api_key = os.environ.get("OPENAI_API_KEY")

MAX_PARAGRAPH_LENGTH = 200


def summarize(text: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f'Summarize the following paragraph into simple English:\n\n"{text}"\n\nSummary:',
        temperature=0.9,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"],
    )

    return response["choices"][0]["text"]


def main(title: str):
    directory = os.path.join("papers", title)

    with open(os.path.join(directory, "paper.txt"), "r") as file:
        paragraphs = file.readlines()

    paragraphs = [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip() != "" and len(paragraph) > MAX_PARAGRAPH_LENGTH
    ]

    summaries = []

    for paragraph in tqdm(paragraphs):
        for _ in range(10):
            try:
                summary = summarize(paragraph)
                summaries.append(summary.strip())
                break
            except Exception as e:
                print(e)
            sleep(1)

    with open(os.path.join(directory, "paper_summary.md"), "w") as file:
        file.write("\n\n".join(summaries))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-t",
        "--title",
        type=str,
        required=True,
        help="Path to the paper to summarize",
    )

    args = parser.parse_args()

    main(title=args.title)
