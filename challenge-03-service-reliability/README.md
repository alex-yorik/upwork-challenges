# Challenge #3 — Python Service Reliability

## Client brief

This small Python service receives orders and stores them in SQLite. It works most of the time, but the client reports occasional duplicate orders, lost/partial data, and poor diagnostics when something goes wrong.

Your task is to investigate the existing implementation and make it reliable.

### Requirements

1. The same `order_id` must not create duplicate orders if received more than once.
2. A failed order write must not leave a partially saved order behind.
3. Invalid orders must be rejected cleanly.
4. Database failures must not crash the service process.
5. Important failures should be logged with enough context to diagnose them.
6. Existing happy-path behavior should continue to work.
7. Add tests for the bugs you find and the fixes you make.
8. Tests must not depend on an external database or network.
9. Do not add unnecessary dependencies.
10. Keep the changes focused and update this README with a short summary of changes.

### Running

```bash
pip install -r requirements.txt
pytest -q
python -m src.main
```

Docker:

```bash
docker compose build
docker compose run --rm app
```

### Expected workflow

Investigate first. Identify the reliability problems and explain why they can occur. Then make the smallest reasonable fixes, add regression tests, and verify the application locally and in Docker.

Do not rewrite the service from scratch.
