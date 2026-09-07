# 07 · Hash tables — compute the address instead of searching for it

> **The analogy.** A cloakroom. You hand over a coat and get ticket 47. When you come back, nobody searches the racks — the ticket *is* the location. The clever part is that the ticket number was **computed from the coat**, so you never had to be told where it went.

---

## 🎞️ Animations

**A key becomes an index, in constant time.**

![Hash function to bucket](../assets/anim/hash-function-bucket.svg)

**Two keys can land on the same index. That is expected, not broken.**

![Collision resolved by chaining](../assets/anim/hash-collision-chaining.svg)

---

## 🧠 Mental model

| Cloakroom | Hash table |
|:--|:--|
| the coat | the **key** |
| the rack slot | the **bucket** |
| the rule that turns a coat into a ticket number | the **hash function** |
| the numbered rack | the underlying **array** |
| two coats given the same ticket | a **collision** |
| hanging both coats on one hook | **separate chaining** |
| putting the second coat on the next free hook | **open addressing** |
| the cloakroom getting too full to work well | the **load factor** rising |

The whole idea is a swap: instead of *searching* for where something is, you *compute* where it must be. Searching is `O(n)`; computing is `O(1)`.

---

## 📐 Blueprint

![Hash table anatomy](../assets/blueprint/07-hash-tables.svg)

---

## 🗺️ Mindmap

```mermaid
flowchart LR
  H["Hash table"] --> F["Hash function"]
  H --> B["Bucket array"]
  H --> C["Collisions"]
  H --> R["Resizing"]

  F --> F1["deterministic — same key, same index"]
  F --> F2["uniform — scatters similar keys apart"]
  F --> F3["fast — O(1) in the key size"]

  B --> B1["index = hash mod capacity"]
  B --> B2["stores key AND value"]
  B --> B3["capacity is usually a power of two or a prime"]

  C --> C1["separate chaining — a list per bucket"]
  C --> C2["open addressing — probe for a free slot"]
  C --> C3["linear / quadratic probing, double hashing"]
  C --> C4["deletion needs tombstones when probing"]

  R --> R1["load factor = entries / buckets"]
  R --> R2["above ~0.75, grow and rehash"]
  R --> R3["rehash is O(n) — every key gets a new index"]

  classDef root fill:#0f2438,stroke:#38bdf8,stroke-width:2px,color:#e2e8f0
  classDef f fill:#0f2438,stroke:#c084fc,color:#c084fc
  classDef b fill:#0f2438,stroke:#34d399,color:#34d399
  classDef c fill:#0f2438,stroke:#fb7185,color:#fb7185
  classDef r fill:#0f2438,stroke:#fbbf24,color:#fbbf24
  class H root
  class F,F1,F2,F3 f
  class B,B1,B2,B3 b
  class C,C1,C2,C3,C4 c
  class R,R1,R2,R3 r
```

---

## ⚙️ Operations

**Lookup — with chaining.**

```text
function get(T, key)
    index ← hash(key) mod T.capacity            O(1)
    for each entry in T.buckets[index] do       walk this bucket's chain only
        if entry.key = key then                 compare the FULL key, not the hash
            return entry.value
        end
    end
    return notFound
```

> **Why compare the full key?** Because a matching index only means the hashes collided. Two different keys legitimately share a bucket, so the key itself is the final authority.

**Insert — with chaining and a growth check.**

```text
function put(T, key, value)
    index ← hash(key) mod T.capacity

    for each entry in T.buckets[index] do
        if entry.key = key then
            entry.value ← value                 update, do not duplicate
            return
        end
    end

    append (key, value) to T.buckets[index]
    T.count ← T.count + 1

    if T.count / T.capacity > 0.75 then
        resize(T)                               grow and rehash — O(n)
    end
```

**Resize — why every key must be recomputed.**

```text
function resize(T)
    old ← T.buckets
    T.capacity ← T.capacity × 2
    T.buckets ← new array of empty chains
    T.count ← 0

    for each chain in old do
        for each entry in chain do
            put(T, entry.key, entry.value)      index = hash mod capacity, and
        end                                     capacity just changed — so every
    end                                         key moves. This is the O(n) cost.
```

**Open addressing — the other collision policy.**

```text
function put(T, key, value)                     linear probing
    index ← hash(key) mod T.capacity
    while T.slots[index] is occupied and T.slots[index].key ≠ key do
        index ← (index + 1) mod T.capacity      just try the next slot
    end
    T.slots[index] ← (key, value)
```

> **The deletion trap.** With probing you cannot simply empty a slot — that would break the probe chain for keys that hopped over it. You must mark it as a **tombstone** ("was occupied, keep probing past me"), and periodically clean up.

<!-- python:examples/keyed.py:HashTable -->
#### 🐍 Python implementation

Separate chaining with a load factor that triggers the rehash:

<details open><summary><i>fold away</i></summary>

```python
class HashTable:
    """Separate chaining, with a load factor that triggers a rehash.

    The index is `hash(key) % capacity`, which is why changing the capacity
    moves essentially every key and makes a resize O(n).
    """

    def __init__(self, capacity: int = 8) -> None:
        self._capacity = max(1, capacity)
        self._buckets: list[list[tuple[Any, Any]]] = [[] for _ in range(self._capacity)]
        self._count = 0
        self.rehashes = 0

    def _index(self, key: Any) -> int:
        return hash(key) % self._capacity

    def put(self, key: Any, value: Any) -> None:
        chain = self._buckets[self._index(key)]
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain[i] = (key, value)      # update, never duplicate
                return
        chain.append((key, value))
        self._count += 1
        if self._count / self._capacity > LOAD_FACTOR_LIMIT:
            self._resize()

    def get(self, key: Any, default: Any = None) -> Any:
        for k, v in self._buckets[self._index(key)]:
            if k == key:                     # compare the FULL key: a matching
                return v                     # bucket only means the hashes agreed
        return default

    def delete(self, key: Any) -> bool:
        chain = self._buckets[self._index(key)]
        for i, (k, _) in enumerate(chain):
            if k == key:
                chain.pop(i)
                self._count -= 1
                return True
        return False

    def __contains__(self, key: Any) -> bool:
        return any(k == key for k, _ in self._buckets[self._index(key)])

    def __len__(self) -> int:
        return self._count

    @property
    def load_factor(self) -> float:
        return self._count / self._capacity

    def _resize(self) -> None:
        entries = [pair for chain in self._buckets for pair in chain]
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._count = 0
        self.rehashes += 1
        for k, v in entries:
            self.put(k, v)                   # every key gets a new index

    def items(self) -> Iterator[tuple[Any, Any]]:
        for chain in self._buckets:
            yield from chain
```

Every line above is covered by [`examples/test_examples.py`](../examples/test_examples.py) — run it with `python3 -m unittest discover -s examples -t .`
</details>
<!-- /python -->

---

## ⏱️ Complexity

| Operation | Average | Worst | Why the worst case |
|:--|:--:|:--:|:--|
| lookup | **O(1)** | O(n) | every key collides into one bucket |
| insert | **O(1)** | O(n) | same, plus the occasional `O(n)` rehash |
| delete | **O(1)** | O(n) | same |
| iterate all entries | O(n + capacity) | O(n + capacity) | you must skip the empty buckets too |
| ordered traversal | **impossible** | — | a hash table has no order at all |

**Space:** `O(n + capacity)`. A hash table deliberately keeps spare capacity — that slack is what keeps collisions rare.

> **How real libraries avoid the worst case:** modern implementations use randomised hash seeds (so an attacker cannot craft colliding keys — a real denial-of-service vector) and convert a bucket's chain into a balanced tree once it grows past a threshold, capping the worst case at `O(log n)`.

---

## ⚖️ Trade-offs

| ✅ Reach for a hash table when | ❌ Avoid a hash table when |
|:--|:--|
| you look things up **by key** | you need keys in sorted order — use a [balanced BST](11-balanced-trees.md) |
| you need the fastest possible membership test | you need range queries ("all keys between 10 and 20") |
| insertion order does not matter | you need the minimum or maximum cheaply — use a [heap](09-heaps.md) |
| you are de-duplicating — see [sets](08-sets.md) | worst-case latency must be bounded (the rehash is a spike) |
| your keys are hashable and compare cheaply | memory is very tight — the spare capacity is real |

---

## 🃏 Flashcards

<details><summary>What three properties must a hash function have?</summary>

**Deterministic** (same key always gives the same index), **uniform** (spreads keys evenly, and scatters similar keys apart), and **fast** (constant in practice). Lose determinism and lookups fail; lose uniformity and you get long chains.
</details>

<details><summary>Is a collision a bug?</summary>

**No.** With more possible keys than buckets, collisions are mathematically unavoidable — the pigeonhole principle. A hash table is *designed* around handling them. A collision is only a problem when there are too many, which is what the load factor tracks.
</details>

<details><summary>Chaining vs open addressing?</summary>

**Chaining** keeps a list per bucket: simple, tolerates a high load factor, but costs a pointer per entry and scatters memory. **Open addressing** probes for the next free slot: cache-friendly and no pointers, but degrades sharply near full and makes deletion awkward (tombstones).
</details>

<details><summary>What is the load factor and why does 0.75 keep appearing?</summary>

`entries / buckets`. Below ~0.75 collisions stay rare and operations stay effectively `O(1)`; above it, chains lengthen fast and performance falls off a cliff. 0.75 is the conventional compromise between wasted memory and collision rate.
</details>

<details><summary>Why does resizing require rehashing every key?</summary>

Because the index is `hash mod capacity`. Change the capacity and the modulo produces a different index for essentially every key, so every entry must be relocated. That is why resizing is `O(n)` and why you double rather than grow by one.
</details>

<details><summary>Why can a hash table not support range queries?</summary>

A good hash function deliberately destroys the relationship between keys — 10 and 11 land in unrelated buckets. There is no way to walk "the next key up" without scanning the whole table. Ordering is the thing you traded away for `O(1)`.
</details>

---

## ❓ Quiz

**1.** Two keys hash to the same index. With chaining, what does a lookup for the second key cost?

<details><summary>Answer</summary>

`O(1)` to compute the index, then a walk of that bucket's chain comparing full keys — `O(chain length)`, so `O(2)` here. Short chains are why the average stays `O(1)`.
</details>

**2.** Your hash function returns a constant. What have you built?

<details><summary>Answer</summary>

A **linked list wearing a hash table costume.** Every key lands in one bucket, so every operation walks the whole chain: `O(n)`. This is exactly the worst case, and exactly what a hash-collision DoS attack engineers deliberately.
</details>

**3.** You need to print all entries in sorted key order. What should you have used?

<details><summary>Answer</summary>

A **balanced BST** (a sorted map). From a hash table your only option is to extract every key and sort them — `O(n log n)` every time you ask. If ordered output is a requirement, the hash table was the wrong choice.
</details>

**4.** Why must you compare the full key after finding the bucket, rather than trusting the hash?

<details><summary>Answer</summary>

Because the bucket index is `hash mod capacity`, so a match means only that two keys' hashes agreed *modulo the capacity* — an enormous number of unrelated keys satisfy that. Skipping the key comparison returns other people's values.
</details>

---

⬅️ [06 · Queues](06-queues.md) · [🏠 Index](../README.md) · [08 · Sets](08-sets.md) ➡️
