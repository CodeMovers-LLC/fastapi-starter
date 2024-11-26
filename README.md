# fastapi-starter

Simple Fast API boilerplate.

## Description
This is the layout for an API with protected routes for users authenticated with AWS Cognito .

## Getting Started

### Dependencies
* Python 3.8

### Installing
```bash
python3 -m venv .venv &&
source .venv/bin/activate &&
pip install -r requirements.txt
```

### Running 
```bash
uvicorn app.main:app --reload
```