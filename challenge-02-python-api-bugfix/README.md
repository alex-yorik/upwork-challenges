# Challenge #2 — Python API Bug Fix

## Client Brief

Hi,

I have a small Python application that communicates with an external REST API. The application works in the happy path, but it has several reliability issues when the API returns errors or unexpected data.

Please review the existing code, reproduce the problems, identify the root causes, and make focused fixes. **Do not rewrite the application from scratch.**

### Requirements

- Handle HTTP 4xx/5xx responses without crashing.
- Handle request timeouts.
- Handle invalid JSON.
- Handle responses where `data` is missing.
- Handle responses where required fields are missing.
- Keep the successful workflow working.
- Add tests for important failure cases.
- Keep the project simple and avoid unnecessary dependencies.
- Update this README with a short summary of your changes when complete.

### Acceptance criteria

A successful API response returns the extracted user data.

API failures result in a controlled error rather than an unhandled exception.

The application can distinguish between an API/network problem and invalid data returned by the API.

The test suite covers the important failure scenarios.

Run the application with:

```bash
python -m src.main
```

Run tests with:

```bash
pytest
```

### Important

This repository intentionally contains defects. Please investigate them rather than assuming the implementation is correct.

Budget: **$20 fixed price**
