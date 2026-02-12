import argparse
import logging
import sys
import os
from pathlib import Path

from datasets import Dataset

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
    parser.add_argument("--split", type=str, default="train", help="Dataset split name.")
    parser.add_argument("--tokenizer", type=str, required=True, help="Path to tokenizer.")
    # fmt: on


def main():
    pass


if __name__ == "__main__":
    main()
