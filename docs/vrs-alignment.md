# Aligning OMOP and Bioconductor with GA4GH VRS and Cat-VRS

Assessed 2026-11-04 against VRS 2.1.1 and Cat-VRS 1.1.1 (both released 2026-10-01).

## The standards

- **VRS** describes specific variation. An `Allele` is a `SequenceLocation` (a `SequenceReference` plus start and end) with a sequence expression, and has a computed identifier (`ga4gh:VA.<digest>`) derived from the normalised content. Other classes: `CopyNumberCount`, `CopyNumberChange`, `Adjacency`, `CisPhasedBlock`, and `Expression` for HGVS or SPDI strings.
- **Cat-VRS** describes categories of variation. A `CategoricalVariant` is a set of constraints, carries `mappings` to external codes and `members` that are VRS objects. Trial-use constraints: `DefiningAlleleConstraint`, `DefiningLocationConstraint`, `CopyCountConstraint`. Draft: `CopyChangeConstraint`, `FeatureContextConstraint`, `FunctionConstraint`, `AdjacencyConstraint`.

## What is consistent today

| Cat-VRS / VRS element | OMOP | Bioconductor |
|---|---|---|
| `Allele` (location plus ref/alt on a build) | OMOP Genomic DNA-variant concept names embed GRCh38 chromosome, position and alleles; Genomic-CDM `variant_occurrence` has `reference_allele`, `alternate_allele`, `rs_id` | `VRanges` and `VCF` (VariantAnnotation) hold these fields with a `Seqinfo` genome build |
| `Expression` (HGVS) | OMOP Genomic synonyms are HGVS at RefSeq and Ensembl transcript and protein level; Genomic-CDM `hgvs_c`, `hgvs_p` | No native HGVS parser; derivable from `predictCoding` |
| `DefiningAlleleConstraint` | OMOP Genomic Gene DNA, RNA and Protein Variant classes, linked by `Transcribes to` and `Translates to` | Allele equality on `VRanges` |
| `DefiningLocationConstraint` | Loosely, OMOP Genomic Gene Variant | `GRanges` overlap |
| `FeatureContextConstraint` | OMOP Genomic Gene Variant; Genomic-CDM `target_gene` with HGNC IDs | Gene models from `TxDb` and `EnsDb` |
| `CopyCountConstraint`, `CopyChangeConstraint` | Genomic-CDM `copy_number`, `cnv_locus`; OMOP Genomic Structural Variant concepts (free-text karyotype strings) | `GRanges` with copy-number metadata |
| `FunctionConstraint` | Genomic-CDM `variant_feature` (free text) | `predictCoding` consequence classes |
| Computed identifiers `ga4gh:VA.` | None in OMOP | AnVILVRS (Bioconductor, Marcel Ramos) computes VRS IDs from VCF through the Python `vrs_anvil_toolkit` via reticulate |

OMOP Genomic is a categorical variant vocabulary, so a Cat-VRS use case; Genomic-CDM `variant_occurrence` rows are VRS `Allele` instances; `VRanges` is the Bioconductor form of both.

## What is missing

1. No VRS identifiers in OMOP. Concept codes are `OMOPnnnnnnn`; Genomic-CDM carries rsIDs and HGVS. No join key.
2. No `SequenceReference`. VRS locations are on refget accessions (`ga4gh:SQ.`); OMOP gives the build name only.
3. Coordinates embedded in text. OMOP Genomic positions live in `concept_name`; Genomic-CDM `variant_occurrence` has no chromosome, start or end columns.
4. No Cat-VRS `mappings` to OMOP Genomic codes, and no OMOP `Maps to` toward VRS or ClinVar/CIViC categorical identifiers.
5. No native VRS or Cat-VRS implementation in R. Normalisation and the `sha512t24u` digest exist only in Python; Cat-VRS membership tests exist nowhere in R.
6. OHDSI awareness is thin: OncologyWG issue #350 (2021, closed) on liftover is the only trace; Vocabulary-v5.0 does not mention GA4GH.

## What compatibility requires

OMOP side (Vocabulary and Genomic-CDM workgroups):

- Compute VRS `Allele` identifiers for every OMOP Genomic DNA variant from its GRCh38 position and alleles; store as `concept_synonym` rows (synonym vocabulary "GA4GH VRS") or a crosswalk table.
- Add structured location columns, or a VRS ID column, to Genomic-CDM `variant_occurrence`, with normalisation at ETL. rsID-only rows (as in delphi-100k) need dbSNP resolution.
- Publish a mapping from OMOP Genomic concept classes to Cat-VRS constraint types: Gene DNA/Protein Variant to `DefiningAlleleConstraint`, Gene Variant to `FeatureContextConstraint`, Structural Variant to `CopyCountConstraint` or `AdjacencyConstraint` where parseable.

Bioconductor side:

- A native R VRS implementation: `VRanges` to normalised `Allele` to computed identifier, with refget accessions from `Seqinfo`. AnVILVRS is the starting point; dropping reticulate removes a Python dependency that secure environments dislike.
- A Cat-VRS representation and matcher: constraints as S4 objects; membership from `GRanges` overlap, allele equality and `predictCoding` consequences.
- The OMOP package then tags `VRanges` rows with OMOP Genomic concept IDs and VRS IDs together, which is the join between an OMOP cohort and an omics assay.

Standards side: VRS 2.1.1 is stable; Cat-VRS has three trial-use constraint types. Build to those first.
