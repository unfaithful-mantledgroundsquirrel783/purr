#!/usr/bin/env bash
# Lean install for purr as a uv tool — avoids the torch/CUDA bloat caused by
# misaki[en] → spacy-curated-transformers → torch.
#
# Strategy: exclude spacy-curated-transformers from resolution so the torch
# dependency chain is never pulled in.
set -euo pipefail

EXCLUDES=$(mktemp)
trap "rm -f $EXCLUDES" EXIT
echo "spacy-curated-transformers" > "$EXCLUDES"

uv tool install --reinstall --excludes "$EXCLUDES" .
