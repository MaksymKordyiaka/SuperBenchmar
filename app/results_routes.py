from fastapi import APIRouter
from app.services import load_data, calculate_averages, filter_results_by_time

router = APIRouter()


@router.get("/results/average")
async def get_average():
    results = load_data()
    return calculate_averages(results)


@router.get('/results/average/{start_time}/{end_time}')
async def get_average_for_time_range(start_time: str, end_time: str):
    results = load_data()
    filtered_results = filter_results_by_time(results, start_time, end_time)
    return calculate_averages(filtered_results)
