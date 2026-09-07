"""Tests for the per-operation functions embedded in docs/.

Every snippet in a module's Operations section is one of these functions, so
these tests are what make the code in the docs trustworthy.

    python3 -m unittest discover -s examples -t .
"""
from __future__ import annotations

import bisect
import itertools
import random
import unittest

from examples import ops_avl as avl
from examples import ops_bst as bst
from examples import ops_dijkstra as dij
from examples import ops_doubly as dbl
from examples import ops_graph as gr
from examples import ops_hash as ht
from examples import ops_heap as hp
from examples import ops_linked_list as ll
from examples import ops_paradigms as par
from examples import ops_queue as q
from examples import ops_recursion as rec
from examples import ops_search as se
from examples import ops_sets as st
from examples import ops_sort as so
from examples import ops_stack as sk
from examples import ops_trie as tr
from examples.nodes import DNode, Node, TrieNode
from examples.ops_arrays import append, delete_at, get, grow, insert_at

SORTS = (so.bubble_sort, so.selection_sort, so.insertion_sort,
         so.merge_sort, so.quick_sort)


def make_list(values):
    head = None
    for v in reversed(values):
        head = ll.prepend(head, v)
    return head


class TestArrayOps(unittest.TestCase):
    def test_get_and_bounds(self):
        store, n = [10, 20, 30, None, None], 3
        self.assertEqual(get(store, n, 1), 20)
        for bad in (-1, 3, 99):
            with self.assertRaises(IndexError):
                get(store, n, bad)

    def test_insert_at_shifts_right(self):
        store, n = [10, 20, 30, 40, 50, None], 5
        n = insert_at(store, n, 2, 25)
        self.assertEqual(store[:n], [10, 20, 25, 30, 40, 50])

    def test_insert_at_front_moves_everything(self):
        store, n = [1, 2, 3, None], 3
        n = insert_at(store, n, 0, 0)
        self.assertEqual(store[:n], [0, 1, 2, 3])

    def test_delete_at_closes_the_gap(self):
        store, n = [10, 20, 30, 40], 4
        n = delete_at(store, n, 1)
        self.assertEqual(store[:n], [10, 30, 40])
        self.assertIsNone(store[3])

    def test_grow_doubles_and_copies(self):
        store, n = [1, 2, 3], 3
        bigger = grow(store, n)
        self.assertEqual(len(bigger), 6)
        self.assertEqual(bigger[:3], [1, 2, 3])

    def test_append_grows_only_when_full(self):
        store, n = [1, 2], 2
        store, n = append(store, n, 3)
        self.assertEqual((store[:n], len(store)), ([1, 2, 3], 4))
        store, n = append(store, n, 4)
        self.assertEqual(len(store), 4)          # no growth needed this time

    def test_amortised_copies_stay_linear(self):
        store, n, total = [None], 0, 0
        for x in range(500):
            before = len(store)
            store, n = append(store, n, x)
            if len(store) != before:
                total += n - 1
        self.assertLess(total, 2 * 500)


class TestLinkedListOps(unittest.TestCase):
    def test_traverse_and_get(self):
        h = make_list(["A", "B", "C", "D"])
        self.assertEqual(ll.traverse(h), ["A", "B", "C", "D"])
        self.assertEqual(ll.get(h, 2), "C")
        with self.assertRaises(IndexError):
            ll.get(h, 9)

    def test_insert_after_keeps_the_tail(self):
        h = make_list(["A", "B", "D"])
        ll.insert_after(h.next, "C")
        self.assertEqual(ll.traverse(h), ["A", "B", "C", "D"])

    def test_prepend_returns_the_new_head(self):
        h = ll.prepend(make_list(["B"]), "A")
        self.assertEqual(ll.traverse(h), ["A", "B"])

    def test_delete_after(self):
        h = make_list(["A", "B", "C"])
        self.assertEqual(ll.delete_after(h), "B")
        self.assertEqual(ll.traverse(h), ["A", "C"])
        tail = h.next
        self.assertIsNone(ll.delete_after(tail))  # nothing after the tail

    def test_reverse(self):
        for values in ([], [1], [1, 2], [1, 2, 3, 4]):
            h = ll.reverse(make_list(values))
            self.assertEqual(ll.traverse(h), values[::-1], values)

    def test_has_cycle(self):
        h = make_list([1, 2, 3])
        self.assertFalse(ll.has_cycle(h))
        h.next.next.next = h
        self.assertTrue(ll.has_cycle(h))


class TestDoublyAndCircularOps(unittest.TestCase):
    def test_insert_after_links_both_ways(self):
        a = DNode(1)
        b = dbl.insert_after(a, 2)
        c = dbl.insert_after(b, 3)
        self.assertEqual(dbl.walk_backward(c), [3, 2, 1])
        self.assertIs(c.prev, b)
        self.assertIs(b.next, c)

    def test_delete_by_reference(self):
        a = DNode(1)
        b = dbl.insert_after(a, 2)
        c = dbl.insert_after(b, 3)
        self.assertEqual(dbl.delete(b), 2)
        self.assertEqual(dbl.walk_backward(c), [3, 1])
        self.assertIs(a.next, c)
        self.assertIs(c.prev, a)

    def test_circular_traversal_terminates(self):
        a, b = Node("X"), Node("Y")
        a.next, b.next = b, a
        self.assertEqual(dbl.traverse_once(a), ["X", "Y"])
        self.assertEqual(dbl.traverse_once(None), [])

    def test_next_turn_wraps_forever(self):
        a, b = Node(1), Node(2)
        a.next, b.next = b, a
        node = a
        for _ in range(11):
            node = dbl.next_turn(node)
        self.assertIs(node, b)            # never None, never an error


class TestStackOps(unittest.TestCase):
    def test_lifo(self):
        s = []
        for x in (1, 2, 3):
            sk.push(s, x)
        self.assertEqual(sk.pop(s), 3)
        self.assertEqual(sk.peek(s), 2)
        self.assertFalse(sk.is_empty(s))

    def test_underflow(self):
        with self.assertRaises(IndexError):
            sk.pop([])
        with self.assertRaises(IndexError):
            sk.peek([])

    def test_balanced(self):
        for good in ("", "()", "{[()]}", "a(b)[c]{d}"):
            self.assertTrue(sk.is_balanced(good), good)
        for bad in ("(", ")", "([)]", "(()", "]"):
            self.assertFalse(sk.is_balanced(bad), bad)


class TestQueueOps(unittest.TestCase):
    def test_fifo(self):
        qq = []
        for x in "ABC":
            q.enqueue(qq, x)
        self.assertEqual(q.dequeue(qq), "A")
        with self.assertRaises(IndexError):
            q.dequeue([])

    def test_circular_reuses_freed_slots(self):
        slots = [None] * 3
        rear, count, front = -1, 0, 0
        rear, count = q.circular_enqueue(slots, rear, count, "A")
        rear, count = q.circular_enqueue(slots, rear, count, "B")
        value, front, count = q.circular_dequeue(slots, front, count)
        self.assertEqual(value, "A")
        rear, count = q.circular_enqueue(slots, rear, count, "C")
        rear, count = q.circular_enqueue(slots, rear, count, "D")
        self.assertEqual(rear, 0)                 # wrapped
        self.assertEqual(count, 3)
        with self.assertRaises(OverflowError):
            q.circular_enqueue(slots, rear, count, "E")
        got = []
        for _ in range(3):
            v, front, count = q.circular_dequeue(slots, front, count)
            got.append(v)
        self.assertEqual(got, ["B", "C", "D"])

    def test_priority_queue_order_and_ties(self):
        heap, tie = [], itertools.count()
        for name, pri in [("Ann", 5), ("Bo", 1), ("Cy", 4), ("Di", 2)]:
            q.pq_insert(heap, name, pri, tie)
        self.assertEqual([q.pq_extract_min(heap) for _ in range(4)],
                         ["Bo", "Di", "Cy", "Ann"])
        heap, tie = [], itertools.count()
        for n in ["first", "second", "third"]:
            q.pq_insert(heap, n, 1, tie)
        self.assertEqual([q.pq_extract_min(heap) for _ in range(3)],
                         ["first", "second", "third"])


class TestHashOps(unittest.TestCase):
    def test_put_get_update_delete(self):
        b = [[] for _ in range(8)]
        self.assertTrue(ht.put(b, "a", 1))
        self.assertFalse(ht.put(b, "a", 2))       # update, not a new key
        self.assertEqual(ht.get(b, "a"), 2)
        self.assertTrue(ht.delete(b, "a"))
        self.assertFalse(ht.delete(b, "a"))
        self.assertIsNone(ht.get(b, "a"))

    def test_resize_keeps_everything_reachable(self):
        b = [[] for _ in range(2)]
        for i in range(50):
            ht.put(b, f"k{i}", i)
        before = ht.load_factor(b)
        b = ht.resize(b)
        self.assertLess(ht.load_factor(b), before)
        for i in range(50):
            self.assertEqual(ht.get(b, f"k{i}"), i)

    def test_collisions_do_not_lose_entries(self):
        class Same:
            def __init__(self, k): self.k = k
            def __hash__(self): return 7
            def __eq__(self, o): return isinstance(o, Same) and o.k == self.k
        b = [[] for _ in range(8)]
        for i in range(10):
            ht.put(b, Same(i), i)
        self.assertEqual(ht.get(b, Same(4)), 4)
        self.assertEqual(sum(len(c) for c in b), 10)


class TestSetOps(unittest.TestCase):
    def test_unique_keeps_first_seen_order(self):
        self.assertEqual(st.unique([5, 3, 5, 9, 3]), [5, 3, 9])
        self.assertEqual(st.unique([]), [])

    def test_algebra(self):
        a, b = {1, 2, 3}, {2, 3, 4}
        self.assertEqual(st.intersection(a, b), {2, 3})
        self.assertEqual(st.intersection(b, a), {2, 3})
        self.assertEqual(st.union(a, b), {1, 2, 3, 4})
        self.assertEqual(st.difference(a, b), {1})

    def test_seen_before_terminates_on_a_cycle(self):
        g = {"a": ["b"], "b": ["c"], "c": ["a"]}
        self.assertEqual(st.seen_before("a", lambda n: g[n]), ["a", "b", "c"])


class TestHeapOps(unittest.TestCase):
    def test_index_arithmetic(self):
        self.assertEqual((hp.left(0), hp.right(0)), (1, 2))
        self.assertEqual(hp.parent(1), 0)
        self.assertEqual(hp.parent(2), 0)
        self.assertEqual(hp.parent(hp.left(5)), 5)

    def test_heap_property_after_build(self):
        h = hp.build_heap([random.randint(0, 999) for _ in range(200)])
        for i in range(1, len(h)):
            self.assertLessEqual(h[hp.parent(i)], h[i])

    def test_insert_and_peek(self):
        h = hp.build_heap([3, 5, 8, 9, 7, 10, 12])
        hp.insert(h, 2)
        self.assertEqual(hp.peek(h), 2)

    def test_extract_min_is_sorted_order(self):
        values = [random.randint(0, 99) for _ in range(60)]
        h = hp.build_heap(values)
        self.assertEqual([hp.extract_min(h) for _ in range(len(values))],
                         sorted(values))

    def test_heapsort_and_empty(self):
        self.assertEqual(hp.heapsort([38, 27, 43, 9, 82, 10]),
                         [9, 10, 27, 38, 43, 82])
        with self.assertRaises(IndexError):
            hp.extract_min([])
        with self.assertRaises(IndexError):
            hp.peek([])


class TestBSTOps(unittest.TestCase):
    def build(self, values):
        root = None
        for v in values:
            root = bst.insert(root, v)
        return root

    def test_search(self):
        r = self.build([50, 30, 70, 20, 40, 60, 80])
        self.assertTrue(bst.search(r, 40))
        self.assertFalse(bst.search(r, 45))
        self.assertFalse(bst.search(None, 1))

    def test_in_order_is_always_sorted(self):
        values = [random.randint(0, 999) for _ in range(150)]
        self.assertEqual(bst.in_order(self.build(values)), sorted(set(values)))

    def test_all_four_traversals(self):
        r = self.build([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(bst.in_order(r), [20, 30, 40, 50, 60, 70, 80])
        self.assertEqual(bst.pre_order(r), [50, 30, 20, 40, 70, 60, 80])
        self.assertEqual(bst.post_order(r), [20, 40, 30, 60, 80, 70, 50])
        self.assertEqual(bst.level_order(r), [50, 30, 70, 20, 40, 60, 80])
        self.assertEqual(bst.level_order(None), [])

    def test_min_max_height(self):
        r = self.build([50, 30, 70, 20, 40, 60, 80])
        self.assertEqual((bst.minimum(r), bst.maximum(r)), (20, 80))
        self.assertEqual(bst.height(r), 3)

    def test_delete_all_three_cases(self):
        r = self.build([50, 30, 70, 20, 40, 60, 80])
        r = bst.delete(r, 20)                     # leaf
        r = bst.delete(r, 70)                     # two children
        self.assertEqual(bst.in_order(r), [30, 40, 50, 60, 80])
        one = self.build([10, 5, 7])
        one = bst.delete(one, 5)                  # one child
        self.assertEqual(bst.in_order(one), [7, 10])
        self.assertIsNone(bst.delete(None, 1))

    def test_sorted_input_degenerates(self):
        self.assertEqual(bst.height(self.build([10, 20, 30, 40, 50])), 5)


class TestAVLOps(unittest.TestCase):
    def build(self, values):
        root = None
        for v in values:
            root = avl.insert(root, v)
        return root

    def test_all_four_rotation_cases(self):
        for case in ([30, 20, 10], [10, 20, 30], [30, 10, 20], [10, 30, 20]):
            t = self.build(case)
            self.assertEqual(bst.height(t), 2, case)
            self.assertEqual(bst.in_order(t), sorted(case), case)

    def test_rotations_preserve_the_ordering(self):
        t = self.build([10, 20, 30])
        self.assertEqual(bst.in_order(t), [10, 20, 30])
        self.assertEqual(t.value, 20)             # 20 became the root

    def test_stays_logarithmic_on_sorted_input(self):
        n = 500
        t = self.build(list(range(n)))
        self.assertEqual(bst.in_order(t), list(range(n)))
        self.assertLessEqual(bst.height(t), 2 * n.bit_length())

    def test_beats_a_plain_bst_on_the_same_input(self):
        values = list(range(64))
        plain = None
        for v in values:
            plain = bst.insert(plain, v)
        self.assertGreater(bst.height(plain), bst.height(self.build(values)))

    def test_balance_factor_stays_within_one(self):
        t = self.build(random.sample(range(10_000), 300))

        def check(node):
            if node is None:
                return
            self.assertIn(avl.balance_factor(node), (-1, 0, 1))
            check(node.left)
            check(node.right)
        check(t)


class TestTrieOps(unittest.TestCase):
    def build(self, words):
        root = TrieNode()
        for w in words:
            tr.insert(root, w)
        return root

    def test_prefix_is_not_a_word(self):
        r = self.build(["cat", "car", "care", "dog"])
        self.assertTrue(tr.search(r, "cat"))
        self.assertFalse(tr.search(r, "ca"))
        self.assertTrue(tr.starts_with(r, "ca"))
        self.assertFalse(tr.starts_with(r, "cz"))

    def test_shared_prefix_costs_one_node(self):
        r = self.build(["cat"])
        before = sum(1 for _ in self.walk(r))
        tr.insert(r, "car")
        after = sum(1 for _ in self.walk(r))
        self.assertEqual(after - before, 1)

    def walk(self, node):
        yield node
        for child in node.children.values():
            yield from self.walk(child)

    def test_autocomplete(self):
        r = self.build(["cat", "car", "care", "dog"])
        self.assertEqual(tr.autocomplete(r, "ca"), ["car", "care", "cat"])
        self.assertEqual(tr.autocomplete(r, "d"), ["dog"])
        self.assertEqual(tr.autocomplete(r, "zz"), [])

    def test_delete_keeps_other_words(self):
        r = self.build(["cat", "car", "care"])
        self.assertTrue(tr.delete(r, "care"))
        self.assertFalse(tr.search(r, "care"))
        self.assertTrue(tr.search(r, "car"))
        self.assertTrue(tr.search(r, "cat"))
        self.assertFalse(tr.delete(r, "cart"))    # never stored

    def test_empty_string(self):
        r = self.build([""])
        self.assertTrue(tr.search(r, ""))


class TestGraphOps(unittest.TestCase):
    def setUp(self):
        self.directed = {"A": ["B", "C"], "B": ["D", "E"], "C": ["E", "F"],
                         "D": ["G"], "E": ["G"], "F": ["G"], "G": []}
        self.undirected = {k: list(v) for k, v in self.directed.items()}
        for u, vs in self.directed.items():
            for v in vs:
                self.undirected[v].append(u)

    def test_bfs_by_distance(self):
        self.assertEqual(gr.bfs(self.undirected, "A"),
                         ["A", "B", "C", "D", "E", "F", "G"])

    def test_dfs_goes_deep(self):
        self.assertEqual(gr.dfs(self.undirected, "A"),
                         ["A", "B", "D", "G", "E", "C", "F"])

    def test_both_visit_each_node_once(self):
        self.assertCountEqual(gr.bfs(self.undirected, "A"),
                              gr.dfs(self.undirected, "A"))

    def test_shortest_unweighted_path(self):
        p = gr.shortest_path_unweighted(self.undirected, "A", "G")
        self.assertEqual((p[0], p[-1], len(p)), ("A", "G", 4))
        self.assertEqual(gr.shortest_path_unweighted(self.undirected, "A", "A"), ["A"])
        self.assertIsNone(gr.shortest_path_unweighted({"a": [], "z": []}, "a", "z"))

    def test_cycle_detection(self):
        self.assertFalse(gr.has_cycle(self.directed))
        self.assertTrue(gr.has_cycle({"x": ["y"], "y": ["z"], "z": ["x"]}))

    def test_topological_sort(self):
        order = gr.topological_sort(self.directed)
        self.assertIsNotNone(order)
        self.assertLess(order.index("A"), order.index("G"))
        self.assertIsNone(gr.topological_sort({"x": ["y"], "y": ["x"]}))


class TestSearchOps(unittest.TestCase):
    def test_linear(self):
        self.assertEqual(se.linear_search([12, 7, 41, 3, 90, 55], 55), 5)
        self.assertEqual(se.linear_search([], 1), -1)

    def test_binary_against_reference(self):
        values = sorted(random.sample(range(1000), 200))
        for target in values[:20] + [-1, 1001]:
            expected = values.index(target) if target in values else -1
            self.assertEqual(se.binary_search(values, target), expected)

    def test_binary_edges(self):
        self.assertEqual(se.binary_search([], 1), -1)
        self.assertEqual(se.binary_search([5], 5), 0)
        self.assertEqual(se.binary_search([1, 2], 2), 1)

    def test_lower_bound_matches_bisect(self):
        values = sorted(random.sample(range(200), 60))
        for target in range(-2, 202, 5):
            self.assertEqual(se.lower_bound(values, target),
                             bisect.bisect_left(values, target))


class TestSortOps(unittest.TestCase):
    def test_all_agree_with_sorted(self):
        for _ in range(25):
            values = [random.randint(-50, 50) for _ in range(random.randint(0, 40))]
            for fn in SORTS:
                self.assertEqual(fn(values), sorted(values), fn.__name__)

    def test_none_mutate_their_input(self):
        values = [3, 1, 2]
        for fn in SORTS:
            fn(values)
            self.assertEqual(values, [3, 1, 2], fn.__name__)

    def test_sorted_reversed_and_duplicates(self):
        for values in (list(range(30)), list(range(30))[::-1], [7] * 10, []):
            for fn in SORTS:
                self.assertEqual(fn(values), sorted(values), fn.__name__)

    def test_stability(self):
        values = [(1, "a"), (0, "x"), (1, "b"), (0, "y")]
        expected = [(0, "x"), (0, "y"), (1, "a"), (1, "b")]
        for fn in (so.merge_sort, so.insertion_sort, so.bubble_sort):
            self.assertEqual(fn(values), expected, fn.__name__)

    def test_merge_takes_the_smaller_front(self):
        self.assertEqual(so.merge([1, 3, 5], [2, 4]), [1, 2, 3, 4, 5])
        self.assertEqual(so.merge([], [1]), [1])

    def test_partition_locks_the_pivot(self):
        a = [10, 80, 30, 90, 40, 50, 70]
        p = so.partition(a, 0, len(a) - 1)
        self.assertEqual(a[p], 70)
        self.assertTrue(all(x <= 70 for x in a[:p]))
        self.assertTrue(all(x > 70 for x in a[p + 1:]))

    def test_quicksort_survives_its_worst_case(self):
        self.assertEqual(so.quick_sort(list(range(300))), list(range(300)))


class TestRecursionOps(unittest.TestCase):
    def test_factorial(self):
        self.assertEqual([rec.factorial(n) for n in range(6)],
                         [1, 1, 2, 6, 24, 120])

    def test_n_queens(self):
        self.assertEqual(rec.solve_n_queens(4), [[1, 3, 0, 2], [2, 0, 3, 1]])
        self.assertEqual(len(rec.solve_n_queens(8)), 92)
        self.assertEqual(rec.solve_n_queens(3), [])

    def test_no_solution_starts_at_column_zero(self):
        # the animation must not claim otherwise
        self.assertFalse([s for s in rec.solve_n_queens(4) if s[0] == 0])


class TestParadigmOps(unittest.TestCase):
    def test_every_fib_variant_agrees(self):
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        for fn in (par.fib_naive, par.fib_memo, par.fib_table, par.fib_two_vars):
            self.assertEqual([fn(n) for n in range(10)], expected, fn.__name__)

    def test_fib_zero(self):
        for fn in (par.fib_naive, par.fib_memo, par.fib_table, par.fib_two_vars):
            self.assertEqual(fn(0), 0, fn.__name__)

    def test_memo_scales_where_naive_cannot(self):
        self.assertEqual(par.fib_memo(90), 2880067194370816120)

    def test_greedy_optimal_for_us_coins(self):
        coins = par.coin_change_greedy(63)
        self.assertEqual((sum(coins), len(coins)), (63, 6))

    def test_greedy_loses_on_a_hostile_coin_system(self):
        self.assertEqual(len(par.coin_change_greedy(6, (1, 3, 4))), 3)
        self.assertEqual(par.coin_change_dp(6, (1, 3, 4)), 2)

    def test_dp_reports_impossible(self):
        self.assertEqual(par.coin_change_dp(7, (5,)), -1)


class TestDijkstraOps(unittest.TestCase):
    def setUp(self):
        self.w = {"A": [("B", 4), ("C", 2)], "B": [("D", 5), ("E", 10)],
                  "C": [("E", 3), ("F", 8)], "D": [("G", 4)],
                  "E": [("G", 6)], "F": [("G", 2)], "G": []}
        for u in list(self.w):
            for v, wt in list(self.w[u]):
                self.w[v].append((u, wt))

    def test_relax_only_improves(self):
        dist = {"a": 0.0, "b": float("inf")}
        prev = {"a": None, "b": None}
        self.assertTrue(dij.relax(dist, prev, "a", "b", 5))
        self.assertEqual((dist["b"], prev["b"]), (5, "a"))
        self.assertFalse(dij.relax(dist, prev, "a", "b", 9))   # 9 > 5: rejected
        self.assertEqual(dist["b"], 5)

    def test_matches_the_worked_trace(self):
        dist, prev = dij.dijkstra(self.w, "A")
        self.assertEqual(dist["C"], 2)
        self.assertEqual(dist["E"], 5)
        self.assertEqual(dist["G"], 11)          # not 12 via F, not 13 via D
        self.assertEqual(dij.path_to(prev, "G"), ["A", "C", "E", "G"])

    def test_rejects_negative_weights(self):
        with self.assertRaises(ValueError):
            dij.dijkstra({"p": [("q", -3)], "q": []}, "p")

    def test_unreachable_stays_infinite(self):
        dist, _ = dij.dijkstra({"a": [], "z": []}, "a")
        self.assertEqual(dist["z"], dij.INFINITY)


if __name__ == "__main__":
    unittest.main()
