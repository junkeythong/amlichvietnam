import time
import datetime as dt
from lunar_vn import solar_to_lunar


def benchmark():
    start_date = dt.date(1900, 1, 1)
    end_date = dt.date(2100, 12, 31)
    
    # Pre-generate dates to avoid measuring date generation
    dates = []
    curr = start_date
    while curr <= end_date:
        dates.append(curr)
        curr += dt.timedelta(days=1)
    
    total = len(dates)
    print(f"Benchmarking {total} conversions (1900-2100)...")
    
    start_time = time.perf_counter()
    for d in dates:
        _ = solar_to_lunar(d)
    end_time = time.perf_counter()
    
    duration = end_time - start_time
    rate = total / duration
    
    print("-" * 30)
    print(f"Total time:  {duration:.4f} seconds")
    print(f"Mean speed:  {rate:,.0f} conversions/sec")
    print("-" * 30)


if __name__ == "__main__":
    benchmark()
