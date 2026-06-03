# GitHub Step-by-Step Workflow

Use a believable development flow: feature branches merge into `dev`, then one final merge from `dev` into `main`.

```bash
git init
git add README.md requirements.txt config.yaml docs data src streamlit_app outputs powerbi
git commit -m "chore: initialize technology eol dashboard project"

git branch -M main
git checkout -b dev

git checkout -b feat/data-docs
git add docs data
git commit -m "docs: add documentation-driven eol research framework"
git checkout dev
git merge --no-ff feat/data-docs -m "merge: add documentation framework"

git checkout -b feat/executive-streamlit-rqs
git add streamlit_app
git commit -m "feat: add executive rq streamlit pages"
git checkout dev
git merge --no-ff feat/executive-streamlit-rqs -m "merge: add executive rq dashboard pages"

git checkout -b feat/analytics-exports
git add src outputs powerbi
git commit -m "feat: add figure exports and power bi reporting outputs"
git checkout dev
git merge --no-ff feat/analytics-exports -m "merge: add analytics export pipeline"

# Final release
git checkout main
git merge --no-ff dev -m "release: merge dev into main for executive eol dashboard"
```
