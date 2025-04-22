# ICDC Data Retriever

A Python tool for retrieving and aggregating cancer imaging data from multiple sources including IDC (Imaging Data Commons), TCIA (The Cancer Imaging Archive), and ICDC (Integrated Canine Data Commons).

## Features

- Retrieves image collections from IDC
- Fetches collections from TCIA
- Gets study data from ICDC via GraphQL
- Concurrent data fetching using async/await
- Error handling and logging

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/icdc-data-retriever-python.git
cd icdc-data-retriever-python
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with the following variables:
```
BENTO_BACKEND_GRAPHQL_URI=https://caninecommons.cancer.gov/v1/graphql/
VERSION=your-version
```

## Usage

Run the script from the `src` directory:
```bash
cd src
python3 main.py
```

The script will:
1. Fetch IDC collections
2. Retrieve TCIA collections
3. Get ICDC study data
4. Print the results

## Output

The script outputs:
- Number of IDC collections found
- Number of TCIA collections found
- Number of ICDC studies found

## Testing

Run tests using pytest:
```bash
pytest tests/
```