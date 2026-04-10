.PHONY: run-backend  # Mark as phony since it doesn't build a file

run-backend:
	uv run uvicorn app.main:app --reload