# LinkVaulter

LinkVaulter is a Flask application for storing useful links (urls), organizing them with tags. Link Vault provided both a small web interface viewver and a JSON API.

Unfortunately, the original development team was unable to complete the application before being assigned to a new client project. The repository contains a handful of smoke test and functional tests. The application starts and its smoke tests pass, however the functional tests fail as their functionality was not completed.

Your team has been tasked with completing the implementation of LinkVaulter.


## Software Architecture of LinkVaulter

- `link_vaulter/app.py` — Flask routes and demo data
- `link_vaulter/models.py` — link and tag transformations, issues 1–5
- `link_vaulter/validation.py` — input validation, issues 6–10
- `link_vaulter/search.py` — filtering and ranking, issues 11–15
- `link_vaulter/formatting.py` — display helpers, issues 16–20
- `link_vaulter/import_export.py` — CSV and JSON boundaries, issues 21–25
- `link_vaulter/analytics.py` — summaries and statistics, issues 26–30
- `tests/test_smoke.py` — passing starter checks
- `tests/test_issues.py` — Issue specific tests


## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m link_vaulter.app
```

Open <http://127.0.0.1:5000>.

## Tests

```bash
pytest -m smoke       # Confirms the starter application runs
pytest                # Includes all the functional test
pytest tests/test_issues.py::test_issue_01  # Runs test named test_issue_01
```

## Pull Request Workflow

As you work on implementing your assigned issue(s), You are expected to follow the workflow outlined below for each issue.

1. Create a branch such as `issue-07-normalize-tag`
2. Add additional tests or strengthen tests before implementing your change
3. Implement your code changes to fix the issue
4. Run the initial and additional test for the issue and ensure that they pass before moving onto step 5
5. Open a draft pull request using the template provided and fill out the information accordingly to reflect the changes included in your PR
6. Request a peer review from the assigned reviewer for that change
7. Respond to the feedback, incorporate changes based on the feedback, re-run tests, and merge only after approval
