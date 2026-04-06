```markdown
# ...
```
```json
{
  "next_cell": {
    "row": ...,
    "col": ...,
    "md_file": "...",
    "type": "..."
  }
}
```
```python
import os
os.makedirs("output_md")
with open("output_md/00_paper_title.md", "w") as f:
    f.write("""# Title
## Abstract
...
""")
print(f"Saved paper to output_md/00_paper_title.md")
```

SNS Score: 0.879