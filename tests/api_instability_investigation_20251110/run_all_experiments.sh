#!/bin/bash
# Run all API instability investigation experiments
# Usage: ./run_all_experiments.sh [phase]
#   phase: 1, 2, all (default: all)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Create results directory
mkdir -p results

echo "=========================================="
echo "API Instability Investigation"
echo "=========================================="
echo ""

PHASE=${1:-all}

run_phase_1() {
    echo "Phase 1: Basic Investigation (High Priority)"
    echo "------------------------------------------"
    echo ""

    echo "[1/2] Running Experiment 3A: Response Structure Logging..."
    python3 experiment_3a_response_logging.py
    echo ""

    echo "[2/2] Running Experiment 6A: Manual Cross-check..."
    python3 experiment_6a_manual_crosscheck.py
    echo ""

    echo "Phase 1 completed!"
    echo ""
}

run_phase_2() {
    echo "Phase 2: Timing & Rate Control (High Priority)"
    echo "-----------------------------------------------"
    echo ""

    echo "[1/1] Running Experiment 1A: Query Complexity..."
    python3 experiment_1a_query_complexity.py
    echo ""

    echo "Phase 2 completed!"
    echo ""
}

# Main execution
case "$PHASE" in
    1)
        run_phase_1
        ;;
    2)
        run_phase_2
        ;;
    all)
        run_phase_1
        run_phase_2
        ;;
    *)
        echo "Error: Unknown phase '$PHASE'"
        echo "Usage: $0 [1|2|all]"
        exit 1
        ;;
esac

echo "=========================================="
echo "All requested experiments completed!"
echo "=========================================="
echo ""
echo "Results saved to: $SCRIPT_DIR/results/"
echo ""
echo "Next steps:"
echo "1. Review generated reports in results/"
echo "2. Compare findings with investigation_plan.md"
echo "3. Update search validation scripts based on findings"
echo ""
