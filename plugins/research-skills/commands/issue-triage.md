# Issue Triage

Evaluate and create GitHub issues with AI-assisted triage.

## User Request
$ARGUMENTS

## Workflow
1. Check duplicates: `gh issue list -R <repo> --search "<keywords>"`
2. Assess difficulty (trivial/easy/medium/hard)
3. Draft issue body
4. Human approval
5. Create: `gh issue create -R <repo> -t "<title>" -b "<body>"`
