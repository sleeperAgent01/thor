#!/usr/bin/env python3
"""
generate_a11_beta_sweep.py

Genera el barrido de priors para el análisis A11.
Cada beta tiene 3 réplicas con semillas fijas.

Crea:
    A11_beta_sweep/b{XXXX}_rep{N}/cfile.ctl
    a11_beta_sweep_map.txt

Cada subdirectorio contiene enlaces simbólicos a:
    thorSep2026-alig.phy
    thorImap.tsv
    constraints.txt
    heredity.txt
"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))

SHARED_FILES = [
    "thorSep2026-alig.phy",
    "thorImap.tsv",
    "constraints.txt",
    "heredity.txt",
]

# Barrido de betas
BETA_VALUES = [0.001, 0.002, 0.004, 0.006, 0.008, 0.010]

# Semillas base por beta
SEED_BASE = {
    0.001: 701,
    0.002: 711,
    0.004: 721,
    0.006: 731,
    0.008: 741,
    0.010: 751,
}

# Parámetros MCMC finales
BURNIN   = 20000
SAMPFREQ = 2
NSAMPLE  = 2000000

TEMPLATE = """# BPP control file - Thorichthys
# Modelo A11: delimitación + árbol de especies
# Barrido de priors: theta ~ IG(3, {beta}), tau ~ IG(3, {beta})
# Réplica: {rep}

seed = {seed}

seqfile = ./thorSep2026-alig.phy
Imapfile = ./thorImap.tsv
jobname = {jobname}

speciesdelimitation = 1 0 2
speciestree = 1 0
speciesmodelprior = 0

species&tree = 13 helleri affinis maculipinnis passionis maculipinnisPapaloapan socolofi panchovillae helleriCacahuano callolepis aureus meeki Tsalvini ellioti
                     74 39 22 15 12 7 7 6 5 5 3 3 2
                     (Tsalvini,(((passionis,(meeki,affinis)),helleri),(((maculipinnis,socolofi),helleriCacahuano),(((panchovillae,(maculipinnisPapaloapan,ellioti)),callolepis),aureus))));

constraintfile = ./constraints.txt

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
    base_dir = os.path.join(BASE, "A11_beta_sweep")
    os.makedirs(base_dir, exist_ok=True)

    runs = []
    idx = 1

    for beta in BETA_VALUES:
        # 0.001 → 0010, 0.010 → 0100
        beta_tag = f"{int(round(beta * 10000)):04d}"
        for rep in (1, 2, 3):
            seed = SEED_BASE[beta] + (rep - 1)
            run_name = f"b{beta_tag}_rep{rep}"
            jobname  = f"Thor_A11_b{beta_tag}_rep{rep}"
            run_dir  = os.path.join(base_dir, run_name)
            os.makedirs(run_dir, exist_ok=True)

            ctl = TEMPLATE.format(
                beta=beta,
                rep=rep,
                seed=seed,
                jobname=jobname,
                burnin=BURNIN,
                sampfreq=SAMPFREQ,
                nsample=NSAMPLE,
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

            runs.append((idx, f"A11_beta_sweep/{run_name}"))
            print(f"  [{idx:02d}] {run_name}  (beta={beta}, seed={seed})")
            idx += 1

    with open(os.path.join(BASE, "a11_beta_sweep_map.txt"), "w") as f:
        for i, path in runs:
            f.write(f"{i}\t{path}\n")

    print(f"\nTotal: {len(runs)} corridas generadas.")
    print(f"Mapa: a11_beta_sweep_map.txt")


if __name__ == "__main__":
    main()
