#!/usr/bin/env python3
"""Load testing script for Visa Dispute Agent"""
import asyncio
import httpx
import time
from datetime import datetime
from typing import List, Dict
import statistics


async def send_dispute(client: httpx.AsyncClient, dispute_id: str) -> Dict:
    """Send a single dispute request"""
    payload = {
        "dispute_id": dispute_id,
        "customer_id": f"cust_{dispute_id}",
        "transaction_id": f"txn_{dispute_id}",
        "amount": "150.00",
        "currency": "USD",
        "reason_code": "10.4",
        "description": "Customer claims unauthorized transaction for load testing",
        "timestamp": datetime.utcnow().isoformat()
    }
    
    start_time = time.time()
    try:
        response = await client.post(
            "http://localhost:8000/webhooks/dispute",
            json=payload,
            timeout=30.0
        )
        elapsed = time.time() - start_time
        
        return {
            "success": response.status_code == 202,
            "status_code": response.status_code,
            "elapsed": elapsed,
            "dispute_id": dispute_id
        }
    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "success": False,
            "error": str(e),
            "elapsed": elapsed,
            "dispute_id": dispute_id
        }


async def run_load_test(
    num_requests: int = 100,
    concurrent: int = 10
) -> Dict:
    """Run load test with specified parameters"""
    print(f"\n{'='*60}")
    print(f"Load Test Configuration")
    print(f"{'='*60}")
    print(f"Total Requests: {num_requests}")
    print(f"Concurrent Requests: {concurrent}")
    print(f"{'='*60}\n")
    
    results: List[Dict] = []
    
    async with httpx.AsyncClient() as client:
        # Create batches of concurrent requests
        for batch_start in range(0, num_requests, concurrent):
            batch_end = min(batch_start + concurrent, num_requests)
            batch_size = batch_end - batch_start
            
            print(f"Sending batch {batch_start//concurrent + 1} ({batch_size} requests)...")
            
            # Create tasks for this batch
            tasks = [
                send_dispute(client, f"load_test_{i}")
                for i in range(batch_start, batch_end)
            ]
            
            # Execute batch concurrently
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            
            # Small delay between batches
            await asyncio.sleep(0.1)
    
    # Calculate statistics
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    elapsed_times = [r["elapsed"] for r in results]
    
    stats = {
        "total_requests": num_requests,
        "successful": len(successful),
        "failed": len(failed),
        "success_rate": len(successful) / num_requests * 100,
        "latency": {
            "min": min(elapsed_times) if elapsed_times else 0,
            "max": max(elapsed_times) if elapsed_times else 0,
            "mean": statistics.mean(elapsed_times) if elapsed_times else 0,
            "median": statistics.median(elapsed_times) if elapsed_times else 0,
            "p95": statistics.quantiles(elapsed_times, n=20)[18] if len(elapsed_times) > 20 else 0,
            "p99": statistics.quantiles(elapsed_times, n=100)[98] if len(elapsed_times) > 100 else 0
        }
    }
    
    return stats


def print_results(stats: Dict) -> None:
    """Print load test results"""
    print(f"\n{'='*60}")
    print(f"Load Test Results")
    print(f"{'='*60}")
    print(f"Total Requests:    {stats['total_requests']}")
    print(f"Successful:        {stats['successful']} ({stats['success_rate']:.2f}%)")
    print(f"Failed:            {stats['failed']}")
    print(f"\nLatency (seconds):")
    print(f"  Min:             {stats['latency']['min']:.3f}s")
    print(f"  Max:             {stats['latency']['max']:.3f}s")
    print(f"  Mean:            {stats['latency']['mean']:.3f}s")
    print(f"  Median:          {stats['latency']['median']:.3f}s")
    print(f"  95th percentile: {stats['latency']['p95']:.3f}s")
    print(f"  99th percentile: {stats['latency']['p99']:.3f}s")
    print(f"{'='*60}\n")


async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load test Visa Dispute Agent")
    parser.add_argument(
        "--requests",
        type=int,
        default=100,
        help="Total number of requests (default: 100)"
    )
    parser.add_argument(
        "--concurrent",
        type=int,
        default=10,
        help="Number of concurrent requests (default: 10)"
    )
    
    args = parser.parse_args()
    
    # Check if server is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health", timeout=5.0)
            if response.status_code != 200:
                print("Error: Server is not healthy")
                return
    except Exception as e:
        print(f"Error: Cannot connect to server at http://localhost:8000")
        print(f"Make sure the server is running with: make run")
        return
    
    # Run load test
    start_time = time.time()
    stats = await run_load_test(args.requests, args.concurrent)
    total_time = time.time() - start_time
    
    # Add throughput
    stats["throughput"] = args.requests / total_time
    
    # Print results
    print_results(stats)
    print(f"Total Test Duration: {total_time:.2f}s")
    print(f"Throughput: {stats['throughput']:.2f} requests/second\n")


if __name__ == "__main__":
    asyncio.run(main())
