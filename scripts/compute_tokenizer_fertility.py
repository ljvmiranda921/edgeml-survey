import argparse
from pathlib import Path

import pandas as pd
import regex
from datasets import get_dataset_config_names, load_dataset
from tqdm import tqdm
from transformers import AutoTokenizer


def get_args():
    # fmt: off
    parser = argparse.ArgumentParser(description="Compute tokenizer fertility from the Flores-200 dataset.")
    parser.add_argument("--input_dataset", type=str, default="openlanguagedata/flores_plus", help="Path to the dataset to compute tokenizer fertility.")
    parser.add_argument("--output_dir", type=Path, default="notebooks/data/tokenizer_fertility", help="Path to save the output CSV file.")
    parser.add_argument("--split", type=str, default="dev", help="Dataset split name.")
    parser.add_argument("--tokenizer", type=str, required=True, help="HuggingFace ID to tokenizer.")
    parser.add_argument("--text_field", type=str, default="text", help="Input field in the dataset that contains the text to tokenize.")
    # fmt: on
    return parser.parse_args()


def main():
    args = get_args()
    print(f"Loading dataset: {args.input_dataset} (split={args.split})")
    subsets = [s for s in get_dataset_config_names(args.input_dataset) if s != "default"]  # fmt: skip

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)

    def tokenize_fn(eg):
        return tokenizer(eg[args.text_field])

    tokenizer_name = args.tokenizer.replace("/", "___")
    output_path = args.output_dir / f"{tokenizer_name}.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing subsets or initialize CSV with headers
    if output_path.exists():
        existing_df = pd.read_csv(output_path)
        existing_subsets = set(existing_df["subset"].tolist())
    else:
        existing_subsets = set()
        df = pd.DataFrame(columns=["subset", "tpw", "tpb", "tt", "tw", "tb"])
        df.to_csv(output_path, index=False)

    for subset in subsets:
        if subset in existing_subsets:
            tqdm.write(f"Skipping {subset} (already exists)")
            continue

        try:
            dataset = load_dataset(args.input_dataset, subset, split=args.split)
        except ValueError:
            tqdm.write(f"Skipping {subset} (no {args.split} split)")
            continue

        total_words = 0
        total_bytes = 0
        for example in dataset:
            total_words += n_words(example[args.text_field])
            total_bytes += n_bytes(example[args.text_field])

        process_ds = dataset.map(tokenize_fn, batched=True)
        total_tokens = 0
        for example in tqdm(process_ds):
            example_tokens = len(example["input_ids"])
            total_tokens += example_tokens

        tokens_per_word = total_tokens / total_words
        tokens_per_byte = total_tokens / total_bytes

        row = {
            "subset": subset,
            "tpw": tokens_per_word,
            "tpb": tokens_per_byte,
            "tt": total_tokens,
            "tw": total_words,
            "tb": total_bytes,
        }

        pd.DataFrame([row]).to_csv(output_path, mode="a", header=False, index=False)
        tqdm.write(f"{subset}: {row}")


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
