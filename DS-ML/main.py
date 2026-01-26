import sys
from src.pipeline.auto_pipeline import run_pipeline

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise ValueError("Please provide path to CSV file")

    csv_path = sys.argv[1]
    run_pipeline(csv_path)
