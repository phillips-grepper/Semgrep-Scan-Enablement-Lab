# Semgrep Scan Enablement Lab

## OBJECTIVE
You are a new developer for the Acme Pet Company. You have been given a last minute assignment due to the main development team being unavailable and are being asked to validate that the company is shipping secure code without any known vulnerabilities. This isn't your typical assignment but because you are being asked to move quickly, and be a team player to do whatever you can to get this out the door quickly. The company is trying to release this new product to the market before the competition so every second matters...lets go!

#### PREREQUISITES

- Git
- Python 3.10+
- Semgrep (Licensed)
- A clone of this repository `https://github.com/phillips-grepper/Semgrep-Scan-Enablement-Lab`

#### USEFUL LINKS
+ https://docs.semgrep.dev/ 
+ https://www.semgrep.dev/



### ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Task 1 — Find the Leaked Partner Token`

  **Background**

  - The partner-integration team rushed a shelter-roster sync into this release. A reviewer suspects a credential slipped into the code, and if it ships, anyone reading the repository can use it.

  **Your Task**

  - Run a Semgrep scan of the PetFolio repository and find the hard-coded value assigned to `PARTNER_ROSTER_TOKEN`.

  **Task Validation:** Submit the full token value, starting with `ghp_` (40 characters).



### ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Task 2 — Trace the SQL Injection Sink`

**Background**

Injection flaws are still among the most common causes of breaches. The pet-search endpoint builds its SQL from request parameters, and Semgrep has flagged it.

**Your Task**

Find the FastAPI SQL injection finding in `routes_pets.py` and identify the **function that contains the sink**: where the untrusted input reaches the database.

**Task Validation:** Submit the function name exactly as it appears in the code, without parentheses.



### ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Task 3 — Find the Safe Requests Version` 

**Background**

PetFolio pins an old version of the popular `requests` HTTP library. Semgrep Supply Chain reports several known vulnerabilities in it, but only one is triggered by how PetFolio uses the library.

**Your Task**

Find the Semgrep Supply Chain finding for `requests` with the identifier **CVE-2023-32681**, and report the version that fixes it.

**Task Validation:** Submit a version number in the form `X.Y.Z`.



### ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `Task 4 — Reducing Scan Noise` 

**Background**

Not every finding needs a human. Semgrep checks whether leaked secrets are still active, and Semgrep Assistant automatically triages findings it judges to be noise, so developers can focus on what matters.

**Your Task**

In the Semgrep web app, find the secrets finding for the GitHub token from Task 1. Semgrep found the token is not active. Report the **triage status** Semgrep assigned to it automatically.

**Getting Started**

This task needs your scan results in the Semgrep platform, so make sure you have run `semgrep ci` (without `--dry-run`) at least once. Then sign in at semgrep.dev with the same Semgrep credentials.

**Task Validation:** Submit the status label exactly as shown.
