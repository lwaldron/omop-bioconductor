#!/usr/bin/env python3
"""Survey FAIR Data Points for OMOP and genomic datasets.

Reads the FAIR Data Point Index, crawls each active FDP's catalogues and
datasets as Turtle, and writes one JSON line per dataset with OMOP and
genomic indicators. Standard library only; parsing is regex-based, so it is a
survey tool, not a full RDF client.

Usage:
    python3 -I survey/fdp_survey.py [--max-catalogs 100] [--max-datasets 500] \
        [--include-test] [--workers 12] [--out datasets.jsonl] [--fdps-out fdps.jsonl]
"""
import argparse
import concurrent.futures as cf
import json
import re
import sys
import urllib.request

INDEX_URL = "https://home.fairdatapoint.org/index/entries/all"
OMOP_WIKIDATA = "http://www.wikidata.org/entity/Q125499706"
UA = "fdp-omop-survey"

# "test" also covers "testbed"; broad on purpose for this index.
TEST_HOST = re.compile(r"test|acc\.|staging|dev\.|demo|fdplight|index\.|w3id", re.I)
LINK = re.compile(r"<(https?://[^>\s]+)>")
CATALOG_PRED = (r"(?:r3d:dataCatalog|fdp-o:metadataCatalog|ldp:contains|dcat:catalog|"
                r"<http://www\.re3data\.org/schema/3-0#dataCatalog>|"
                r"<https://w3id\.org/fdp/fdp-o#metadataCatalog>)")
DATASET_PRED = r"(?:dcat:dataset|<http://www\.w3\.org/ns/dcat#dataset>)"
TITLE = re.compile(r'(?:dcterms:title|dct:title|<http://purl\.org/dc/terms/title>)\s+"(?:"")?([^"]+)')
CONFORMS = re.compile(r"(?:dcterms:conformsTo|dct:conformsTo|<http://purl\.org/dc/terms/conformsTo>)"
                      r"\s+((?:<[^>]+>\s*,?\s*)+)")
OMOP_TEXT = re.compile(r"\bOMOP\b", re.I)
NON_OMOP = re.compile(r"non[- ]OMOP", re.I)
GENOMIC = re.compile(r"genom|sequenc|exome|variant|GWAS|SNP\b", re.I)


def get(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"Accept": "text/turtle", "User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read(2_000_000).decode("utf-8", "replace")
    except Exception:
        return ""


def objects(ttl, pred):
    out = []
    for m in re.finditer(pred + r"\s+((?:<[^>]+>\s*,?\s*)+)", ttl):
        out.extend(LINK.findall(m.group(1)))
    return list(dict.fromkeys(out))


def describe(ds_url, ttl, root, catalog):
    title = TITLE.search(ttl)
    conforms = [u for m in CONFORMS.finditer(ttl) for u in LINK.findall(m.group(1))]
    text_hits = len(OMOP_TEXT.findall(ttl)) - len(NON_OMOP.findall(ttl))
    return {
        "fdp": root,
        "catalog": catalog,
        "dataset": ds_url,
        "title": title.group(1).strip()[:200] if title else None,
        "omop_conforms_to": OMOP_WIKIDATA in conforms,
        "omop_text": text_hits > 0,
        "genomic_text": bool(GENOMIC.search(ttl)),
        "conforms_to": conforms,
    }


def survey(root, max_catalogs, max_datasets):
    ttl = get(root)
    if not ttl:
        return {"fdp": root, "reachable": False}, []
    rows = []
    catalogs = objects(ttl, CATALOG_PRED)[:max_catalogs]
    for cat in catalogs:
        for ds in objects(get(cat), DATASET_PRED)[:max_datasets]:
            dttl = get(ds)
            if dttl:
                rows.append(describe(ds, dttl, root, cat))
    return {"fdp": root, "reachable": True, "catalogs": len(catalogs), "datasets": len(rows)}, rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--max-catalogs", type=int, default=100)
    ap.add_argument("--max-datasets", type=int, default=500, help="per catalogue")
    ap.add_argument("--include-test", action="store_true", help="keep test/staging FDPs")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default="datasets.jsonl")
    ap.add_argument("--fdps-out", default="fdps.jsonl")
    a = ap.parse_args()

    req = urllib.request.Request(INDEX_URL, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        entries = json.load(r)
    roots = sorted({e["clientUrl"].rstrip("/") for e in entries
                    if e.get("state") == "ACTIVE" and e.get("clientUrl")})
    if not a.include_test:
        roots = [u for u in roots if not TEST_HOST.search(u)]
    print(f"index: {len(entries)} registrations, {len(roots)} active roots surveyed", file=sys.stderr)

    n_ds = n_omop = n_gen = 0
    with open(a.out, "w") as out, open(a.fdps_out, "w") as fout, \
            cf.ThreadPoolExecutor(a.workers) as ex:
        for summary, rows in ex.map(lambda u: survey(u, a.max_catalogs, a.max_datasets), roots):
            fout.write(json.dumps(summary) + "\n")
            for row in rows:
                out.write(json.dumps(row) + "\n")
                n_ds += 1
                n_omop += row["omop_conforms_to"] or row["omop_text"]
                n_gen += row["genomic_text"]
    print(f"datasets: {n_ds}, OMOP: {n_omop}, genomic: {n_gen}", file=sys.stderr)


if __name__ == "__main__":
    main()
