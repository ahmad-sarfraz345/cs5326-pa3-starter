#!/usr/bin/env bash
set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: bash make_submission.sh <roll_number>"
    echo "Example: bash make_submission.sh 24100123"
    exit 1
fi

ROLL_NUMBER=$1
ARCHIVE_NAME="${ROLL_NUMBER}_pa3.zip"

echo "Creating submission archive: ${ARCHIVE_NAME}"

# Verify required files exist
if [ ! -f "submission_adapter.py" ]; then
    echo "Error: submission_adapter.py not found in repository root."
    exit 1
fi

if [ ! -d "src" ]; then
    echo "Error: src/ directory not found."
    exit 1
fi

# Run public smoke tests
echo "Running public smoke tests..."
python -m pytest -v tests/test_public_adapter_smoke.py || echo "Warning: Some tests failed. Proceeding with packaging."

# Create zip archive
zip -r "${ARCHIVE_NAME}" \
    src/ \
    submission_adapter.py \
    outputs/results_summary.json \
    REPORT.pdf \
    -x "__pycache__/*" "src/__pycache__/*" "*.pyc"

echo "=========================================="
echo "Successfully generated: ${ARCHIVE_NAME}"
echo "Please verify its contents and upload to the LMS."
echo "=========================================="

