#!/bin/bash -l
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=32g
#SBATCH --tmp=10g
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mgarduos@umn.edu
#SBATCH --job-name=Thor_A00_sweep
#SBATCH --array=1-18

BPP_BIN="/scratch.global/mgarduos/thor/bpp/bin/bpp"
BASE="/scratch.global/mgarduos/thor/datos"

if [ ! -x "${BPP_BIN}" ]; then
    echo "Error: BPP no encontrado o no ejecutable en ${BPP_BIN}"
    exit 1
fi

MAP_FILE="${BASE}/a00_beta_sweep_map.txt"
RUN_DIR=$(awk -v idx=${SLURM_ARRAY_TASK_ID} '$1==idx {print $2}' "${MAP_FILE}")

if [ -z "${RUN_DIR}" ]; then
    echo "Error: no se encontró directorio para índice ${SLURM_ARRAY_TASK_ID}"
    exit 1
fi

cd "${BASE}/${RUN_DIR}"
echo "Corriendo en: $(pwd)"
echo "BPP: ${BPP_BIN}"
echo "Job ID: ${SLURM_JOB_ID}, Array task: ${SLURM_ARRAY_TASK_ID}"
echo "CPUs: ${SLURM_CPUS_PER_TASK}"
echo "Inicio: $(date)"

#Corriendo BPP
${BPP_BIN}  --cfile cfile.ctl > bpp.log 2>&1
EXIT_CODE=$?

echo "Terminado con código: ${EXIT_CODE}"
echo "Fin: $(date)"

if [ ${EXIT_CODE} -ne 0 ]; then
    echo "--- Últimas líneas de bpp.log ---"
    tail -n 30 bpp.log
fi

exit ${EXIT_CODE}
