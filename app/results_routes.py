from fastapi import APIRouter, Path
from app.services import load_data, calculate_averages, filter_results_by_time

router = APIRouter()


@router.get("/results/average")
async def get_average():
    results = load_data()
    return calculate_averages(results)


@router.get("/results/average/{start_time}/{end_time}")
async def get_average_for_time_range(
    start_time: str = Path(
        example="2024-06-01 12:00:00", description="Start date and time in format: YYYY-MM-DD HH:MM:SS"
    ),
    end_time: str = Path(
        example="2024-06-01 13:00:00", description="End date and time in format: YYYY-MM-DD HH:MM:SS"
    ),
):
    results = load_data()
    filtered_results = filter_results_by_time(results, start_time, end_time)
    return calculate_averages(filtered_results)
