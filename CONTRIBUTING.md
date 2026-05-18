# Contributing to ecommerce-product-trend-analysis

Thank you for your interest in contributing!

## Setup
```bash
git checkout -b feat/your-feature
docs: add CONTRIBUTING.mdmake test
```

## Standards
- Formatter: **Black** (120 chars)
- Linter: **flake8**
- Imports: **isort**
- Run: `make format && make lint`

## Testing
- Add tests in `tests/` for new features
- Run: `make test-cov`
- Target: >80% coverage

## Commits (Conventional Commits)
```
feat: new feature
fix: bug fix
docs: documentation
chore: maintenance
```

## Pull Request
1. `make test && make lint` must pass
2. Describe changes clearly

By contributing, you agree to the MIT License.
