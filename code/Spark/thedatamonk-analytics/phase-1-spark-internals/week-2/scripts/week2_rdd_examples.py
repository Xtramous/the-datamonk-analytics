#!/usr/bin/env python3
"""
Week 2: RDD Fundamentals & Core Concepts
Practical examples covering:
- RDD creation and lineage
- Lazy evaluation
- Transformations vs Actions
- Partitioning
- Shuffles
- Caching
"""

from pyspark import SparkContext, StorageLevel
import time

def example1_lazy_evaluation():
    """
    Demonstrate lazy evaluation - transformations don't execute immediately
    """
    print("\n" + "="*70)
    print("EXAMPLE 1: Lazy Evaluation")
    print("="*70)

    sc = SparkContext("local", "LazyEvaluation")

    # Step 1: Create RDD
    print("\n[1] Creating RDD from [1..10]...")
    start = time.time()
    rdd1 = sc.parallelize(range(1, 11))
    print(f"    Created in {time.time()-start:.4f}s (instantaneous)")

    # Step 2: Apply transformation (NO EXECUTION)
    print("\n[2] Applying map(x*2) - LAZY, no execution...")
    start = time.time()
    rdd2 = rdd1.map(lambda x: x * 2)
    print(f"    Map applied in {time.time()-start:.4f}s (instant!)")

    # Step 3: Apply another transformation (NO EXECUTION)
    print("\n[3] Applying filter(x > 10) - LAZY, no execution...")
    start = time.time()
    rdd3 = rdd2.filter(lambda x: x > 10)
    print(f"    Filter applied in {time.time()-start:.4f}s (instant!)")

    # Step 4: Show lineage (before execution)
    print("\n[4] RDD Lineage (dependencies):")
    print(rdd3.toDebugString().decode())

    # Step 5: Execute action
    print("\n[5] Calling collect() - NOW EXECUTION HAPPENS!")
    start = time.time()
    result = rdd3.collect()
    execution_time = time.time() - start
    print(f"    Executed in {execution_time:.4f}s")
    print(f"    Result: {result}")

    sc.stop()


def example2_transformations_and_actions():
    """
    Demonstrate different transformations and actions
    """
    print("\n" + "="*70)
    print("EXAMPLE 2: Transformations vs Actions")
    print("="*70)

    sc = SparkContext("local", "TransformationsActions")

    # Create sample data
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    rdd = sc.parallelize(data, numPartitions=2)

    print(f"\nOriginal data: {data}")

    # TRANSFORMATIONS (Narrow)
    print("\n--- NARROW TRANSFORMATIONS (no shuffle) ---")

    # map
    rdd_map = rdd.map(lambda x: x * 2)
    print(f"\nmap(x*2): {rdd_map.collect()}")

    # filter
    rdd_filter = rdd.filter(lambda x: x > 5)
    print(f"filter(x>5): {rdd_filter.collect()}")

    # flatMap
    rdd_flat = rdd.flatMap(lambda x: [x, x*2])
    print(f"flatMap([x, x*2]): {rdd_flat.collect()}")

    # TRANSFORMATIONS (Wide - with shuffle)
    print("\n--- WIDE TRANSFORMATIONS (require shuffle) ---")

    # Create (key, value) pairs
    pairs = rdd.map(lambda x: ("even" if x % 2 == 0 else "odd", x))
    print(f"\nPairs: {pairs.collect()}")

    # reduceByKey
    summed = pairs.reduceByKey(lambda x, y: x + y)
    print(f"reduceByKey(sum): {summed.collect()}")

    # groupByKey
    grouped = pairs.groupByKey()
    print(f"groupByKey(): {[(k, list(v)) for k, v in grouped.collect()]}")

    # ACTIONS (trigger execution)
    print("\n--- ACTIONS (trigger execution) ---")

    print(f"\ncount(): {rdd.count()}")
    print(f"first(): {rdd.first()}")
    print(f"take(3): {rdd.take(3)}")
    print(f"sum: {rdd.sum()}")
    print(f"min: {rdd.min()}")
    print(f"max: {rdd.max()}")

    sc.stop()


def example3_partitioning():
    """
    Demonstrate partitioning and data distribution
    """
    print("\n" + "="*70)
    print("EXAMPLE 3: Partitioning Strategy")
    print("="*70)

    sc = SparkContext("local[4]", "Partitioning")  # 4 cores

    # Create RDD with different partition counts
    data = range(1, 101)

    print(f"\nData size: 100 elements, 4 cores available")

    # Few partitions
    print("\n--- TOO FEW PARTITIONS (underutilized) ---")
    rdd_few = sc.parallelize(data, numPartitions=1)
    print(f"Partitions: {rdd_few.getNumPartitions()}")
    print(f"Partition sizes: {rdd_few.mapPartitions(lambda x: [sum(1 for _ in x)]).collect()}")
    print("Issue: Only 1 core used, others idle")

    # Optimal partitions
    print("\n--- OPTIMAL PARTITIONS (matches cores) ---")
    rdd_opt = sc.parallelize(data, numPartitions=4)
    print(f"Partitions: {rdd_opt.getNumPartitions()}")
    partition_sizes = rdd_opt.mapPartitions(lambda x: [sum(1 for _ in x)]).collect()
    print(f"Partition sizes: {partition_sizes}")
    print("Benefit: All 4 cores utilized equally")

    # Too many partitions
    print("\n--- TOO MANY PARTITIONS (overhead) ---")
    rdd_many = sc.parallelize(data, numPartitions=16)
    print(f"Partitions: {rdd_many.getNumPartitions()}")
    partition_sizes = rdd_many.mapPartitions(lambda x: [sum(1 for _ in x)]).collect()
    print(f"Partition sizes: {partition_sizes}")
    print("Issue: Task scheduling overhead, many small partitions")

    # Re-partitioning
    print("\n--- RE-PARTITIONING ---")
    rdd_repart = rdd_few.repartition(4)
    print(f"Repartitioned from 1 to {rdd_repart.getNumPartitions()} partitions")
    partition_sizes = rdd_repart.mapPartitions(lambda x: [sum(1 for _ in x)]).collect()
    print(f"New partition sizes: {partition_sizes}")
    print("Note: Causes SHUFFLE - all data moves between partitions")

    sc.stop()


def example4_narrow_vs_wide():
    """
    Demonstrate narrow vs wide transformations and their impact
    """
    print("\n" + "="*70)
    print("EXAMPLE 4: Narrow vs Wide Transformations")
    print("="*70)

    sc = SparkContext("local", "NarrowVsWide")

    data = [("a", 1), ("b", 2), ("a", 3), ("b", 4), ("c", 5)]
    rdd = sc.parallelize(data, numPartitions=2)

    print(f"\nOriginal data: {data}")
    print(f"Partitions: 2")

    # NARROW TRANSFORMATION
    print("\n--- NARROW TRANSFORMATION: map ---")
    mapped = rdd.map(lambda kv: (kv[0], kv[1] * 2))
    print(f"Result: {mapped.collect()}")
    print("Effect: Each partition processed independently")
    print("Partitions: Still 2 (no shuffle)")
    print("Stage boundary: No (same stage)")

    # WIDE TRANSFORMATION
    print("\n--- WIDE TRANSFORMATION: reduceByKey ---")
    reduced = rdd.reduceByKey(lambda x, y: x + y)
    print(f"Result: {reduced.collect()}")
    print("Effect: Data shuffled - same keys grouped together")
    print("Partitions: Default (200 or spark.sql.shuffle.partitions)")
    print("Stage boundary: Yes (new stage created)")
    print("Network I/O: Yes - all-to-all shuffle")

    # Show stage info
    print("\n--- DAG VISUALIZATION ---")
    print("Narrow chain:")
    print("  RDD → map → RDD'  (all in Stage 1)")
    print("\nWide transformation:")
    print("  RDD → reduceByKey → RDD'  (RDD in Stage 1, shuffle, RDD' in Stage 2)")

    sc.stop()


def example5_shuffles():
    """
    Demonstrate shuffle operations and their performance impact
    """
    print("\n" + "="*70)
    print("EXAMPLE 5: Shuffles & Wide Transformations")
    print("="*70)

    sc = SparkContext("local", "Shuffles")

    # Create sample data
    data = [("user1", 10), ("user2", 20), ("user1", 15), ("user3", 5), ("user2", 10)]
    rdd = sc.parallelize(data)

    print(f"\nOriginal data: {data}")

    # groupByKey (causes shuffle)
    print("\n--- groupByKey (causes shuffle) ---")
    grouped = rdd.groupByKey()
    result = [(k, list(v)) for k, v in grouped.collect()]
    print(f"Result: {result}")

    # reduceByKey (also causes shuffle, but optimized)
    print("\n--- reduceByKey (also shuffles, but optimized) ---")
    reduced = rdd.reduceByKey(lambda x, y: x + y)
    print(f"Result: {reduced.collect()}")
    print("\nDifference:")
    print("groupByKey: [user1 → [10,15]], [user2 → [20,10]]")
    print("reduceByKey: [user1 → 25], [user2 → 30]")
    print("reduceByKey is preferred - does local reduction before shuffle!")

    sc.stop()


def example6_caching():
    """
    Demonstrate caching and persistence
    """
    print("\n" + "="*70)
    print("EXAMPLE 6: Caching & Persistence")
    print("="*70)

    sc = SparkContext("local", "Caching")

    # Create large RDD
    rdd = sc.parallelize(range(1, 1000001))  # 1 million elements

    # Expensive transformation
    filtered = rdd.filter(lambda x: x % 2 == 0)  # 500k elements

    print("\nTest 1: Without cache (recomputed each action)")

    # First use
    start = time.time()
    result1 = filtered.count()
    time1 = time.time() - start
    print(f"  count(): {result1} in {time1:.4f}s")

    # Second use (recomputes!)
    start = time.time()
    result2 = filtered.sum()
    time2 = time.time() - start
    print(f"  sum(): {result2} in {time2:.4f}s")
    print(f"  Total time: {time1 + time2:.4f}s")

    # With cache
    print("\nTest 2: With cache (computed once, reused)")

    cached = rdd.filter(lambda x: x % 2 == 0).cache()

    # First use (computes and caches)
    start = time.time()
    result1 = cached.count()
    time1 = time.time() - start
    print(f"  count(): {result1} in {time1:.4f}s (computes + caches)")

    # Second use (uses cache)
    start = time.time()
    result2 = cached.sum()
    time2 = time.time() - start
    print(f"  sum(): {result2} in {time2:.4f}s (uses cache)")
    print(f"  Total time: {time1 + time2:.4f}s")
    print(f"\nSpeedup: {(time1 + time2):.1f}x faster with cache!")

    # Different storage levels
    print("\n--- Storage Levels ---")
    rdd_mem = rdd.cache()  # MEMORY_ONLY
    rdd_disk = rdd.persist(StorageLevel.MEMORY_AND_DISK)

    print("MEMORY_ONLY: Fast, may OOM if data > memory")
    print("MEMORY_AND_DISK: Spills to disk if memory full")
    print("DISK_ONLY: Always uses disk")

    # Cleanup
    rdd_mem.unpersist()
    rdd_disk.unpersist()

    sc.stop()


def example7_optimization():
    """
    Optimization techniques and best practices
    """
    print("\n" + "="*70)
    print("EXAMPLE 7: Performance Optimization Techniques")
    print("="*70)

    sc = SparkContext("local[4]", "Optimization")

    # Sample data
    words = sc.parallelize(
        ["apple", "banana", "apple", "cherry", "banana", "apple"] * 1000,
        numPartitions=4
    )

    print("\nProblem: Count words using groupByKey vs reduceByKey")

    # Inefficient: groupByKey
    print("\n--- INEFFICIENT: groupByKey ---")
    pairs = words.map(lambda w: (w, 1))
    grouped = pairs.groupByKey()
    result_slow = grouped.map(lambda kv: (kv[0], sum(kv[1]))).collect()
    print(f"Result: {sorted(result_slow)}")
    print("Problem: All values for each key collected into memory")

    # Efficient: reduceByKey
    print("\n--- EFFICIENT: reduceByKey ---")
    result_fast = pairs.reduceByKey(lambda x, y: x + y).collect()
    print(f"Result: {sorted(result_fast)}")
    print("Benefit: Local reduction happens first, then shuffle")

    # Chaining operations
    print("\n--- CHAINING OPERATIONS ---")
    print("Bad: Multiple maps")
    result = (words
        .map(lambda w: w.upper())
        .map(lambda w: (w, 1))
        .map(lambda kv: kv)  # unnecessary!
        .collect())

    print("Good: Single map chain")
    result = (words
        .map(lambda w: (w.upper(), 1))
        .collect())

    sc.stop()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("WEEK 2: RDD FUNDAMENTALS & CORE CONCEPTS - PRACTICAL EXAMPLES")
    print("="*70)

    # Run all examples
    example1_lazy_evaluation()
    example2_transformations_and_actions()
    example3_partitioning()
    example4_narrow_vs_wide()
    example5_shuffles()
    example6_caching()
    example7_optimization()

    print("\n" + "="*70)
    print("✅ All examples completed!")
    print("="*70)
