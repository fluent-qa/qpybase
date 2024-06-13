# fluentqa-base

<div align="center">

![Coverage Report](assets/images/coverage.svg)

</div>

## What is fluentqa-base?

Fluent-QA Python Base Package, include:

1. BaseDataModel: pydantic model for structured data
2. builtin tools
3. configuration tools



## Very first steps

### Initialize your code

1. Initialize `git` inside your repo:

```bash
cd fluentqa-base && git init
```

2. If you don't have `Poetry` installed run:

```bash
make poetry-download
```

3. Initialize poetry and install `pre-commit` hooks:

```bash
make install
make pre-commit-install
```

4. Run the codestyle:

```bash
make codestyle
```

5. Upload initial code to GitHub:

```bash
git add .
git commit -m ":tada: Initial commit"
git branch -M main
git remote add origin https://github.com/fluent-qa/fluentqa-base.git
git push -u origin main
```

