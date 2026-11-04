# FDP survey

Survey of FAIR Data Points (FDPs) for datasets that declare OMOP CDM conformance or mention genomic data. A starting point for a Bioconductor catalogue client.

```sh
python3 -I survey/fdp_survey.py --workers 16
```

Run from the repo root. Writes `datasets.jsonl` (one line per dataset) and `fdps.jsonl` (one line per FDP), both gitignored. Standard library only, about 4 minutes.

## What it does

1. Reads the FDP Index at `https://home.fairdatapoint.org/index/entries/all`.
2. Keeps `ACTIVE` entries and drops hosts that look like test, staging or demo servers (`--include-test` keeps them).
3. Fetches each FDP root, its catalogues and their datasets as Turtle (caps: `--max-catalogs 100`, `--max-datasets 500` per catalogue).
4. Flags each dataset:
   - `omop_conforms_to`: `dct:conformsTo <http://www.wikidata.org/entity/Q125499706>` (Wikidata item for the OMOP CDM)
   - `omop_text`: "OMOP" anywhere in the record, minus "non-OMOP"
   - `genomic_text`: the record contains `genom`, `sequenc`, `exome`, `variant`, `GWAS` or `SNP`

## Limitations

- Regex over Turtle, not an RDF parser. `title` is the first `dct:title` in the response, which is sometimes a nested resource (for example a coding system) rather than the dataset.
- Text flags are noisy: `sequenc` matches "consequence" and `variant` matches viral variants. Check hits by hand.
- Responses are truncated at 2 MB, so a very large catalogue listing loses datasets. `fdp.lovd.nl` hits the 500-dataset cap.
- FDPs that page their catalogues, or use predicates other than those in `CATALOG_PRED` and `DATASET_PRED`, are under-counted.
- Network errors are swallowed; a dataset that times out is skipped.

## Results, 2026-11-04

233 index registrations (71 active, 77 unreachable, 57 inactive, 27 invalid), 49 active production roots, 1,776 datasets read. 13 flagged OMOP, 95 genomic.

Only one OMOP record (IIS La Fe, OmicSpace project) uses the Wikidata `conformsTo`; the rest say OMOP in titles or descriptions. Most OMOP hits are UK NHS datasets in the EHDS pilot FDP (`ehdsfdp.healthdataportal.eu`): Leeds Teaching Hospitals, Lancashire Teaching Hospitals, Cheshire and Merseyside primary care, and four COVID datasets. Others: Monasterio HAI pilot and SPHN's Infection Radar (Bern, OMOP CDM 5.4). Two hits titled "Analytics" are unverified.

Context: `docs/landscape.md`.
