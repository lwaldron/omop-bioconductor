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
- delphi-100k (100k persons, CDM 5.4) includes Genomic-CDM tables, but its origin and license are undocumented.
- Genomic-CDM `VARIANT_OCCURRENCE` has no chromosome, start or end: only `rs_id`, transcript `reference_sequence`, `hgvs_c` and `hgvs_p`. `GENOMIC_TEST` has an optional `reference_genome`. Conversion to `VRanges` needs HGVS or rsID resolution against a build.
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
