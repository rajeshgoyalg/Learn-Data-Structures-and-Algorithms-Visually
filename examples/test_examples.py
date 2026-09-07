"""Tests for every reference implementation in `examples/`.

stdlib `unittest` only -- no pytest, no install. Run with:

    python3 -m unittest discover -s examples -v

The snippets embedded in `docs/` are excerpts of the code these tests cover,
so a claim made in a module is a claim something here actually checks.
"""
from __future__ import annotations

import random
import unittest

from examples.algorithms import (binary_search, bubble_sort, coin_change_dp,
                                 coin_change_greedy, factorial, fib_memo,
                                 fib_naive, fib_table, fib_two_vars,
                                 insertion_sort, linear_search, lower_bound,
                                 merge_sort, partition, quick_sort,
                                 selection_sort, solve_n_queens)
from examples.graphs import (Graph, bfs, dfs, dijkstra, has_cycle, path_to,
                             shortest_path_unweighted, topological_sort)
from examples.hierarchical import (AVLTree, BST, MinHeap, Trie, heapsort, top_k)
from examples.keyed import HashTable, intersection, unique
from examples.linear import (CircularLinkedList, DoublyLinkedList,
                             DynamicArray, SinglyLinkedList)
from examples.restricted import (CircularQueue, Deque, PriorityQueue, Queue,
                                 Stack, is_balanced)

SORTS = (bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort)


class TestDynamicArray(unittest.TestCase):
    def test_append_doubles_capacity(self):
        a = DynamicArray(2)
        for x in range(9):
            a.append(x)
        self.assertEqual(list(a), list(range(9)))
        self.assertGreaterEqual(a.capacity, 9)

    def test_amortised_copies_stay_linear(self):
        n = 1000
        a = DynamicArray(1)
        for x in range(n):
            a.append(x)
        # doubling copies fewer than 2n elements in total across n appends
        self.assertLess(a.copies, 2 * n)

    def test_insert_and_delete_shift(self):
        a = DynamicArray()
        for x in [10, 20, 30, 40, 50]:
            a.append(x)
        a.insert_at(2, 25)
        self.assertEqual(list(a), [10, 20, 25, 30, 40, 50])
        self.assertEqual(a.delete_at(0), 10)
        self.assertEqual(list(a), [20, 25, 30, 40, 50])

    def test_bounds(self):
        a = DynamicArray()
        a.append(1)
        with self.assertRaises(IndexError):
            _ = a[1]
        with self.assertRaises(IndexError):
            a.delete_at(5)


class TestSinglyLinkedList(unittest.TestCase):
    def test_insert_after_preserves_tail(self):
        ll = SinglyLinkedList(["A", "B", "D"])
        b = ll.head.next
        SinglyLinkedList.insert_after(b, "C")
        self.assertEqual(ll.to_list(), ["A", "B", "C", "D"])

    def test_delete_after_routes_around(self):
        ll = SinglyLinkedList(["A", "B", "C", "D"])
        self.assertEqual(SinglyLinkedList.delete_after(ll.head.next), "C")
        self.assertEqual(ll.to_list(), ["A", "B", "D"])

    def test_get_costs_k_hops(self):
        ll = SinglyLinkedList(list(range(10)))
        self.assertEqual(ll.get(7), 7)
        with self.assertRaises(IndexError):
            ll.get(99)

    def test_reverse(self):
        ll = SinglyLinkedList([1, 2, 3, 4])
        ll.reverse()
        self.assertEqual(ll.to_list(), [4, 3, 2, 1])

    def test_reverse_of_empty_and_single(self):
        for values in ([], [1]):
            ll = SinglyLinkedList(values)
            ll.reverse()
            self.assertEqual(ll.to_list(), values[::-1])

    def test_cycle_detection(self):
        ll = SinglyLinkedList([1, 2, 3])
        self.assertFalse(ll.has_cycle())
        ll.head.next.next.next = ll.head          # close the loop
        self.assertTrue(ll.has_cycle())


class TestDoublyAndCircular(unittest.TestCase):
    def test_walks_both_ways(self):
        d = DoublyLinkedList([1, 2, 3])
        self.assertEqual(d.forward(), [1, 2, 3])
        self.assertEqual(d.backward(), [3, 2, 1])

    def test_delete_by_reference_is_o1(self):
        d = DoublyLinkedList([1, 2, 3])
        middle = d.head.next
        self.assertEqual(d.delete(middle), 2)
        self.assertEqual(d.forward(), [1, 3])
        self.assertEqual(d.backward(), [3, 1])

    def test_delete_endpoints(self):
        d = DoublyLinkedList([1, 2, 3])
        d.delete(d.head)
        d.delete(d.tail)
        self.assertEqual(d.forward(), [2])

    def test_circular_never_ends_on_none(self):
        c = CircularLinkedList(["A", "B", "C"])
        self.assertEqual(c.traverse_once(), ["A", "B", "C"])
        node = c.head
        for _ in range(7):                        # keep walking past the end
            node = node.next
        self.assertIsNotNone(node)


class TestStackAndQueues(unittest.TestCase):
    def test_stack_is_lifo(self):
        s = Stack()
        for x in (1, 2, 3):
            s.push(x)
        self.assertEqual([s.pop(), s.pop()], [3, 2])
        self.assertEqual(s.peek(), 1)

    def test_stack_underflow(self):
        with self.assertRaises(IndexError):
            Stack().pop()

    def test_balanced_brackets(self):
        for good in ("", "()", "{[()]}", "a(b)[c]{d}"):
            self.assertTrue(is_balanced(good), good)
        for bad in ("(", ")", "([)]", "(()"):
            self.assertFalse(is_balanced(bad), bad)

    def test_queue_is_fifo(self):
        q = Queue()
        for x in "ABC":
            q.enqueue(x)
        self.assertEqual(q.dequeue(), "A")
        self.assertEqual(q.peek(), "B")
        self.assertEqual(len(q), 2)

    def test_queue_survives_churn(self):
        q = Queue()
        for x in range(200):
            q.enqueue(x)
        got = [q.dequeue() for _ in range(200)]
        self.assertEqual(got, list(range(200)))

    def test_circular_queue_reuses_freed_slots(self):
        cq = CircularQueue(3)
        cq.enqueue("A"); cq.enqueue("B")
        self.assertEqual(cq.dequeue(), "A")
        cq.enqueue("C"); cq.enqueue("D")          # wraps into the freed slot
        self.assertTrue(cq.is_full)
        with self.assertRaises(OverflowError):
            cq.enqueue("E")
        self.assertEqual([cq.dequeue() for _ in range(3)], ["B", "C", "D"])

    def test_deque_both_ends(self):
        d = Deque()
        d.push_back(2); d.push_back(3); d.push_front(1)
        self.assertEqual((d.pop_front(), d.pop_back()), (1, 3))

    def test_priority_queue_ignores_arrival_order(self):
        pq = PriorityQueue()
        for name, pri in [("Ann", 5), ("Bo", 1), ("Cy", 4), ("Di", 2)]:
            pq.insert(name, pri)
        self.assertEqual(pq.peek(), "Bo")
        self.assertEqual([pq.extract_min() for _ in range(4)],
                         ["Bo", "Di", "Cy", "Ann"])

    def test_priority_queue_breaks_ties_by_arrival(self):
        pq = PriorityQueue()
        for n in ["first", "second", "third"]:
            pq.insert(n, 1)
        self.assertEqual([pq.extract_min() for _ in range(3)],
                         ["first", "second", "third"])


class TestHashTableAndSets(unittest.TestCase):
    def test_put_get_update_delete(self):
        h = HashTable(4)
        h.put("a", 1)
        h.put("a", 2)                             # update, not duplicate
        self.assertEqual(len(h), 1)
        self.assertEqual(h.get("a"), 2)
        self.assertTrue(h.delete("a"))
        self.assertFalse(h.delete("a"))
        self.assertIsNone(h.get("a"))

    def test_resize_keeps_every_key_reachable(self):
        h = HashTable(2)
        for i in range(200):
            h.put(f"k{i}", i)
        self.assertGreater(h.rehashes, 0)
        self.assertLessEqual(h.load_factor, 0.75)
        for i in range(200):
            self.assertEqual(h.get(f"k{i}"), i)   # nothing lost in a rehash

    def test_collisions_do_not_lose_entries(self):
        class Same:
            def __init__(self, k): self.k = k
            def __hash__(self): return 1          # force every key into one bucket
            def __eq__(self, o): return isinstance(o, Same) and o.k == self.k
        h = HashTable(8)
        for i in range(10):
            h.put(Same(i), i)
        self.assertEqual(len(h), 10)
        self.assertEqual(h.get(Same(7)), 7)

    def test_unique_preserves_first_seen_order(self):
        self.assertEqual(unique([5, 3, 5, 9, 3]), [5, 3, 9])

    def test_intersection_is_symmetric(self):
        a, b = {1, 2, 3}, {2, 3, 4}
        self.assertEqual(intersection(a, b), {2, 3})
        self.assertEqual(intersection(b, a), {2, 3})


class TestHeap(unittest.TestCase):
    def test_heap_property_holds_everywhere(self):
        h = MinHeap([random.randint(0, 999) for _ in range(200)])
        a = h.as_list()
        for i in range(1, len(a)):
            self.assertLessEqual(a[(i - 1) // 2], a[i])

    def test_extract_min_yields_sorted_order(self):
        values = [random.randint(0, 99) for _ in range(60)]
        h = MinHeap(values)
        self.assertEqual([h.extract_min() for _ in range(len(values))],
                         sorted(values))

    def test_insert_then_peek(self):
        h = MinHeap([3, 5, 8, 9, 7, 10, 12])
        h.insert(2)
        self.assertEqual(h.peek(), 2)

    def test_heapsort(self):
        self.assertEqual(heapsort([38, 27, 43, 9, 82, 10]),
                         [9, 10, 27, 38, 43, 82])

    def test_top_k_uses_bounded_memory(self):
        self.assertEqual(top_k(iter([5, 1, 9, 3, 7, 8]), 3), [9, 8, 7])
        self.assertEqual(top_k(iter([1, 2]), 5), [2, 1])
        self.assertEqual(top_k(iter([1, 2]), 0), [])

    def test_empty_raises(self):
        with self.assertRaises(IndexError):
            MinHeap().extract_min()


class TestBST(unittest.TestCase):
    def setUp(self):
        self.b = BST([50, 30, 70, 20, 40, 60, 80])

    def test_search(self):
        self.assertTrue(self.b.search(40))
        self.assertFalse(self.b.search(45))

    def test_in_order_is_always_sorted(self):
        values = [random.randint(0, 999) for _ in range(120)]
        got = BST(values).in_order()
        self.assertEqual(got, sorted(set(values)))

    def test_traversal_orders(self):
        self.assertEqual(self.b.in_order(), [20, 30, 40, 50, 60, 70, 80])
        self.assertEqual(self.b.pre_order(), [50, 30, 20, 40, 70, 60, 80])
        self.assertEqual(self.b.post_order(), [20, 40, 30, 60, 80, 70, 50])
        self.assertEqual(self.b.level_order(), [50, 30, 70, 20, 40, 60, 80])

    def test_min_max(self):
        self.assertEqual((self.b.minimum(), self.b.maximum()), (20, 80))

    def test_delete_all_three_cases(self):
        self.b.delete(20)                         # leaf
        self.b.delete(70)                         # two children
        self.assertEqual(self.b.in_order(), [30, 40, 50, 60, 80])
        one = BST([10, 5, 7])
        one.delete(5)                             # one child
        self.assertEqual(one.in_order(), [7, 10])

    def test_sorted_input_degenerates(self):
        self.assertEqual(BST([10, 20, 30, 40, 50]).height(), 5)


class TestAVL(unittest.TestCase):
    def test_stays_logarithmic_on_sorted_input(self):
        n = 1000
        avl = AVLTree(list(range(n)))
        self.assertEqual(avl.in_order(), list(range(n)))
        self.assertLessEqual(avl.height(), 2 * (n.bit_length()))

    def test_beats_plain_bst_on_the_same_input(self):
        values = list(range(64))
        self.assertGreater(BST(values).height(), AVLTree(values).height())

    def test_all_four_rotation_cases(self):
        for case in ([30, 20, 10], [10, 20, 30], [30, 10, 20], [10, 30, 20]):
            t = AVLTree(case)
            self.assertEqual(t.height(), 2, case)
            self.assertEqual(t.in_order(), sorted(case), case)

    def test_random_inserts_keep_the_invariant(self):
        values = random.sample(range(10_000), 400)
        t = AVLTree(values)
        self.assertEqual(t.in_order(), sorted(values))
        for v in values[:50]:
            self.assertTrue(t.search(v))


class TestTrie(unittest.TestCase):
    def setUp(self):
        self.t = Trie(["cat", "car", "care", "dog"])

    def test_prefix_is_not_a_word(self):
        self.assertTrue(self.t.search("cat"))
        self.assertFalse(self.t.search("ca"))
        self.assertTrue(self.t.starts_with("ca"))
        self.assertFalse(self.t.starts_with("cz"))

    def test_autocomplete_returns_only_matches(self):
        self.assertEqual(self.t.autocomplete("ca"), ["car", "care", "cat"])
        self.assertEqual(self.t.autocomplete("d"), ["dog"])
        self.assertEqual(self.t.autocomplete("zz"), [])

    def test_delete_keeps_other_words_reachable(self):
        self.t.delete("care")
        self.assertFalse(self.t.search("care"))
        self.assertTrue(self.t.search("car"))     # must survive
        self.assertTrue(self.t.search("cat"))

    def test_delete_absent_word_is_a_noop(self):
        self.assertFalse(self.t.delete("cart"))
        self.assertTrue(self.t.search("car"))

    def test_empty_string(self):
        t = Trie([""])
        self.assertTrue(t.search(""))


class TestGraphs(unittest.TestCase):
    def setUp(self):
        self.g = Graph()
        for u, v, w in [("A", "B", 4), ("A", "C", 2), ("B", "D", 5),
                        ("B", "E", 10), ("C", "E", 3), ("C", "F", 8),
                        ("D", "G", 4), ("E", "G", 6), ("F", "G", 2)]:
            self.g.add_edge(u, v, w)

    def test_bfs_visits_by_distance(self):
        self.assertEqual(bfs(self.g, "A"), ["A", "B", "C", "D", "E", "F", "G"])

    def test_dfs_goes_deep(self):
        self.assertEqual(dfs(self.g, "A"), ["A", "B", "D", "G", "E", "C", "F"])

    def test_both_visit_every_reachable_node_once(self):
        self.assertCountEqual(bfs(self.g, "A"), dfs(self.g, "A"))

    def test_unweighted_shortest_path_minimises_edges(self):
        path = shortest_path_unweighted(self.g, "A", "G")
        self.assertEqual(len(path), 4)                 # A -> ? -> ? -> G
        self.assertEqual((path[0], path[-1]), ("A", "G"))
        self.assertEqual(shortest_path_unweighted(self.g, "A", "A"), ["A"])

    def test_unreachable_returns_none(self):
        g = Graph()
        g.add_edge("a", "b")
        g.add_vertex("z")
        self.assertIsNone(shortest_path_unweighted(g, "a", "z"))

    def test_dijkstra_matches_the_worked_trace(self):
        dist, prev = dijkstra(self.g, "A")
        self.assertEqual(dist["C"], 2)
        self.assertEqual(dist["E"], 5)
        self.assertEqual(dist["G"], 11)                # not 12 via F, not 13 via D
        self.assertEqual(path_to(prev, "G"), ["A", "C", "E", "G"])

    def test_dijkstra_rejects_negative_weights(self):
        g = Graph()
        g.add_edge("p", "q", -3)
        with self.assertRaises(ValueError):
            dijkstra(g, "p")

    def test_cycle_detection_and_topological_sort(self):
        dag = Graph(directed=True)
        for u, v in [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d")]:
            dag.add_edge(u, v)
        self.assertFalse(has_cycle(dag))
        order = topological_sort(dag)
        self.assertIsNotNone(order)
        self.assertLess(order.index("a"), order.index("d"))

        cyclic = Graph(directed=True)
        for u, v in [("x", "y"), ("y", "z"), ("z", "x")]:
            cyclic.add_edge(u, v)
        self.assertTrue(has_cycle(cyclic))
        self.assertIsNone(topological_sort(cyclic))    # the circular-dep error


class TestSearching(unittest.TestCase):
    def test_linear_search(self):
        self.assertEqual(linear_search([12, 7, 41, 3, 90, 55], 55), 5)
        self.assertEqual(linear_search([], 1), -1)

    def test_binary_search_against_reference(self):
        values = sorted(random.sample(range(1000), 200))
        for target in values[:20] + [-1, 1001]:
            expected = values.index(target) if target in values else -1
            self.assertEqual(binary_search(values, target), expected)

    def test_binary_search_edges(self):
        self.assertEqual(binary_search([], 1), -1)
        self.assertEqual(binary_search([5], 5), 0)
        self.assertEqual(binary_search([1, 2], 2), 1)

    def test_lower_bound_is_the_insertion_point(self):
        import bisect
        values = sorted(random.sample(range(200), 60))
        for target in range(-2, 202, 7):
            self.assertEqual(lower_bound(values, target),
                             bisect.bisect_left(values, target))


class TestSorting(unittest.TestCase):
    def test_all_sorts_agree_with_sorted(self):
        for _ in range(25):
            values = [random.randint(-50, 50) for _ in range(random.randint(0, 40))]
            for fn in SORTS:
                self.assertEqual(fn(values), sorted(values), fn.__name__)

    def test_sorts_do_not_mutate_the_input(self):
        values = [3, 1, 2]
        for fn in SORTS:
            fn(values)
            self.assertEqual(values, [3, 1, 2], fn.__name__)

    def test_already_sorted_and_reversed(self):
        for values in (list(range(30)), list(range(30))[::-1], [7] * 10):
            for fn in SORTS:
                self.assertEqual(fn(values), sorted(values), fn.__name__)

    def test_merge_and_insertion_are_stable(self):
        values = [(1, "a"), (0, "x"), (1, "b"), (0, "y")]
        expected = [(0, "x"), (0, "y"), (1, "a"), (1, "b")]
        for fn in (merge_sort, insertion_sort, bubble_sort):
            self.assertEqual(fn(values), expected, fn.__name__)

    def test_partition_places_the_pivot_finally(self):
        a = [10, 80, 30, 90, 40, 50, 70]
        p = partition(a, 0, len(a) - 1)
        self.assertEqual(a[p], 70)
        self.assertTrue(all(x <= 70 for x in a[:p]))
        self.assertTrue(all(x > 70 for x in a[p + 1:]))

    def test_quicksort_survives_its_worst_case_input(self):
        self.assertEqual(quick_sort(list(range(300))), list(range(300)))


class TestRecursionAndParadigms(unittest.TestCase):
    def test_factorial(self):
        self.assertEqual([factorial(n) for n in range(6)], [1, 1, 2, 6, 24, 120])

    def test_n_queens(self):
        self.assertEqual(solve_n_queens(4), [[1, 3, 0, 2], [2, 0, 3, 1]])
        self.assertEqual(len(solve_n_queens(8)), 92)
        self.assertEqual(solve_n_queens(3), [])          # no solution exists

    def test_no_four_queens_solution_starts_at_column_zero(self):
        # the animation must not claim otherwise
        self.assertFalse([s for s in solve_n_queens(4) if s[0] == 0])

    def test_every_fibonacci_variant_agrees(self):
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        for fn in (fib_naive, fib_memo, fib_table, fib_two_vars):
            self.assertEqual([fn(n) for n in range(10)], expected, fn.__name__)

    def test_fib_zero_is_zero_in_every_variant(self):
        for fn in (fib_naive, fib_memo, fib_table, fib_two_vars):
            self.assertEqual(fn(0), 0, fn.__name__)

    def test_memo_scales_where_naive_cannot(self):
        self.assertEqual(fib_memo(90), 2880067194370816120)

    def test_greedy_is_optimal_for_us_coins(self):
        coins = coin_change_greedy(63)
        self.assertEqual(sum(coins), 63)
        self.assertEqual(len(coins), 6)

    def test_greedy_loses_on_a_hostile_coin_system(self):
        greedy = coin_change_greedy(6, (1, 3, 4))
        self.assertEqual(len(greedy), 3)                 # 4 + 1 + 1
        self.assertEqual(coin_change_dp(6, (1, 3, 4)), 2)  # 3 + 3 is better

    def test_coin_change_dp_reports_impossible(self):
        self.assertEqual(coin_change_dp(7, (5,)), -1)


if __name__ == "__main__":
    unittest.main()
