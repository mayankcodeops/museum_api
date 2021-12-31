### Reporter Package

**Reporter** is a Python library for generating CSV, HTML, XML and PDF reports from API data

#### Installation
```python
pip install -i https://test.pypi.org/simple/ reporter-mayank1729 
```

#### Usage Example
```python
import os
import pandas as pd
from reporter.helpers.fetch_response import fetch_response
from reporter.converter.converter import Converter

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

config = {
    "URL": os.environ.get('URL', 'https://api.example.com/todos/'),
    "REPORT_DIR": os.path.join(BASE_DIR, 'reports/'),
}

headers: dict[str, str] = {
    'Accept': '*/*',
    'Content-Type': 'application/json'
}

response = fetch_response(config['URL'], header=headers)
df = pd.json_normalize(response.json())

converter = Converter()
converter.convert_to_csv(config["REPORT_DIR"], 'report.csv', df)
converter.convert_to_html(config["REPORT_DIR"], 'report.html', df)
converter.convert_to_pdf(config["REPORT_DIR"], 'report.pdf', 'report.html')
converter.convert_to_xml(config["REPORT_DIR"], 'report.csv')
```
