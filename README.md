# cja-pre-commit

This repository provides a [pre-commit](https://pre-commit.com/) hook definition for [`cja format`](https://github.com/jhasse/cja) and a dummy package that allows installing cja from PyPI.

## [pre-commit](https://pre-commit.com/) hook

You can use `cja format` with a pre-commit hook by adding the following to `.pre-commit-config.yaml` of your repository:

```yaml
repos:
- repo: https://github.com/jhasse/cja-pre-commit
  rev: 0.9.0
  hooks:
  - id: cja-format
```

Indentation, column limit, blank lines and line endings are taken from the nearest `.clang-format` file.
