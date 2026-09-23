import re
import numpy as np

input_file = "Thor2026_correcciones.mcmc.txt"

# guardar theta, tau y número de especies
theta_means = []
tau_means = []
n_species = []

with open(input_file) as f:
    for line in f:
        line = line.strip()
        if not line or not line.startswith("("):
            continue
        thetas = [float(t) for t in re.findall(r'#([\d\.]+)', line)]
        taus   = [float(t) for t in re.findall(r':\s*([\d\.]+)', line)]
        # el número de especies está al final, después del último ";"
        m = re.search(r';\s*(\d+)\s*$', line)
        nsp = int(m.group(1)) if m else None

        if thetas:
            theta_means.append(np.mean(thetas))
        if taus:
            tau_means.append(np.mean(taus))
        n_species.append(nsp)

theta_means = np.array(theta_means)
tau_means   = np.array(tau_means)
n_species   = np.array(n_species)

def ess_manual(x, max_lag=1000):
    x = np.asarray(x, dtype=float)
    n = len(x)
    x = x - x.mean()
    f = np.fft.fft(x, n=2*n)
    acf = np.fft.ifft(f * np.conjugate(f))[:n].real
    acf /= acf[0]
    cutoff = np.where(acf < 0.05)[0]
    K = cutoff[0] if len(cutoff) > 0 else min(max_lag, n-1)
    s = 1 + 2 * np.sum(acf[1:K+1])
    return n / s

print(f"Muestras totales: {len(tau_means)}")
print(f"ESS θ (global): {ess_manual(theta_means):.1f}")
print(f"ESS τ (global): {ess_manual(tau_means):.1f}")
print()

# ESS de tau separado por número de especies
for k in sorted(set(n_species)):
    mask = n_species == k
    tau_k = tau_means[mask]
    print(f"Configuración con {k} especies: n = {mask.sum()}")
    print(f"  Media τ: {tau_k.mean():.6f}")
    print(f"  ESS τ: {ess_manual(tau_k):.1f}")
