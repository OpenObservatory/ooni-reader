import unittest

from oonireader.report import Report

SOME_REPORT = """---
test_name: dns_consistency
...
---
entry: 0
...
---
[entry: 1]...
---
entry: 2
...
---
entry: 3
...
---
[entry: 4]...
---
[entry: 5]...
---
[entry: 6]...
---
[entry: 7]...
---
entry: 8
...
"""

class TestReport(unittest.TestCase):
    def test_invalid_report(self):
        with open('my_report.yaml', 'w+') as f:
            f.write(SOME_REPORT)
 
        r = Report('my_report.yaml')
        for idx, entry in enumerate(r.parse_entries()):
            pass

        assert idx == 8

if __name__ == "__main__":
    unittest.main()

