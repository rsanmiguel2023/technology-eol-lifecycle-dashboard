
# Continue From Existing GitHub Project

Do not run `git init` if your repo already exists.

```bash
git checkout dev
git pull origin dev
git checkout -b feat/enterprise-data-layer-v4
```

Copy this V4 package over your repo, then run the pipeline.

```bash
git add data docs src streamlit_app outputs powerbi README.md requirements.txt config.yaml RUN_DASHBOARD_PIPELINE.md
git commit -m "refactor: implement enterprise raw processed engineered data layers"
git push origin feat/enterprise-data-layer-v4

git checkout dev
git merge --no-ff feat/enterprise-data-layer-v4 -m "merge: add enterprise data layer v4"
git push origin dev
```
