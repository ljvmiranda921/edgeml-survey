import argparse
import logging
import sys
import regex
from pathlib import Path
from transformers import AutoTokenizer
from tqdm import tqdm

from datasets import load_dataset

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.INFO,
)


def get_args():
    # fmt: off
    parser = argparse.ArgumentParser(description="Compute tokenizer fertility.")
    parser.add_argument("--input_dataset", type=str, required=True, help="Path to the dataset to compute tokenizer fertility.")
    parser.add_argument("--output_path", type=Path, help="Path to save the output CSV file.")
    parser.add_argument("--split", type=str, default="train", help="Dataset split name.")
    parser.add_argument("--tokenizer", type=str, required=True, help="HuggingFace ID to tokenizer.")
    parser.add_argument("--text_field", type=str, default="text", help="Input field in the dataset that contains the text to tokenize.")
    # fmt: on


def main():
    args = get_args()
    logging.info(f"Loading dataset: {args.input_dataset} (split={args.split})")
    dataset = load_dataset(args.input_dataset, split=args.split)

    total_words = 0
    total_bytes = 0
    for example in dataset:
        total_words += n_words(example[args.text_field])
        total_bytes += n_bytes(example[args.text_field])

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)

    def tokenize_fn(eg):
        return tokenizer(eg[args.text_field])

    logging.debug("Performing tokenization...")
    process_ds = dataset.map(tokenize_fn, batched=True)
    total_tokens = 0
    for example in tqdm(process_ds):
        example_tokens = len(example["input_ids"])
        total_tokens += example_tokens

    tokens_per_word = total_tokens / total_words
    tokens_per_byte = total_tokens / total_bytes
    breakpoint()


def n_words(sentence: str) -> int:
    words = regex.findall(
        r"[ ]?[\p{L}]+|[ ]?[^\p{L}\p{N} \t\n]+|[ ]+|[\t]+|[\n]+|\d{1}", sentence
    )
    return len(words)


def n_bytes(sentence: str) -> int:
    bytes_ = sentence.encode("utf-8")
    return len(bytes_)


if __name__ == "__main__":
    main()
