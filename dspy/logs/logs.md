## logs track progress step by step

use naming convention <step integer>-log.md             e.g. 1-logs.md
advanced <step integer>-<step increment>-log.md         e.g. 1-1-logs.md

## For any consultants or software dev teams using this repo.
Here is the SCC report for this repo after the modules for starter and dspy


```
$ go install github.com/boyter/scc/v3@latest

$ scc .
───────────────────────────────────────────────────────────────────────────────
Language                 Files     Lines   Blanks  Comments     Code Complexity
───────────────────────────────────────────────────────────────────────────────
Markdown                    36      4252      963         0     3289          0
Python                      32      1709      222       325     1162        106
Plain Text                   2        10        0         0       10          0
License                      1        21        4         0       17          0
───────────────────────────────────────────────────────────────────────────────
Total                       71      5992     1189       325     4478        106
───────────────────────────────────────────────────────────────────────────────
Estimated Cost to Develop (organic) $130,386
Estimated Schedule Effort (organic) 6.34 months
Estimated People Required (organic) 1.83

```