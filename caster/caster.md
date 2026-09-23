# Species tree inference with CASTER-site — *Thorichthys* ddRADseq

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the reproducible workflow for inferring the species tree of the genus *Thorichthys* (and closely related *Mesoheros* and *Trichromis*) using **CASTER-site**, a site-based coalescent method implemented in the ASTER package. The analysis replaces a previous ASTRAL-based approach that was found to be numerically inconsistent (see *Background* below).

Este repositorio contiene el flujo de trabajo reproducible para inferir el árbol de especies del género *Thorichthys* (y los géneros cercanos *Mesoheros* y *Trichromis*) usando **CASTER-site**, un método de coalescencia basado en sitios implementado en el paquete ASTER. El análisis reemplaza un enfoque previo basado en ASTRAL que presentaba inconsistencias numéricas (ver *Antecedentes* abajo).

---

## 📋 Background / Antecedentes

**EN:** The original analysis used ASTRAL on 100 subsets of SNPs derived from short ddRAD loci. A reviewer correctly pointed out that the description was numerically inconsistent (100 non-overlapping subsets of 10% each cannot be drawn from 262,255 SNPs) and that the assumption of independent gene trees was questionable for short loci. We therefore replaced the ASTRAL analysis entirely with CASTER-site, which operates directly on the concatenated alignment of loci, models evolution site-by-site under the multispecies coalescent, and is statistically consistent even in the presence of linked sites.

**ES:** El análisis original usaba ASTRAL sobre 100 subconjuntos de SNPs derivados de loci ddRAD cortos. Un revisor señaló correctamente que la descripción era numéricamente inconsistente (no se pueden generar 100 subconjuntos no solapados del 10% a partir de 262,255 SNPs) y que la suposición de árboles de genes independientes era cuestionable para loci cortos. Por ello, reemplazamos completamente el análisis de ASTRAL por CASTER-site, que opera directamente sobre el alineamiento concatenado de loci, modela la evolución sitio por sitio bajo el modelo de coalescencia multiespecie y es estadísticamente consistente incluso en presencia de sitios ligados.

---

## 🧬 Dataset / Conjunto de datos

| Item / Elemento | Value / Valor |
|---|---|
| Marker type / Tipo de marcador | ddRADseq (pairddrad) |
| Samples / Muestras | 28 |
| Assembly software / Software de ensamblaje | ipyrad v0.9.108 |
| Assembly mode / Modo de ensamblaje | *de novo* |
| Loci recovered / Loci recuperados | 28,559 |
| Alignment length / Longitud del alineamiento | 4,411,424 bp |
| Taxa / Taxones | *Thorichthys* (7 spp.), *Trichromis salvini*, *Mesoheros* (3 spp.) |

---

## 🛠️ Software requirements / Requisitos de software

| Software | Version | Purpose / Propósito |
|---|---|---|
| [ipyrad](https://ipyrad.readthedocs.io/) | 0.9.108 | *de novo* assembly of ddRAD loci |
| [ASTER](https://github.com/chaoszhang/ASTER) (`caster-site`) | 1.25.2.6 | Species tree inference |
| R | ≥ 4.0 | Tree visualization |

**Install ASTER via conda / Instalar ASTER vía conda:**
```bash
conda create -n aster -c conda-forge -c bioconda aster
conda activate aster
caster-site --version   # should print 1.25.2.6 or later
```
**command used:**
```bash
caster-site \
    -t 8 \
    -i thor_ddrad-2026.phy \
    -f phylip \
    -o Thor-caster.nwk \
    -R \
    -a hapmap.tsv \
    --root M_atromaculatus \
    2> caster.log
```
