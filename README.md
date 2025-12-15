# EdgeML Survey

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
git clone git@github.com:ljvmiranda921/edgeml-survey.git
cd edgeml-survey
uv sync
```

## Usage

### Fetching papers

Set up your [Semantic Scholar API key](https://www.semanticscholar.org/product/api#api-key-form) in a `.env` file:

```bash
S2_API_KEY=your_api_key_here
python scripts/s2_fetch.py \
    --limit 10000 \           # Set the limit of papers you want to get (you can set this high enough)
    --download data/pdfs  \   # Add the directory to where you want to store the downloaded pdfs
    --use_bulk_api        \   # Highly-recommend to just use the bulk API for fast processing
    --output_dataset your_hf_dataset
```