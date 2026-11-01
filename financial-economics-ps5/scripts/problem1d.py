#!/usr/bin/env python3
"""Financial Economics PS5 Problem 1(d); same seven cells as notebooks/problem1d.ipynb."""

def main():
    # Cell 1: imports, annual calibration, and reproducibility settings.
    import json
    import platform
    from pathlib import Path
    import zipfile
    import numpy as np
    import pandas as pd

    T = 100_000
    SEED = 42
    sigma = 0.036
    mu = 0.018
    gamma = 10.0
    beta = 0.99
    SAVE_PATHS = False  # True also exports all 100,000 simulated observations.
    def find_project_root():
        # Scripts know their own location; notebooks may start in notebooks/.
        if "__file__" in globals():
            script = Path(__file__).resolve()
            if script.parent.name == "scripts":
                return script.parent.parent
        current = Path.cwd().resolve()
        for candidate in (current, *current.parents):
            if (
                (candidate / "notebooks").is_dir()
                and (candidate / "scripts").is_dir()
                and (candidate / "requirements.txt").is_file()
            ):
                return candidate
        # Standalone Colab: use its current runtime directory.
        return current

    PROJECT_ROOT = find_project_root()
    OUT_DIR = PROJECT_ROOT / "results" / "problem1d"

    assert T >= 3 and sigma > 0 and gamma > 0 and 0 < beta < 1
    print(f"Python {platform.python_version()}; NumPy {np.__version__}; pandas {pd.__version__}")
    print(f"Annual observations: {T:,}; seed: {SEED}")


    # Cell 2: ONE vector of shocks drives all four log series.
    rng = np.random.Generator(np.random.PCG64(SEED))
    epsilon = rng.standard_normal(T)

    r_f_value = -np.log(beta) + gamma * mu - 0.5 * gamma**2 * sigma**2
    delta_c = mu + sigma * epsilon
    m = np.log(beta) - gamma * delta_c
    r_d = (
        -np.log(beta) + gamma * mu
        - 0.5 * (1 - gamma)**2 * sigma**2
        + sigma * epsilon
    )
    r_f = np.full(T, r_f_value)

    data = pd.DataFrame({"r_f": r_f, "delta_c": delta_c, "m": m, "r_d": r_d})
    assert np.isfinite(data.to_numpy()).all()
    print(data.head().to_string(index=False, float_format=lambda x: f"{x:.8f}"))


    # Cell 3: explicit sample statistics, with a constant-series check.
    def sample_std(x):
        x = np.asarray(x, dtype=float)
        if np.all(x == x[0]):
            return 0.0
        return float(np.std(x, ddof=1))

    def acf1(x):
        x = np.asarray(x, dtype=float)
        if np.all(x == x[0]):
            return np.nan  # Correlation is undefined for a constant series.
        z = x - np.mean(x)
        return float(np.dot(z[1:], z[:-1]) / np.dot(z, z))

    def sample_corr(x, y):
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)
        if np.all(x == x[0]) or np.all(y == y[0]):
            return np.nan
        return float(np.corrcoef(x, y)[0, 1])

    print("Sample SD uses ddof=1; ACF uses the full-sample mean.")
    print("Constant series: SD = 0, ACF = N/A.")


    # Cell 4: population benchmarks derived by hand.
    theory = {
        "r_f": (r_f_value, 0.0, np.nan),
        "delta_c": (mu, sigma, 0.0),
        "m": (np.log(beta) - gamma * mu, gamma * sigma, 0.0),
        "r_d": (
            -np.log(beta) + gamma * mu - 0.5 * (1 - gamma)**2 * sigma**2,
            sigma, 0.0,
        ),
    }

    rows = []
    for name in data.columns:
        x = data[name].to_numpy()
        mean_theory, sd_theory, acf_theory = theory[name]
        rows.append({
            "series": name,
            "sample_mean": float(np.mean(x)),
            "theory_mean": mean_theory,
            "sample_std": sample_std(x),
            "theory_std": sd_theory,
            "sample_acf1": acf1(x),
            "theory_acf1": acf_theory,
        })
    summary = pd.DataFrame(rows)
    print(summary.to_string(index=False, float_format=lambda x: f"{x:.8f}", na_rep="N/A"))


    # Cell 5: the required contemporaneous correlation, plus optional checks.
    corr_c_equity = sample_corr(delta_c, r_d)
    correlations = pd.DataFrame(np.nan, index=data.columns, columns=data.columns)
    for name_x in data.columns:
        for name_y in data.columns:
            correlations.loc[name_x, name_y] = sample_corr(data[name_x], data[name_y])
    print(f"Corr(log consumption growth, log equity return) = {corr_c_equity:.8f}")
    print(correlations.to_string(float_format=lambda x: f"{x:.8f}", na_rep="N/A"))


    # Cell 6: check pricing identities and distinguish simulation error from bugs.
    log_q = np.log(beta) + (1 - gamma) * mu + 0.5 * (1 - gamma)**2 * sigma**2
    assert log_q < 0, "The fundamental price-dividend ratio requires q < 1."
    assert np.allclose(r_d, delta_c - log_q, rtol=0, atol=1e-12)
    assert np.isclose(corr_c_equity, 1.0, rtol=0, atol=1e-12)
    assert np.isclose(sample_std(m), gamma * sample_std(delta_c), rtol=0, atol=1e-12)
    assert np.isclose(sample_std(r_d), sample_std(delta_c), rtol=0, atol=1e-12)
    assert np.isnan(acf1(r_f))

    euler_rows = []
    for label, log_gross_return in [("riskfree", r_f), ("equity", r_d)]:
        pricing_product = np.exp(m + log_gross_return)
        estimate = float(np.mean(pricing_product))
        mc_se = sample_std(pricing_product) / np.sqrt(T)
        euler_rows.append({
            "asset": label,
            "sample_mean_M_times_gross_return": estimate,
            "population_value": 1.0,
            "monte_carlo_standard_error": mc_se,
            "z_score_from_one": (estimate - 1.0) / mc_se if mc_se > 0 else np.nan,
        })
    euler_checks = pd.DataFrame(euler_rows)
    print(euler_checks.to_string(index=False, float_format=lambda x: f"{x:.8f}"))
    print(f"Approximate white-noise ACF reference band: +/- {1.96 / np.sqrt(T):.6f}")
    print(f"Sample mean log excess return: {np.mean(r_d - r_f):.8f}")
    print(f"Population mean log excess return: {(gamma - 0.5) * sigma**2:.8f}")
    simple_equity_sd_theory = (
        np.exp(theory["r_d"][0] + 0.5 * sigma**2)
        * np.sqrt(np.expm1(sigma**2))
    )
    simple_equity_sd_sample = sample_std(np.expm1(r_d))
    print(f"Supplementary simple equity-return SD: sample {simple_equity_sd_sample:.8f}; theory {simple_equity_sd_theory:.8f}")
    print("Structural identities passed. Euler averages need only be close to one.")


    # Cell 7: save the results, run metadata, and a draft submission paragraph.
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(OUT_DIR / "summary.csv", index=False, float_format="%.12g", na_rep="N/A")
    correlations.to_csv(OUT_DIR / "correlations.csv", index_label="series", float_format="%.12g", na_rep="N/A")
    euler_checks.to_csv(OUT_DIR / "euler_checks.csv", index=False, float_format="%.12g")

    metadata = {
        "repository": "financial-economics-ps5",
        "problem": "Assignment 1 Problem 1(d)",
        "frequency": "annual", "T": T, "seed": SEED,
        "random_generator": "NumPy Generator with PCG64",
        "parameters": {"sigma": sigma, "mu": mu, "gamma": gamma, "beta": beta},
        "versions": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__},
        "units": "Natural-log units; growth and returns are annual; m is log SDF.",
        "sample_std": "ddof=1; exactly constant arrays return zero",
        "acf1": "sum((x[1:]-mean(x))*(x[:-1]-mean(x)))/sum((x-mean(x))**2)",
        "N/A": "Undefined because one or both variables have zero variance.",
        "burn_in": "None: all draws are IID and stationary from the first observation.",
        "saved_full_paths": SAVE_PATHS,
    }
    (OUT_DIR / "run_metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")

    sample = summary.set_index("series")
    submission = (
        f"I simulated {T:,} annual observations using the stated calibration and "
        f"one shared IID standard-normal shock per year (PCG64, seed {SEED}). "
        f"The sample standard deviations of log consumption growth, the log SDF, "
        f"and the log equity return were {sample.loc['delta_c', 'sample_std']:.6f}, "
        f"{sample.loc['m', 'sample_std']:.6f}, and {sample.loc['r_d', 'sample_std']:.6f}, "
        f"respectively, close to their population values of {sigma:.3f}, "
        f"{gamma * sigma:.3f}, and {sigma:.3f}. Their lag-one sample autocorrelations "
        f"were all approximately {sample.loc['delta_c', 'sample_acf1']:.6f}, "
        f"consistent with zero population serial correlation. The riskfree rate was "
        f"constant, with zero standard deviation and undefined autocorrelation. "
        f"The consumption-growth/equity-return correlation was {corr_c_equity:.6f}, "
        "as implied by the model's constant price-dividend ratio. The results match "
        "the model's theoretical moments but fail to match important empirical "
        "features discussed in the course: consumption growth is only moderately "
        "correlated with stock returns (Lecture 4, printed p. 146), and riskfree "
        "rates exhibit nonzero volatility (Lecture 4, printed p. 156). The model's "
        f"ordinary equity-return SD is {100 * simple_equity_sd_theory:.2f}%, versus "
        "16.54% for annual real S&P returns in 1889-1978 (Mehra and Prescott, 1985, "
        "Table 1). The model's "
        "3.6% consumption-growth volatility is a calibration input. This exercise "
        "does not estimate new moments from an empirical dataset."
    )
    (OUT_DIR / "submission_paragraph.txt").write_text(submission + "\n", encoding="utf-8")
    if SAVE_PATHS:
        data.assign(epsilon=epsilon).to_csv(OUT_DIR / "simulated_paths.csv", index=False)

    archive = PROJECT_ROOT / "problem1d_results.zip"
    output_files = [
        OUT_DIR / "summary.csv", OUT_DIR / "correlations.csv",
        OUT_DIR / "euler_checks.csv", OUT_DIR / "run_metadata.json",
        OUT_DIR / "submission_paragraph.txt",
    ]
    if SAVE_PATHS:
        output_files.append(OUT_DIR / "simulated_paths.csv")
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for file in output_files:
            z.write(file, arcname=str(Path("results") / "problem1d" / file.name))
    print(submission)
    print("\nSaved:")
    for file in output_files:
        print(f"  {file.relative_to(PROJECT_ROOT)}")
    print(f"  {archive.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
