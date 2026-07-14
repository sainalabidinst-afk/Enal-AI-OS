# Contributing to Enal Cognitive Platform

Thank you for your interest in contributing to ECP!

## Code of Conduct

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please:
- Check if the feature has already been requested
- Clearly describe the problem and solution
- Explain why this feature would be useful

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Run benchmarks (`python -m benchmarks`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/enal-ai-org/ecp.git
cd ecp

# Setup environment
cp .env.example .env
docker-compose up -d

# Install backend
cd backend
poetry install

# Install SDK
cd ../sdk
pip install -e .

# Run tests
cd backend
pytest
```

## Coding Standards

- Python: Follow PEP 8, use `black` for formatting, `ruff` for linting
- Type hints required for all public APIs
- Docstrings required for all public classes and methods
- Tests required for all new features

## RFC Process

For significant changes, please submit an RFC:
1. Create a new file in `docs/rfcs/RFC-XXXX-title.md`
2. Follow the RFC template in `docs/rfcs/README.md`
3. Submit a PR for review

## Package Boundaries

Respect the package boundaries defined in `benchmarks/package_boundaries.py`:
- `kernel` must not depend on `runtime`, `sdk`, or `apps`
- `runtime` must not depend on `apps` or `sdk`
- `sdk` must not depend on `runtime`

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
