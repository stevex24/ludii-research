import csv,statistics,collections,pathlib
p=pathlib.Path(__file__).resolve().parent
rows=list(csv.DictReader((p/"research_candidates.csv").open(newline="")))
def number(s):
 try: return float(str(s).replace(",",".")) if str(s).strip() else None
 except ValueError: return None
ratings=[number(r["rating"]) for r in rows]
counts=[number(r["users_rated"]) for r in rows]
valid=[(a,b) for a,b in zip(ratings,counts) if a is not None and b is not None]
by_path=collections.defaultdict(list)
by_id=collections.defaultdict(list)
for r in rows:
 by_path[r["ludii_path"]].append(r)
 by_id[r["bgg_id"]].append(r)
duplicate_paths={k:v for k,v in by_path.items() if len(v)>1}
duplicate_ids={k:v for k,v in by_id.items() if len(v)>1}
def family(r):
 parts=pathlib.PurePosixPath(r["ludii_path"]).parts
 return parts[1] if len(parts)>1 else "unknown"
families=collections.Counter(family(r) for r in rows)
lines=["# Day 6 Task 5: Statistical Suitability Audit","",f"Candidate pairs: {len(rows)}",f"Distinct Ludii paths: {len(by_path)}",f"Distinct BGG IDs: {len(by_id)}",f"Complete numeric rating/count pairs: {len(valid)}",f"Missing or invalid ratings: {sum(x is None for x in ratings)}",f"Missing or invalid rating counts: {sum(x is None for x in counts)}",""]
if valid:
 a=[x for x,y in valid]; b=[y for x,y in valid]
 lines+=["## Rating distribution",f"Minimum: {min(a):.3f}",f"Median: {statistics.median(a):.3f}",f"Mean: {statistics.mean(a):.3f}",f"Maximum: {max(a):.3f}","", "## Number of user ratings",f"Minimum: {min(b):.0f}",f"Median: {statistics.median(b):.0f}",f"Maximum: {max(b):.0f}"]
 for threshold in (10,30,100,300,1000,10000):
  lines.append(f"Pairs with at least {threshold} user ratings: {sum(x>=threshold for x in b)}")
lines+=["","## Duplicate Ludii mappings",f"Paths with multiple candidate rows: {len(duplicate_paths)}"]
for k,v in sorted(duplicate_paths.items()):
 lines.append(f"- {k}: "+", ".join(r["bgg_id"] for r in v))
lines+=["","## Duplicate BGG mappings",f"BGG IDs mapped to multiple Ludii paths: {len(duplicate_ids)}"]
for k,v in sorted(duplicate_ids.items()):
 lines.append(f"- {k}: "+", ".join(r["ludii_path"] for r in v))
lines+=["","## Ludii top-level categories (candidate pairs)"]
for k,v in families.most_common(): lines.append(f"- {k}: {v}")
lines+=["","## Leakage and eligibility warnings","- Multiple BGG entries for one Ludii game must stay in the same evaluation group.","- Different variants or related games may share a family even when filenames differ.","- Ludii directory categories are only a preliminary grouping, not verified game families.","- Ratings are historical BGG user averages, not direct measurements of fun.","- No candidate has completed rules verification; training-eligible pairs: 0.","- Do not fit predictive models or claim validation performance from this dataset yet."]
report=chr(10).join(lines)+chr(10)
(p/"TASK5_AUDIT.md").write_text(report)
print(report)
