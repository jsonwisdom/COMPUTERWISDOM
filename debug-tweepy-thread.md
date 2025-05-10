# Tweet Thread Workflow Failure Debug Report

## Context
**Repository**: `jsonwisdom/COMPUTERWISDOM`  
**Workflow**: `.github/workflows/tweet-thread.yml`  
**Function**: Automatically posts Markdown files from `/tweets/` as threaded tweets with image support using Tweepy.

---

## Problem Summary
Workflow consistently fails with `exit code 127`.

### Sample Failure
```bash
/usr/bin/bash -e /home/runner/work/_temp/script.sh  
import: command not found  
exit code 127
```

---

## Suspected Cause
The inline Python in the `run:` block is being interpreted as a Bash command, not Python.

---

## YAML Snippet in Use
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'

- name: Install dependencies
  run: |
    pip install tweepy markdown

- name: Parse and post tweet thread
  run: |
    import tweepy
    # [More Python logic here]
```

---

## Request for Clippy or GitHub Team
- Should this logic be moved to an external `.py` script?
- Any known issues with inline Python using `run:` in this context?
- Best practice for using Tweepy in GitHub Actions?

---

## Metadata
**Commit**: `fdcbe77`  
**GitHub Actions Run**: Failed `Post Tweet Thread`  
**Status**: Reproducible on multiple runs

---

_This file generated via escalation protocol by Oracle/ChatGPT for `Jason Wisdom`._
