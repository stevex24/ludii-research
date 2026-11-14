import csv
from pathlib import Path
from collections import Counter
p=Path(__file__).resolve().parent
with (p/"identity_verification.csv").open(newline="") as f:
 reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
required={"ludii_path","ludii_title","bgg_id","bgg_title","rating","users_rated","verification_status"}
assert required.issubset(fields), "Missing required columns"
assert len(rows)==134, "Unexpected input row count"
assert all(r["verification_status"] in {"mismatch","strong_candidate","variant_review","unresolved"} for r in rows)
kept=[]
for r in rows:
 if r["verification_status"]=="mismatch": continue
 r["training_eligible"]="no"
 r["training_exclusion_reason"]={"strong_candidate":"rules_not_fully_verified","variant_review":"edition_or_variant_unresolved","unresolved":"identity_unresolved"}[r["verification_status"]]
 r["label_source"]="historical_BGG_snapshot"
 r["rating_type"]="BGG_user_average_not_direct_fun"
 kept.append(r)
fields=fields+["training_eligible","training_exclusion_reason","label_source","rating_type"]
with (p/"research_candidates.csv").open("w",newline="") as f:
 w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(kept)
c=Counter(r["verification_status"] for r in rows)
report=f"Day 6 Task 4 Audit\nSource pairs: {len(rows)}\nExcluded mismatches: {c['mismatch']}\nRetained candidates: {len(kept)}\nStrong candidates: {c['strong_candidate']}\nVariant review: {c['variant_review']}\nUnresolved: {c['unresolved']}\nDistinct Ludii paths: {len(set(r['ludii_path'] for r in kept))}\nDistinct BGG IDs: {len(set(r['bgg_id'] for r in kept))}\nTraining eligible: 0\n"
(p/"TASK4_AUDIT.md").write_text(report)
print(report)
