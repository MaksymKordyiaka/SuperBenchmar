import os
import json
import logging
from datetime import datetime
from fastapi import HTTPException
from app.schemas import BenchmarkingResult
from dotenv import load_dotenv

load_dotenv()
DEBUG = os.getenv("SUPERBENCHMARK_DEBUG", "False").lower() in ["true", "1"]

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def load_data(file_path: str = 'test_database.json') -> list[BenchmarkingResult]:
    if not DEBUG:
        raise HTTPException(status_code=501, detail="Feature not ready for production use")

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
        results = data.get("benchmarking_results", [])
        return [BenchmarkingResult(**result) for result in results]
    except Exception as e:
        logger.error(f"Error loading data from {file_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading data from {file_path}")


def calculate_averages(results: list[BenchmarkingResult]) -> dict:
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    try:
        total_tokens = sum(item.token_count for item in results)
        total_time_to_first_token = sum(item.time_to_first_token for item in results)
        total_time_per_output_token = sum(item.time_per_output_token for item in results)
        total_generation_time = sum(item.total_generation_time for item in results)

        count = len(results)

        return {
            "average_token_count": total_tokens / count,
            "average_time_to_first_token (ms)": total_time_to_first_token / count,
            "average_time_per_output_token (ms)": total_time_per_output_token / count,
            "average_total_generation_time (ms)": total_generation_time / count
        }
    except Exception as e:
        logger.error(f"Error calculating averages: {e}")
        raise HTTPException(status_code=400, detail='Error calculating averages')


def filter_results_by_time(results: list[BenchmarkingResult],
                           start_time: str, end_time: str) -> list[BenchmarkingResult]:
    try:
        start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logger.error(f"Invalid date format: {e}")
        raise HTTPException(status_code=400, detail="Invalid date format")

    filtered_results = [
        result for result in results
        if start_datetime <= result.timestamp <= end_datetime
    ]
    return filtered_results
