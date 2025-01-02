
**Just fixed your dead dependencies!**

[Grim Repor Website](https://grimrepor.sundai.club) | [Twitter](https://x.com/GrimRepor) 
---

## Overview

Welcome to **Grim Repor** — an AI-powered framework designed to **resurrect dead dependencies**. We identify research papers with code using our vigilante that roams the internet that finds broken or outdated Python dependencies and **fixes them** so your code runs smoothly again.

**You are here because we found your broken repository.**  
Give us a new repo, and we’ll put it’s back in action. We are dedicated to keeping great research projects alive, allowing researchers to focus on **what matters most**: innovation.

---

## What We Do

1. **Scan & Identify**: Our AI scans repositories, identifying broken or outdated dependencies.
2. **Fix & Upgrade**: We automatically fix version mismatches, upgrade dead dependencies, and ensure compatibility with modern environments.
3. **Deliver Working Code**: Once the fixes are in place, we provide a working version of your repository — so you and your users can focus on research, not debugging.



## Our methodology in detail
Most of the workflow below occurs in `scripts/build_check.py`.

- Run thru the repos we have available. 
    - Presently: These are in `scripts/paper_repo_info.csv`
    - Future improvement: we will source this more dynamically
- For each available repos assess what they use for dependency resolution to produce a list of packages that must be installed via `pip`:
    - Presently: `requirements.txt`, `environment.yml` (conda), and `setup.py`  based repos are supported. Other systems result in a "No requirements found" message
    - Future improvement: Expand to support other depedency/build systems (Docker, etc.)
    - Future improvement: Actually pull the GitHub repo (currently we just fetch the dependency file)
- Attempt to install required packages:
    - Presently: Create a new venv in a temp directory based on the `requirements.txt`. If pip is able to install all the required packages we call this a "Success"
- On install failure:
    - Attempt to fix using techniques (`scripts/process_errors.py`):
        - Check the date of the last commit and assume that the project built/ran then. Set dependency versions to the latest release at that point in time (findable via pypi's `Release History` page (ex: https://pypi.org/project/numpy/#history))
        - Check for duplicate entries for a given dependency
        - Check for mis-spelling of common
    - Attempt to a re-install
- Attempt to build:
    - Presently: Some projects may require an actual build step (vs being purely interpreted). At present none of this is considered.
- Verify functionality 
    - Presently: Does not appear to happen at all
- Store results of the workflow (that is subsequently used by other files)
    - Presently: Results are stored in `output/build_check_results.csv`
    - Future: Something more robust like a SQLite DB


`output/build_check_results.csv` is used as an input to:
- `scripts/new_repo.py`.
    - TODO: This script seems to not do much. Clones repos, but doesn't do any actual checks...
- `scripts/process_errors.py`
    - This implements the fixes.
    - Seems like it needs some work around Forking, pushing, creating a PR.


---

## Why Choose Grim Repor?

Over time, dependencies fall apart, versions get cranky, and your code starts gathering dust. But why waste your brilliance fixing boring dependency issues when **Grim Repor** can handle the dirty work? Whether you're a researcher, developer, or just trying to keep your stars and citations intact — let’s be honest, you're better off focusing on innovation. Leave the tedious dependencies to us. Need proof? Check out Grim Repor on GitHub and watch us keep your code shining!
[Github](https://github.com/grimrepor)

**We Keep Great Code Alive!**

---

## Setup

### Create and activate the virtual environment:

Create the virtual environment (installs `requirements.txt`)
```bash
./scripts/create_venv.sh
```

Activate the virtual environment
```bash
source venv/bin/activate
```

Run python script(s)
```bash
(venv) python3 scripts/build_check.py
```

To deactivate the virtual environment when you're done:
```bash
(venv) deactivate
```

---

## Get Involved

Need help with a new repository? Submit it to Grim Repor, and we’ll fix those dead dependencies for you.

---

## Support Us

If you appreciate our work and want to support our mission, consider tipping us **$10**. Every contribution helps us continue reviving dead dependencies and improving the research community.

---

## Stay Connected

- Website: [grimrepor.sundai.club](https://grimrepor.sundai.club)
- Twitter: [@GrimRepor](https://x.com/GrimRepor)

---

### Let's Keep Great Code Alive, Together!


|------------------|-------------|-------------------------------------------|

