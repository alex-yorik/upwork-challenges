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

## Summary of Changes

- `src/api_client.py`: added a small exception hierarchy rooted at the existing `APIError`:
  - `APINetworkError` — timeouts, connection failures and other request/transport errors;
  - `APIHTTPError` — HTTP 4xx/5xx responses, carries `status_code`;
  - `APIInvalidDataError` — invalid JSON, a missing `data` field, or missing required user fields.
  This lets the caller distinguish an API/network problem from invalid data returned by the API.
- `src/api_client.py` (`fetch_user`): 
  - `raise_for_status()` catches HTTP 4xx/5xx as `APIHTTPError`;
  - timeouts/connection/request errors are mapped to `APINetworkError`;
  - `response.json()` failures are mapped to `APIInvalidDataError`;
  - the payload is validated (JSON object with `data`, or a flat user object containing `name` and `email`, as returned by jsonplaceholder) and required fields are checked.
- `src/main.py`: reports category-specific messages (`API error`, `Network problem`, `Invalid data from API`) instead of a single generic failure, and never crashes.
- `tests/test_api_client.py`: replaced the stub tests with real assertions and added coverage for success, HTTP 404/500, timeout, connection error, invalid JSON, missing `data`, missing required fields, error-type distinction, and `main` output. All tests are mocked — no network calls.
- No new dependencies were added.
