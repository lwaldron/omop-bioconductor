# Open questions

Grouped by who can answer. To be filed as GitHub issues, one per group; this file is the index.

## Catalogues and standards (EMA, HealthDCAT-AP, FDP, Health-RI, DbDiagnostics)

1. Does the HMA-EMA catalogue have an API or stable export, and do its records include biospecimen or genetic-data fields?
2. Will HealthDCAT-AP include omics or biospecimen descriptors, and who takes proposals?
3. Will the FDP and HealthDCAT-AP communities endorse `dct:conformsTo wd:Q125499706` for OMOP, with a per-version identifier?
4. Would Health-RI add OMOP to its coding-system or conforms-to facet?
5. Could DbDiagnostics profiles report row counts for `specimen` and the Genomic-CDM tables?
6. Is there a maintained, deduplicated harvest of all FDPs so clients need not crawl 70 servers?

## Genomic-clinical linkage (GDI, FinnGen, EHDEN, DARWIN EU)

7. Which EHDEN and DARWIN EU data partners have linked biobank or omics data?
8. Do GDI FDP nodes link genomic datasets to clinical datasets of the same participants, and in which vocabulary?
9. Does FinnGen, or any GDI node, expose OMOP-structured phenotype tables in its secure environment, and which tables and version?
10. Which databases run inside FinnGen, GDI nodes, All of Us and AnVIL, and does CDMConnector reach each?
11. Can Bioconductor packages be installed in those environments?
12. Does the OMOP `specimen` table, in real biobank-linked databases, carry the sample identifiers used in omics files?

## Beacon (GA4GH, CNAG, pgxRpi)

13. Would a general Bioconductor Beacon v2 client be welcome, and would the pgxRpi and Progenetix team collaborate?
14. Is the IMPaCT-Data on-the-fly OMOP-to-Beacon service released and reusable at other OMOP sites?
15. Could Beacon filtering terms accept OMOP concept IDs, or should OMOP sites map to SNOMED/NCIT as Convert-Pheno does?

## Synthetic datasets (omock, CDMConnector, Eunomia)

16. Could GiBleed, delphi-100k and the Synthea sets get a DOI per version?
17. Are the zips versioned and immutable, and could `omock::mockDatasets` carry checksum, version and landing page?
18. Who controls the Azure and S3 hosting, is there a mirror, and could `drug_strength` move off Dropbox?
19. Can the datasets be read without R (Parquet plus manifest)?
20. What is delphi-100k: source, generator, parameters? Are its Genomic-CDM tables populated, and do they use OMOP Genomic concept IDs?
21. Which vocabulary release does each dataset use, per vocabulary?
22. Could each dataset ship a machine-readable data dictionary, for example an OmopSketch `summarised_result`?
23. What license covers each dataset? GiBleed is Apache-2.0 in EunomiaDatasets; what covers delphi and the Azure copies?

## Vocabularies (Athena, Vocabulary-v5.0, Genomic-CDM)

24. Is there a sanctioned API for programmatic Athena lookups?
25. Could the unrestricted parts of the vocabularies be a versioned AnnotationHub resource?
26. Which identifiers do OMOP Genomic concepts use for genes and variants, and how do they map to `org.Hs.eg.db`, `TxDb`/`EnsDb`?
27. Could the OMOP Genomic source files move from Google Drive to a versioned, citable location?
28. Is there an intended route from Genomic-CDM tables to `VRanges`, and is `reference_genome` populated?

## Bioconductor and OHDSI package communities

29. Would omock maintainers support an ExperimentHub resource wrapping the synthetic datasets?
30. Would darwin-eu/OHDSI package authors consider Bioconductor submission or cross-listing in a workflow?
31. Are there small, stable fixtures a Bioconductor package could depend on in tests?
32. What is the recommended way to link `person_id` data to sample-keyed omics (`MultiAssayExperiment` sample maps), and would a worked example be welcome?

## Training materials (Oxford RWE Summer School)

33. What license covers the slides and code, and could an `renv.lock` or `sessionInfo()` be published with the site?
34. The committed `GiBleed_database_description.json` describes GiBleed as Eunomia stochastic simulation while the database's `cdm_source` names Synthea; which is right, and can the two be reconciled?
