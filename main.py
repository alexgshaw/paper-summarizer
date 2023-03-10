import openai
import os
from tqdm import tqdm
from time import sleep
import argparse

openai.api_key = os.environ.get("OPENAI_API_KEY")

MAX_PARAGRAPH_LENGTH = 200


def summarize(text: str) -> str:
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


def main(title: str, has_double_endlines: bool):
    directory = os.path.join("papers", title)

    sep = "\n\n" if has_double_endlines else "\n"

    with open(os.path.join(directory, "paper.txt"), "r") as file:
        paragraphs = file.read().split(sep)

    paragraphs = [
        paragraph.strip().replace("\n", " ")
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

    # add a flag that indicates double endlines when present
    parser.add_argument(
        "-d",
        "--double",
        action="store_true",
        help="Paragraphs are seperated by double endlines",
    )

    args = parser.parse_args()

    main(title=args.title, has_double_endlines=args.double)
