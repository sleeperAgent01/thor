#!/bin/bash -l
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=32g
#SBATCH --tmp=10g
#SBATCH --mail-type=ALL
#SBATCH --mail-user=mgarduos@umn.edu
#SBATCH --job-name=Thor_A00
#SBATCH --array=1-2

# --- AJUSTA ESTAS DOS RUTAS ---
BPP_BIN="/scratch.global/mgarduos/thor/bpp/bin/bpp"
BASE="/scratch.global/mgarduos/thor/datos"
# ------------------------------

MAP_FILE="${BASE}/a00_array_map.txt"

RUN_DIR=$(awk -v idx=${SLURM_ARRAY_TASK_ID} '$1==idx {print $2}' ${MAP_FILE})

if [ -z "${RUN_DIR}" ]; then
    echo "Error: no se encontró directorio para índice ${SLURM_ARRAY_TASK_ID}"
    exit 1
fi

cd ${BASE}/${RUN_DIR}
echo "Corriendo en: $(pwd)"
echo "Job ID: ${SLURM_JOB_ID}, Array task: ${SLURM_ARRAY_TASK_ID}"
echo "Inicio: $(date)"

${BPP_BIN} --cfile cfile.ctl > bpp.log 2>&1
EXIT_CODE=$?

echo "Terminado con código: ${EXIT_CODE}"
echo "Fin: $(date)"
exit ${EXIT_CODE}
