# BPP analyses for *Thorichthys* species delimitation

This repository contains the BPP control files, scripts, and configuration
used for species delimitation and species-tree inference in the
*Thorichthys* dataset.

## Software

- **BPP v4.8.7** (`bpp v4.8.7_linux_x86_64`)
  Source: https://github.com/bpp/bpp
  Binary used: `bpp/bin/bpp`

All analyses were run on the Minnesota Supercomputing Institute (MSI)
cluster using SLURM. Each job used 2 CPUs (`--cpus-per-task=2`) and
32 GB of RAM, and was invoked with the `--no-pin` flag to avoid thread
pinning errors.

## Input data

| File | Description |
|---|---|
| `thorSep2026-alig.phy` | PHYLIP alignment of the mt-Cytb locus, one sequence per individual. |
| `thorImap.tsv` | Individual-to-species assignment for the A11 analyses (13 candidate lineages, including `affinis` and `meeki` as separate species). |
| `thorImap2.tsv` | Individual-to-species assignment for the A00 analyses (12 lineages, with `affinismeeki` already collapsed). |
| `heredity.txt` | Contains a single value, `0.25`, the mitochondrial inheritance scalar for a diploid organism. |
| `constraints.txt` | Topological constraint file specifying the outgroup for rooting (`outgroup Tsalvini`). |

## Model configuration

All BPP analyses used the following configuration:

- **Substitution model:** TN93 (`model = TN93`).
- **Inheritance scalar:** fixed at 0.25 (`heredity = 2 ./heredity.txt`).
- **Priors:** inverse-gamma on both θ and τ, with α = 3 and β varying
  across the sweep (see below).
- **MCMC:** 2,000,000 samples, burn-in of 20,000 generations, sampling
  interval of 2 generations (4,020,000 generations total per chain).

## Analysis schemes

### A11 — Joint species delimitation and species-tree inference

Directory: `A11_beta_sweep/`

Prior sweep: β ∈ {0.001, 0.002, 0.004, 0.006, 0.008, 0.010}.
For each β, three independent chains were run with fixed, distinct seeds
(901–953). Total: 18 runs.

Control file template:
`generate_bpp_inputs_extra.py` (with `speciesdelimitation = 1 0 2`
and `speciestree = 1 0`).

Each run directory contains:
- `cfile.ctl` — BPP control file.
- `bpp.log` — SLURM/BPP stdout.
- `Thor_A11_b*.mcmc.txt` — sampled species trees (one per line, Newick).
- `Thor_A11_b*.txt` — BPP output with delimitation probabilities.

### A00 — Within-model parameter estimation on a fixed tree

Directory: `A00_beta_sweep/`

The species tree was fixed to the topology inferred by A11 (12 lineages,
with `affinismeeki` collapsed). Same prior sweep as A11
(β ∈ {0.001, 0.002, 0.004, 0.006, 0.008, 0.010}, three chains each).
Total: 18 runs.

Control file template:
`generador_a00_sweep.py` (with `speciesdelimitation = 0` and
`speciestree = 0`).

Each run directory contains:
- `cfile.ctl`
- `bpp.log`
- `Thor_A00_b*.out` — BPP summary table with ESS, Eff, and rho1 for
  every θ and τ parameter.

### A01 / A10 — Exploratory analyses

Directory: `A01_runs/`, `A10_runs/`

A01 (`speciesdelimitation = 0`, `speciestree = 1 1`) and
A10 (`speciesdelimitation = 1 1 2 0.5`, `speciestree = 0`) were run
with three chains each for β = 0.12 as exploratory analyses. These
results are reported in the Supplementary Material and are not the
basis for the delimitation presented in the main text.

## Running the analyses

### On a SLURM cluster

```bash
cd /path/to/datos
python3 generate_bpp_inputs_extra.py   # generates A11 control files
python3 generador_a00_sweep.py         # generates A00 control files
sbatch bash/Thor_A11.sh
sbatch bash/Thor_A00_sweep.sh
