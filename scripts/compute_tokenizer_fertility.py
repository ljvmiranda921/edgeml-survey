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
    pass


def main():
    pass


if __name__ == "__main__":
    main()
