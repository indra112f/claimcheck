"""Offline tests: no network, no model. Run: python3 -m unittest test_claimcheck.py"""
import json
import unittest

import claimcheck as cc


class FakeModel:
    def __init__(self, answers):
        self.answers = list(answers)
        self.calls = self.prompt_tokens = self.completion_tokens = 0

    def chat(self, system, user, max_tokens=0):
        self.calls += 1
        return self.answers.pop(0)


SRC = {"https://docs.example/py": "Python 3.15 makes UTF-8 the default encoding for open(). "
       "The frozendict type is a new built-in immutable mapping. Possible candidates for frozendict in the stdlib "
       "include EnumType.__members__ and errno.errorcode."}
SRC_N = {u: cc.norm(t) for u, t in SRC.items()}


class Helpers(unittest.TestCase):
    def test_quote_in_normalizes(self):
        t = cc.norm("Claude Code’s  cache lasts\n one   hour — on a subscription.")
        self.assertTrue(cc.quote_in("Claude Code's cache lasts one hour - on a subscription", t))
        self.assertFalse(cc.quote_in("cache lasts two hours", t))
        self.assertFalse(cc.quote_in("hour", t))             # too short to count

    def test_quote_with_ellipsis_needs_every_piece(self):
        t = cc.norm("The first part is here. Much later the second part appears.")
        self.assertTrue(cc.quote_in("The first part is here ... the second part appears", t))
        self.assertFalse(cc.quote_in("The first part is here ... a made up ending", t))

    def test_links_skip_images_and_dedupe(self):
        md = "See [docs](https://a.dev/x). ![img](https://a.dev/i.png) <https://b.dev/y> [again](https://a.dev/x)."
        self.assertEqual(cc.md_links(md), ["https://a.dev/x", "https://b.dev/y"])

    def test_strip_code(self):
        md = "Text one.\n```python\nx = 'Python 2.7 is default'\n```\nText two."
        self.assertNotIn("Python 2.7", cc.strip_code(md))
        self.assertIn("Text two.", cc.strip_code(md))

    def test_html_to_text_drops_scripts_and_nav(self):
        h = "<nav>menu</nav><script>var a=1</script><p>Hello &amp; welcome</p><p>Second</p>"
        self.assertEqual(cc.html_to_text(h), "Hello & welcome\nSecond")

    def test_retrieval_prefers_numbers(self):
        src = {"u": "Version 3.14 notes. " * 60 + "In 3.15 the default encoding is UTF-8. " + "filler text " * 80}
        top = cc.top_passages("Python 3.15 default encoding UTF-8", src, k=1)
        self.assertIn("3.15", top[0][1])


class Verify(unittest.TestCase):
    def test_supported_with_real_quote(self):
        m = FakeModel([json.dumps({"verdict": "supported", "source": "S1",
                                   "evidence": "Python 3.15 makes UTF-8 the default encoding for open()."})])
        r = cc.verify(m, "Python 3.15 uses UTF-8 as the default encoding", SRC, SRC_N)
        self.assertEqual(r["verdict"], "supported")
        self.assertTrue(r["quote_checked"])

    def test_fabricated_evidence_is_downgraded(self):
        m = FakeModel([json.dumps({"verdict": "supported", "source": "S1",
                                   "evidence": "The stdlib now returns frozendict from EnumType.__members__."})])
        r = cc.verify(m, "The stdlib now returns frozendict from EnumType.__members__", SRC, SRC_N)
        self.assertEqual(r["verdict"], "not_found")
        self.assertIn("not in the source", r["note"])

    def test_contradiction_kept_when_quote_is_real(self):
        m = FakeModel([json.dumps({"verdict": "contradicted", "source": "S1",
                                   "evidence": "Possible candidates for frozendict in the stdlib include EnumType.__members__ and errno.errorcode."})])
        r = cc.verify(m, "EnumType.__members__ now returns a frozendict", SRC, SRC_N)
        self.assertEqual(r["verdict"], "contradicted")

    def test_garbage_answer_is_not_found(self):
        r = cc.verify(FakeModel(["I think so"]), "Python 3.15 UTF-8 default", SRC, SRC_N)
        self.assertEqual(r["verdict"], "not_found")


class Extract(unittest.TestCase):
    def test_claims_must_quote_the_draft(self):
        draft = "Python 3.15 makes UTF-8 the default.\n```\ncode 9.9\n```\nfrozendict is new."
        m = FakeModel([json.dumps([
            {"claim": "Python 3.15 defaults to UTF-8", "quote": "Python 3.15 makes UTF-8 the default"},
            {"claim": "Invented claim", "quote": "this sentence is not in the draft at all"},
            {"claim": "Python 3.15 defaults to UTF-8", "quote": "Python 3.15 makes UTF-8 the default"},
        ])])
        out = cc.extract_claims(m, draft, 10)
        self.assertEqual([c["claim"] for c in out], ["Python 3.15 defaults to UTF-8"])


class Report(unittest.TestCase):
    def test_report_orders_problems_first(self):
        res = [{"claim": "a", "quote": "qa", "verdict": "supported", "source": "u", "evidence": "e", "note": "", "quote_checked": True},
               {"claim": "b", "quote": "qb", "verdict": "contradicted", "source": "u", "evidence": "e2", "note": "n", "quote_checked": True}]
        st = {"model": "m", "calls": 3, "prompt_tokens": 10, "completion_tokens": 5, "seconds": 1, "sources_ok": 1, "sources_failed": 0}
        md = cc.report_md("d.md", res, st)
        self.assertLess(md.index("[WRONG] b"), md.index("[OK] a"))


if __name__ == "__main__":
    unittest.main()
