# Receipt Extractor

Command-line tool that processes receipt images in a directory and outputs a JSON mapping from filename to:
- date
- amount
- vendor
- category

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY="YOUR_KEY"

