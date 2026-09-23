#!/usr/bin/env python3
"""
generador_a00_sweep.py

Genera el barrido de priors para A00 sobre el árbol fijo de 12 especies.
Usa thorImap2.tsv (affinismeeki fusionado).
3 réplicas por cada valor de beta.
Sin especificar threads (se controla vía SLURM con --cpus-per-task=2 y --no-pin).
"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))

SHARED_FILES = [
    "thorSep2026-alig.phy",
    "thorImap2.tsv",
    "heredity.txt",
]

BETA_VALUES = [0.001, 0.002, 0.004, 0.006, 0.008, 0.010]

SEED_BASE = {
    0.001: 901,
    0.002: 911,
    0.004: 921,
    0.006: 931,
    0.008: 941,
    0.010: 951,
}

BURNIN   = 20000
SAMPFREQ = 2
NSAMPLE  = 2000000

TEMPLATE = """# BPP control file - Thorichthys
# Modelo A00: inferencia within-model con árbol fijo
# Topología: mejor árbol del análisis A11 (12 especies)
# Barrido de priors: theta ~ IG(3, {beta}), tau ~ IG(3, {beta})
# Réplica: {rep}

seed = {seed}

seqfile = ./thorSep2026-alig.phy
Imapfile = ./thorImap2.tsv
jobname = Thor_A00_b{beta_tag}_rep{rep}

speciesdelimitation = 0
speciestree = 0
speciesmodelprior = 0

species&tree = 12 affinismeeki aureus callolepis ellioti helleri helleriCacahuano maculipinnis maculipinnisPapaloapan panchovillae passionis socolofi Tsalvini
                     42 5 5 2 74 6 22 12 7 15 7 3
                     (Tsalvini, (((affinismeeki, helleri), passionis), ((aureus, ((callolepis, (ellioti, maculipinnisPapaloapan)), panchovillae)), (helleriCacahuano, (maculipinnis, socolofi)))));

usedata = 1
nloci = 1
cleandata = 0

thetaprior = invgamma 3 {beta} e
tauprior   = invgamma 3 {beta}

finetune = 1

heredity = 2 ./heredity.txt
scaling = 1

model = TN93

print = 1 0 0 0 0

burnin = {burnin}
sampfreq = {sampfreq}
nsample = {nsample}
"""


def main():
    base_dir = os.path.join(BASE, "A00_beta_sweep")
    os.makedirs(base_dir, exist_ok=True)

    runs = []
    idx = 1

    for beta in BETA_VALUES:
        beta_tag = f"{int(round(beta * 10000)):04d}"
        for rep in (1, 2, 3):
            seed = SEED_BASE[beta] + (rep - 1)
            run_name = f"b{beta_tag}_rep{rep}"
            run_dir  = os.path.join(base_dir, run_name)
            os.makedirs(run_dir, exist_ok=True)

            ctl = TEMPLATE.format(
                beta=beta, beta_tag=beta_tag, rep=rep, seed=seed,
                burnin=BURNIN, sampfreq=SAMPFREQ, nsample=NSAMPLE,
            )

            with open(os.path.join(run_dir, "cfile.ctl"), "w") as f:
                f.write(ctl)

            for fname in SHARED_FILES:
                src = os.path.join(BASE, fname)
                dst = os.path.join(run_dir, fname)
                if not os.path.exists(src):
                    print(f"  ADVERTENCIA: no existe {src}")
                    continue
                if not os.path.exists(dst):
                    os.symlink(src, dst)

            runs.append((idx, f"A00_beta_sweep/{run_name}"))
            print(f"  [{idx:02d}] {run_name}  (beta={beta}, seed={seed})")
            idx += 1

    with open(os.path.join(BASE, "a00_beta_sweep_map.txt"), "w") as f:
        for i, path in runs:
            f.write(f"{i}\t{path}\n")

    print(f"\nTotal: {len(runs)} corridas generadas.")


if __name__ == "__main__":
    main()
