import os
import subprocess
import pandas as pd

# Assuming df is your DataFrame containing GitHub issues
# df = pd.read_csv('path_to_your_csv_file.csv')

keywords = [
    'version conflict', 'pip issue', 'version mismatch', 'python version mismatch',
    'module not found', 'import error', 'attribute error', 'deprecated',
    'incompatible version', 'requires version', 'unsupported version',
    'version not supported', 'version error', 'version not found',
    'version not installed', 'version requirement', 'version constraint',
    'version dependency', 'version incompatibility', 'version issue',
    "pip install", "pip upgrade", "pip uninstall", "pip install --upgrade",
    "pip install --user", "pip install --system", "pip install --target",
    "pip install --editable", "pip install --no-index", "pip install --find-links",
    "pip install --no-deps", "pip install --no-binary", "pip install --only-binary"
]


def classify_issues(df):
    def check_issue(row):
        title = str(row['title']).lower()
        body = str(row['body']).lower()
        for keyword in keywords:
            if keyword in title or keyword in body:
                return True
        return False

    df['is_version_issue'] = df.apply(check_issue, axis=1)
    return df

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

file_issues = os.path.join(ROOT, "output", "issues.csv")
df  = pd.read_csv(file_issues)
df = classify_issues(df)
output_file = os.path.join(ROOT, "output", "issues_classified.csv")
df.to_csv(output_file, index=False)
print(df[['title', 'is_version_issue']])
