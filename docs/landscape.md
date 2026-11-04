# Landscape: where OMOP data is described, and what is missing

Observed 2026-11-04 unless stated.

## Real OMOP data: catalogues

| Resource | Content | Access |
|---|---|---|
| [HMA-EMA RWD Catalogue](https://catalogues.ema.europa.eu) | 484 data sources, 3,454 studies, 192 networks. Has a "CDM Mapping: OMOP" filter, export, and a record-completeness score. A full-text search for "OMOP" returned 15 sources | Public browse; the filter could not be driven from a script |
| [EHDEN Portal](https://portal.ehden.eu) | 187 data partners in 29 countries mapping to OMOP | Login |
| OHDSI | Adoption map only (650+ databases). [DbDiagnostics](https://ohdsi.github.io/DbDiagnostics/) builds aggregate profiles for fit-for-purpose checks | No public catalogue |
| EHDS / HealthDCAT-AP | EU metadata standard for health data access bodies' catalogues; Release 5, hosted by the European Commission | Public specification |
| [MIMIC-IV demo in OMOP](https://physionet.org/content/mimic-iv-demo-omop/) | 100 real de-identified patients; ODbL; DOI 10.13026/2d25-8g07 | Open download; the only openly downloadable real OMOP data found |

Not verified: All of Us (OMOP EHR plus genomes, Researcher Workbench), N3C (OMOP, controlled), UK Biobank (OHDSI's Vocabulary-v5.0 contains a `UK_Biobank` vocabulary).

### FAIR Data Points

Many national and project catalogues publish DCAT metadata through [FAIR Data Points](https://www.fairdatapoint.org) (FDPs), listed in the FDP Index (`https://home.fairdatapoint.org/index/entries/all`). Each serves RDF over HTTP with no key, so one client can read them all. Relevant active FDPs: the EHDS pilot (`ehdsfdp.healthdataportal.eu`), Health-RI (NL), Genomic Data Infrastructure nodes (LU, CZ, DE, IE, HR, RO, NL), EGA, EJP-RD, Orphanet, LOVD, SIB Swiss (SPHN), EATRIS, Erasmus MC, Radboudumc, LUMC.

A [survey](../survey/) of 1,776 datasets across them found 13 OMOP datasets, only one of which declares OMOP in a structured way. Wikidata [Q125499706](https://www.wikidata.org/wiki/Q125499706) is the OMOP CDM and can be used as `dct:conformsTo <http://www.wikidata.org/entity/Q125499706>`; there is no per-version identifier.

### Health-RI National Health Data Catalogue (NL)

[catalogus.healthdata.nl](https://catalogus.healthdata.nl) has an open JSON API (`POST https://api.healthdata.nl/discovery/api/v1/datasets/search`, `GET .../filters`) with HealthDCAT-AP-style facets, including coding system, access rights and DPV personal-data categories (Genetic, DNA Code). 703 datasets.

| Exact phrase | Datasets |
|---|---|
| "OMOP", "Common Data Model", "FHIR" | 0 |
| "genome" | 21 |
| "sequencing" | 20 |
| "EGA" | 12 |
| "biobank" | 5 |

The coding-system facet lists SNOMED, LOINC, ATC, ICD-O-3 and DICOM, not OMOP.

### Pattern and gap

Genomic data is becoming findable through these catalogues; OMOP data mostly is not, because publishers do not declare it. No catalogue or DbDiagnostics profile reports whether a database populates the OMOP `specimen` table or Genomic-CDM tables, or links to EGA/dbGaP accessions.

## GA4GH Beacon v2 and GDI: record-level discovery

[Beacon](https://genomebeacons.org) ([API docs](https://docs.genomebeacons.org)) gives yes/no or count answers about variants and, in v2, individuals, biosamples and clinical attributes, with host-controlled access levels. It is a core component of the [European Genomic Data Infrastructure](https://gdi.onemilliongenomes.eu) (GDI, 1+MG), which provides federated access to genomic and related clinical data, and of the ELIXIR Beacon Network.

- ELIXIR Beacon Network aggregator: `https://beacon-network-backend-demo.ega-archive.org/beacon-network/v2.0.0/`. Filtering terms: 1,396, mostly NCIT (1,078), plus ICD10, ICD-O-3, HP, MONDO, SNOMED, LOINC, SO. No OMOP concept IDs.
- OMOP to Beacon: CNAG's [Convert-Pheno](https://github.com/CNAG-Biomedical-Informatics/convert-pheno) (Artistic-2.0) converts OMOP CDM exports to Beacon v2 `individuals`, and between Phenopackets, FHIR, REDCap and openEHR.
- The IMPaCT-Data paper on OMOP CDM 5.4 to Beacon v2 ([doi:10.1186/s12911-026-03649-0](https://doi.org/10.1186/s12911-026-03649-0), [repo](https://github.com/CNAG-Biomedical-Informatics/omop-cdm-2-beacon-v2)) also describes serving Beacon queries directly from a PostgreSQL OMOP database.
- FinnGen participates in GDI, and its October 2025 lab-value GWAS identifies 383 lab measurements by OMOP concept IDs ([browser](https://labvalues.finngen.fi)).
- Bioconductor: [pgxRpi](https://bioconductor.org/packages/pgxRpi) is a Beacon v2 client for Progenetix only; GA4GHclient and GA4GHshiny target older GA4GH APIs. No general Beacon v2 client.

## R software for OMOP

[awesome-OMOP](https://github.com/aryacsoman/awesome-OMOP) (MIT) lists 27 R packages for OMOP analysis, mostly HADES and darwin-eu. Last updated January 2025; several links point to repositories that do not exist under the OHDSI organisation (CohortSurvival, DrugUtilisation, dsOMOP, ROMOP, allofus, PopulationLevelEstimation), and the contributing link is a placeholder. Two entries matter for running Bioconductor code where secured data lives:

- [allofus](https://roux-ohdsi.github.io/allofus/) (CRAN, `roux-ohdsi/allofus`): interface to the All of Us Researcher Workbench, which holds OMOP CDM data in BigQuery. A worked example of the "same code inside the enclave" route.
- [dsOMOP](https://github.com/isglobal-brge/dsOMOP) (`isglobal-brge`, active): OMOP CDM access from DataSHIELD, with server-side disclosure controls (small-cell suppression, count banding). A federated route that never exposes person-level rows.

OHDSI's own catalogue of packages is [HADES](https://ohdsi.github.io/Hades/packages.html); darwin-eu's is at [oxford-pharmacoepi.github.io/Oxinfer](https://oxford-pharmacoepi.github.io/Oxinfer/packages/summary.html).

## Synthetic OMOP data

Used by OHDSI and DARWIN EU training, for example the [Oxford RWE Summer School 2026](https://github.com/oxford-pharmacoepi/RealWorldEvidenceSummerSchool2026).

| Resource | Gives | Gaps |
|---|---|---|
| [omock](https://github.com/OHDSI/omock) `mockDatasets` | Name to URL map, CDM version, counts; `drug_strength` fetched separately | Code Apache-2; datasets have no license, checksum or version; `drug_strength` is hosted on Dropbox |
| Azure `cdmconnectordata.blob.core.windows.net/cdmconnector-example-data/` | GiBleed_5.3, delphi-100k_5.4, ~17 Synthea sets, synpuf-1k_5.4 | No landing page or manifest |
| [EunomiaDatasets](https://github.com/OHDSI/EunomiaDatasets) | GiBleed_5.3 and 5.5, MIMIC, Synthea27Nj; Apache-2.0 | No provenance |
| `s3://ohdsi-sample-data` (OHDSI-in-a-Box) | SynPUF, Synthea, vocabulary sets; publicly listable | No README, license or manifest |
| [OMOP CDM spec](https://ohdsi.github.io/CommonDataModel/) | Field-level dictionary, `CDM_SOURCE` | |
| [Genomic-CDM](https://github.com/OHDSI/Genomic-CDM) v2.0 | Spec for `genomic_test`, `target_gene`, `variant_occurrence`, `variant_annotation` | Prototype; not in core CDM |
| [Athena](https://athena.ohdsi.org) | Standardized Vocabularies browser and download | Licensed vocabularies gated; scripted requests refused |
| [Vocabulary-v5.0](https://github.com/OHDSI/Vocabulary-v5.0) | Build scripts, dated releases, `OMOP Genomic` vocabulary (source CSVs on Google Drive) | Source vocabularies keep their own licenses |
| [OmopSketch](https://ohdsi.github.io/OmopSketch/) | Database characterisation as `summarised_result` | Not published alongside the datasets |

The [Book of OHDSI](https://ohdsi.github.io/TheBookOfOhdsi/OpenScience.html) section 3.7 (built 2021) names these FAIR gaps: no persistent identifiers, licenses uncommon, metadata not automated.
