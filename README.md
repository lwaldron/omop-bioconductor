# omop-bioconductor

Draft project: make OMOP CDM health data findable and accessible to Bioconductor users, and make Bioconductor analysis usable on OMOP data, synthetic or secured.

## Problem

- Bioconductor has no OMOP or OHDSI packages.
- Real OMOP databases stay with their custodians and can only be found through catalogues, and no catalogue records what an omics researcher searches on: linked biospecimens or omics, their types and counts, and where they are deposited.
- The synthetic OMOP datasets used for training have no DOIs, landing pages, checksums or, mostly, license and provenance statements.

## Proposed discovery chain

1. **Catalogues** (FAIR Data Points, HealthDCAT-AP, HMA-EMA catalogue): which datasets exist, who holds them, how to apply.
2. **GA4GH Beacon v2**: does a dataset contain my variant or phenotype, and for how many people, before access.
3. **Access request** to the custodian (out of scope here).
4. **One R package** that loads OMOP data as `SummarizedExperiment` / `MultiAssayExperiment` from a CDMConnector connection, so the same code runs on synthetic data and, after access, inside a secure environment.

## Work

| Item | Status | Where |
|---|---|---|
| Survey of FAIR Data Points for OMOP and genomic datasets | done | [survey/](survey/) |
| Landscape of catalogues, Beacon and synthetic data | draft | [docs/landscape.md](docs/landscape.md) |
| Design of the OMOP to Bioconductor package | draft | [docs/package-design.md](docs/package-design.md) |
| Open questions for maintainers and standards bodies | draft, to be filed as issues | [docs/questions.md](docs/questions.md) |
| Catalogue client, Beacon client, ExperimentHub resources | idea | [docs/package-design.md](docs/package-design.md#related-ideas) |

## License

MIT.
