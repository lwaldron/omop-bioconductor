# Package design: OMOP to Bioconductor, synthetic to secured

Goal: a Bioconductor package that loads OMOP data as Bioconductor structures, documents basic analysis, and runs unchanged on secured data once access is granted.

## Principles

- **Input is a CDMConnector `cdm_reference`, not a file.** The same code runs on DuckDB synthetic data (omock, or an ExperimentHub copy), the MIMIC-IV demo, and Postgres, SQL Server, Databricks or Snowflake inside an enclave. Only the `DBI` connection changes.
- **Compute in the database** (dbplyr); pull only what is needed into R.
- **Enclave constraints:** CRAN and Bioconductor dependencies only, small footprint, no internet at run time.
- **Execution routes to support:** direct `DBI` connection inside an enclave (All of Us via `allofus` and BigQuery; FinnGen sandbox; GDI nodes); DataSHIELD via `dsOMOP`, where only server-reviewed aggregates return to the client.

## Outputs

- `SummarizedExperiment`: features (concepts, cohorts, measurements) by persons. `colData` from `person`, `observation_period` and PatientProfiles demographics; `rowData` from vocabulary tables. Sparse `Matrix` or `DelayedArray` for size.
- `MultiAssayExperiment`: OMOP `specimen` rows as the `sampleMap` linking `person_id` to sample-keyed omics; Genomic-CDM variants as `VRanges` where a reference build is known.
- Results leaving an enclave: aggregate `omopgenerics` summarised results with minimum cell counts.

## Data constraints

- GiBleed (2,694 persons, CDM 5.3, Synthea-derived, Apache-2.0) can be redistributed: its `concept` table has 444 concepts from RxNorm, SNOMED, LOINC, CVX, ICD10CM and NDC, none from licensed vocabularies.
- delphi-100k (99,523 persons, CDM 5.4) has populated, simulated Genomic-CDM tables: 70 SNPs by rsID on GRCh37, one specimen per person, HGNC gene IDs, GWAS-style annotations. CDMConnector already attaches these tables to the `cdm_reference`. Provenance is documented in `cdm_source`; the dataset license is not stated.
- Genomic-CDM `VARIANT_OCCURRENCE` has no chromosome, start or end: only `rs_id`, `reference_sequence`, `hgvs_c` and `hgvs_p`. In delphi only `rs_id` and alleles are filled. Conversion to `VRanges` needs rsID resolution against the build named in `GENOMIC_TEST.reference_genome` (for example via `SNPlocs.Hsapiens.dbSNP155.GRCh37`).
- `specimen` is the join between `person_id` and genomic rows, so it is the natural `MultiAssayExperiment` sample map.
- Vocabulary lookups come from the CDM's own vocabulary tables or a user-supplied Athena download; the package ships no vocabulary files (#9). OMOP Genomic concepts carry HGVS synonyms (RefSeq and Ensembl) and GRCh38 positions in their names, but no rsIDs, ClinVar or HGNC IDs, so those are the join keys.
- `VOCABULARY.vocabulary_version` carries per-vocabulary versions; published dataset metadata usually gives only the overall string.

## Documentation and tests

- Vignettes run on synthetic data (GiBleed) and on the MIMIC-IV OMOP demo for real data.
- A "secured data" vignette shows only the connection swap and the export step.
- Tests on omock mock CDMs and GiBleed.
- First real target: FinnGen through GDI, which has genomes plus OMOP-coded phenotypes discoverable before access.

## Scope risk

Bioconductor reviewers may question scope for EHR-only data. Genomic-CDM and `MultiAssayExperiment` linkage make the case; submit the ExperimentHub resource and the package together.

## Related ideas

- Catalogue client: read the FDP Index, harvest DCAT from each active FDP, add the Health-RI API and EMA export, return a `DataFrame` of datasets with publisher, access rights, OMOP conformance, omics indicators and links.
- General Beacon v2 client (generalising pgxRpi): `g_variants` to `GRanges`/`VRanges`, `individuals` to `DataFrame`.
- ExperimentHub resources for GiBleed and other redistributable synthetic sets.
