# cja-pre-commit

This repository provides [pre-commit](https://pre-commit.com/) hook definitions for [`cja format`](https://github.com/jhasse/cja) and a dummy package that allows installing cja from PyPI.

## [pre-commit](https://pre-commit.com/) hook

You can use `cja format` with a pre-commit hook by adding the following to `.pre-commit-config.yaml` of your repository:

```yaml
repos:
- repo: https://github.com/jhasse/cja-pre-commit
  rev: 0.10.0
  hooks:
  - id: cja-format
```

Indentation, column limit, blank lines and line endings are taken from the nearest `.clang-format` file.

### Only formatting changed lines

To adopt `cja format` in an existing code base without reformatting whole files, use the `cja-format-changed` hook instead:

```yaml
  hooks:
  - id: cja-format-changed
```

Like `git clang-format`, it only formats the statements touched by the staged changes (`cja format --lines`). When pre-commit runs with `--from-ref` and `--to-ref` (e.g. in CI), the changes between these refs are used. `pre-commit run --all-files` therefore does nothing without staged changes.
