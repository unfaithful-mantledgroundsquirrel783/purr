# kitten-cli dev notes

## Local setup

```bash
uv pip install -e ".[dev]"
# or without dev extras:
uv pip install -e .
```

This installs the `purr` command and all dependencies including `kittentts` from its GitHub wheel.

## Running tests

```bash
pytest tests/
```

Tests mock out `kittentts`, `sounddevice`, and `soundfile` — no model download or audio hardware needed.

## Manual smoke test

```bash
purr model list
purr model install nano
purr speak "Hello, world." --output /tmp/test.wav
purr speak "Hello, world."                         # auto /tmp/purr-<ts>.wav
purr speak "Hello, world." --play
echo "Testing stdin" | purr speak --play --voice Luna
purr voices --model nano
purr model remove nano
```

Model files land in `~/.cache/kitten-cli/models/nano/`.
