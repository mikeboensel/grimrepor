# Database Setup and Management

This directory contains scripts for setting up and managing the MySQL database that tracks ML paper implementations and their build status.

## Setup

The `database_cmds.py` script handles:

1. MySQL installation
2. Server startup
3. Database creation
4. Table creation
5. Updating the table

## Environment Variables

A `.env` file is required in the root directory with the following variables:

```console
MYSQL_HOST='localhost'  
MYSQL_PORT=3306|33060  
MYSQL_USER='root'  
MYSQL_PASSWORD=''  
MYSQL_ROOT_PASSWORD='non_blank_pw'  
GITHUB_TOKEN=your_github_token  
OPENAI_API_KEY=api_key  
DATABASE_NAME='grimrepor_db'  
```

## Table Schema

| Field                    | Type         | Null | Key | Default | Extra          |
|-------------------------|--------------|------|-----|---------|----------------|
| id                      | int          | NO   | PRI | NULL    | auto_increment |
| paper_title             | varchar(255) | NO   | UNI | NULL    |                |
| paper_arxiv_id          | varchar(255) | YES  | UNI | NULL    |                |
| paper_arxiv_url         | varchar(255) | YES  | UNI | NULL    |                |
| paper_pwc_url           | varchar(255) | YES  | UNI | NULL    |                |
| github_url              | varchar(255) | YES  | UNI | NULL    |                |
| contributors            | varchar(255) | YES  |     | NULL    |                |
| build_sys_type         | varchar(255) | YES  |     | NULL    |                |
| deps_file_url          | varchar(255) | YES  | UNI | NULL    |                |
| deps_file_content_orig | mediumtext   | YES  |     | NULL    |                |
| deps_last_commit_date  | date         | YES  |     | NULL    |                |
| build_status_orig      | varchar(255) | YES  |     | NULL    |                |
| deps_file_content_edited| mediumtext   | YES  |     | NULL    |                |
| build_status_edited    | varchar(255) | YES  |     | NULL    |                |
| datetime_latest_build  | datetime     | YES  |     | NULL    |                |
| num_build_attempts     | int          | YES  |     | 0       |                |
| py_valid_versions      | varchar(255) | YES  |     | NULL    |                |
| github_fork_url        | varchar(255) | YES  | UNI | NULL    |                |
| pushed_to_fork         | tinyint(1)   | YES  |     | 0       |                |
| pull_request_made      | tinyint(1)   | YES  |     | 0       |                |
| tweet_posted           | tinyint(1)   | YES  |     | 0       |                |
| tweet_url              | varchar(255) | YES  | UNI | NULL    |                |

## Data Population

### Launch database creation and table population
Linux setup will require sudo
```bash
./setup/create_venv.sh
```

```bash
./setup/mysql_setup.sh
```

```bash
source venv/bin/activate
```

```bash
(venv) python3 database/database_cmds.py
```

### Initial Data
The `populate_table_from_papers_and_code_json()` function populates the first 5 columns using the Papers with Code dataset from:
https://production-media.paperswithcode.com/about/links-between-papers-and-code.json.gz

The JSON contains these fields for each entry:
- `paper_title`: Title of the research paper
- `paper_url`: URL to the paper on Papers with Code
- `repo_url`: GitHub repository URL
- `arxiv_id`: arXiv identifier (if available)
- `arxiv_url`: URL to the paper on arXiv

Note: Only unique paper titles and GitHub URLs are inserted to avoid duplicates. For papers with multiple implementations, currently only the first unique repository is stored.

### GitHub Data
The `populate_table_from_github_repo()` function:
- Uses the GitHub API to fetch repository data
- Limited to 5000 API calls per hour
- Uses `row_limit_parse` parameter to stay under API limits
- Performance is primarily constrained by database query operations

### Build System Types
The `build_sys_type` column can contain:
- `pip` (requirements.txt)
- `conda` (environment.yml, env.yml)
- `Not found` (no requirements file found)

This field determines how future build attempts will be handled - whether creating fresh requirements files or using pip/conda with virtual environments.
