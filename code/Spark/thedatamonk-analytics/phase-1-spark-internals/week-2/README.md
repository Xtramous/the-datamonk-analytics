# Week 2: Spark Core Concepts & RDD Architecture

## 📚 Study Materials Created

### 1. **Complete HTML Study Guide** ⭐
**File:** `WEEK2_COMPLETE_GUIDE.html`

A comprehensive, interactive HTML document covering:
- RDD Fundamentals (5 core properties)
- Lazy Evaluation & DAG
- Transformations vs Actions
- Partitioning strategies
- Shuffles & Wide Transformations
- Caching & Persistence
- Performance optimization
- **5 L5-Level Interview Questions with detailed answers**

**How to use:**
```bash
# Open in browser
open WEEK2_COMPLETE_GUIDE.html
# or
google-chrome WEEK2_COMPLETE_GUIDE.html
```

---

## 🎯 Key Concepts Summary

### RDD Fundamentals
- **Resilient:** Fault tolerance via lineage
- **Distributed:** Data split across cluster
- **Immutable:** Cannot be changed
- **Lazy:** Operations deferred until action called

### Lazy Evaluation
```
rdd.map(...) → NOT executed (lazy)
rdd.filter(...) → NOT executed (lazy)
rdd.collect() → NOW everything executes! (action)
```

### Transformations vs Actions

**Transformations (Lazy):**
- `map(f)` - Apply function to each element
- `filter(f)` - Keep elements where f=True
- `reduceByKey(f)` - Aggregate by key (SHUFFLE!)
- `join(other)` - Join two RDDs (SHUFFLE!)

**Actions (Execute immediately):**
- `collect()` - Return all data to driver
- `count()` - Number of elements
- `first()` - First element
- `saveAsTextFile()` - Write to HDFS

### Narrow vs Wide Dependencies

| Aspect | Narrow | Wide |
|--------|--------|------|
| **Example** | map, filter | reduceByKey, join |
| **Shuffle** | No | YES (expensive!) |
| **Stage** | Same | New stage |
| **Recovery** | Fast | Slow |

### Partitioning Strategy

**Rule of thumb:**
```
num_partitions = num_cores * 2 to 4
```

Too few → underutilized cores
Too many → task scheduling overhead

### Caching Benefits

```python
filtered = rdd.filter(...).cache()

# First use: computes and caches
result1 = filtered.count()

# Second use: uses cache (much faster!)
result2 = filtered.sum()
```

---

## 📊 L5 Interview Questions Covered

1. **Fault Tolerance Design**
   - How Spark recovers from executor crashes
   - RDD lineage and recovery mechanism
   - Shuffle data considerations

2. **Performance & Optimization**
   - Designing pipelines for 100GB+ data
   - When to use take() vs collect()
   - Partition count selection

3. **Data Skew Problems**
   - Detecting skew with statistics
   - Salting technique
   - Isolation approach
   - Custom partitioner

4. **Complex Multi-Stage Pipelines**
   - Broadcast joins
   - Filter pushdown
   - Coalesce vs repartition
   - Performance metrics

5. **Lineage & Recovery Deep Dive**
   - Narrow vs wide dependency implications
   - Stage boundaries
   - Shuffle wait semantics

---

## 🔍 Diagrams Included

1. **RDD Lineage & Fault Tolerance** - Shows how data flows through transformations and how failures are recovered
2. **Lazy Evaluation Timeline** - Demonstrates when code executes
3. **Partitioning Architecture** - How data is distributed across executors
4. **Shuffle Operations** - Network communication in reduceByKey
5. **DAG Visualization** - Graph showing stage boundaries

---

## 💡 Key Takeaways

### Performance Optimization Tips

1. **Minimize Shuffles**
   - Chain narrow operations together
   - Use `reduceByKey` instead of `groupByKey`
   - Combine filters before wide transformations

2. **Partition Wisely**
   - Match cluster capacity (cores × 2-4)
   - Re-partition after heavy filtering
   - Use custom partitioners for skewed data

3. **Cache Strategically**
   - Cache RDDs used multiple times
   - Only cache before expensive operations
   - Unpersist when done

4. **Memory Management**
   - Use `take(n)` instead of `collect()`
   - Save large results to disk, not memory
   - Monitor executor memory in Web UI

### Common Mistakes to Avoid

❌ **DON'T:**
```python
# Collects 1 billion rows into driver memory → OOM!
result = huge_rdd.collect()

# groupByKey before reduceByKey (inefficient)
grouped = rdd.groupByKey()
result = grouped.map(lambda kv: (kv[0], sum(kv[1])))
```

✅ **DO:**
```python
# Take only what you need
result = huge_rdd.take(1000)

# Use reduceByKey (optimized with local reduction)
result = rdd.reduceByKey(lambda x, y: x + y)
```

---

## 📖 How to Study This Material

### Day 1-2: Fundamentals
- Read: RDD Fundamentals & Lazy Evaluation sections
- Study: 5 core properties of every RDD
- Review: Lineage diagrams

### Day 3-4: Transformations & Actions
- Study: All transformation types
- Practice: Distinguish narrow vs wide
- Review: When each action is appropriate

### Day 5-6: Partitioning & Shuffles
- Read: Partitioning strategy section
- Understand: Why shuffles are expensive
- Study: How to detect and avoid skew

### Day 7: Interview Prep
- Read all 5 L5 interview questions
- Understand the architecture behind each answer
- Practice explaining concepts out loud

---

## 🎓 Next Steps

After mastering Week 2 content:

1. **Practice:** Run code examples from `week2_rdd_examples.py`
2. **Interview Prep:** Review the 5 L5 questions daily
3. **Deep Dive:** Read Spark source code for lineage tracking
4. **Week 3:** Move to DataFrames & SQL optimization

---

## 📝 Quick Reference

### RDD Operations Cheat Sheet

```python
from pyspark import SparkContext, StorageLevel

sc = SparkContext("local", "App")

# Create RDD
rdd = sc.parallelize([1,2,3,4,5])
rdd = sc.textFile("path/to/file")

# Transformations (Lazy)
rdd.map(lambda x: x * 2)              # Narrow
rdd.filter(lambda x: x > 5)           # Narrow
rdd.flatMap(lambda x: [x, x*2])       # Narrow
rdd.reduceByKey(lambda x,y: x+y)      # Wide (SHUFFLE!)
rdd.groupByKey()                       # Wide (SHUFFLE!)
rdd.join(other_rdd)                    # Wide (SHUFFLE!)
rdd.distinct()                         # Wide (SHUFFLE!)

# Caching
rdd.cache()                            # Same as persist(MEMORY_ONLY)
rdd.persist(StorageLevel.MEMORY_AND_DISK)
rdd.unpersist()                        # Free memory

# Actions (Execute!)
rdd.collect()                          # Return all to driver
rdd.count()                            # Number of elements
rdd.first()                            # First element
rdd.take(10)                           # First 10 elements
rdd.sum()                              # Sum of all elements
rdd.saveAsTextFile("path")             # Write to HDFS

# Partitioning
rdd.repartition(10)                    # Change partitions (SHUFFLE!)
rdd.coalesce(5)                        # Reduce partitions (no shuffle)
rdd.getNumPartitions()                 # Get partition count
```

---

## 🔗 Resources

- **Spark Documentation:** https://spark.apache.org/docs/latest/rdd-programming-guide.html
- **Source Code:** https://github.com/apache/spark/tree/master/core/src/main/scala/org/apache/spark/rdd

---

**Last Updated:** June 2026
**Level:** L4-L5 (Senior Engineer / Staff Engineer)
