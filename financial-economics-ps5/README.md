**Financial Economics PS5**

Computational work accompanying the Financial Economics problem set. Repository name: financial-economics-ps5. The course source PDF is titled Assignment 1. This repository starts with the complete Problem 1(d) IID simulation and will also contain the required computational work for Problem 2.

**Contents available now**

| Problem | Worked notebook | Runnable script | Saved outputs |
|---|---|---|---|
| 1(d) IID consumption growth | [notebooks/problem1d.ipynb](notebooks/problem1d.ipynb) | [scripts/problem1d.py](scripts/problem1d.py) | [results/problem1d/summary.csv](results/problem1d/summary.csv) |

**Planned additions when we reach Problem 2**

| Problem | Notebook path | Script path | Output directory |
|---|---|---|---|
| 2(b) AR(1) consumption growth | notebooks/problem2b.ipynb | scripts/problem2b.py | results/problem2b/ |
| 2(c) Bond yields | notebooks/problem2c.ipynb | scripts/problem2c.py | results/problem2c/ |

The planned files will be added after their equations are derived. The current package implements Problem 1(d). All observations are annual and the provided reference run uses T=100,000 with seed=42. The original course PDFs are not included.

**1. Create the repository once.** Sign into GitHub and visit https://github.com/new . Use your personal account as Owner and enter financial-economics-ps5 exactly as the repository name. A suitable description is Financial Economics Problem Set 5 simulations for Problems 1 and 2. Private is the initial visibility used in this guide; follow any course-specific visibility instructions. Leave the initial README, generated gitignore and license unset because this bundle already provides the project files. Click Create repository. If financial-economics-ps5 already exists, use that repository and add these files.

**2. Upload the unpacked project contents.** In the empty repository, click uploading an existing file. In an existing repository, use Add file > Upload files. Upload the CONTENTS of the financial-economics-ps5 folder, so README.md and requirements.txt are at the repository root alongside notebooks/, scripts/ and results/. Uploading the project ZIP alone does not unpack it. Use a commit message such as Add Problem 1d simulation and shared PS5 structure. Show hidden files if needed to include .gitignore and .devcontainer/devcontainer.json. If your file picker omits them, use Add file > Create new file, type the complete relative path and paste the supplied contents. The Colab route only needs the notebook; the development-container file automates Codespaces setup.

**3. Understand where Python runs.** GitHub stores and versions the files. Colab or GitHub Codespaces runs them. GitHub's file viewer and github.dev editor do not execute Python. Recommended beginner route: store all work in this one repo and execute the self-contained notebooks in Colab. Alternative: execute in Codespaces using the same repo.

**4. Colab setup.** Open https://colab.research.google.com and sign in. Choose File > Upload notebook and select problem1d.ipynb from the downloaded notebooks/ folder. Save a personal copy in Drive. Use a Python 3 CPU runtime. Read the explanatory cells and run each code cell in order using Shift+Enter, or Runtime > Run all. If NumPy or pandas is missing, install with `%pip install numpy pandas` in a separate cell, restart if prompted and run from the top. The notebook prints the actual installed versions. No repository clone, Drive mount or external dataset is required for this notebook.

**5. Colab output locations and saving.** The notebook writes results/problem1d/ under its current runtime directory and creates problem1d_results.zip. Download the completed notebook through the File menu. Download problem1d_results.zip using the Files sidebar, or run:

```python
from google.colab import files
files.download(str(PROJECT_ROOT / "problem1d_results.zip"))
```

Unzip the results locally. To save the executed notebook on GitHub, open the repository's notebooks/ folder and use Add file > Upload files to upload problem1d.ipynb there, replacing the same filename. To save outputs, return to the repository ROOT and upload the extracted results/ folder, preserving results/problem1d/ inside it. This avoids creating duplicate notebooks at the root or nesting results/ inside results/problem1d/. Commit with a message such as Run Problem 1d with seed 42. Colab's temporary runtime files and the saved notebook are separate; preserve both the executed notebook and the output files.

**6. Codespaces setup.** Open financial-economics-ps5 on GitHub and choose Code > Codespaces > Create codespace on main. Wait for setup to finish. The supplied .devcontainer configuration requests Python 3.12 and installs NumPy, pandas and a notebook kernel. Open notebooks/problem1d.ipynb in browser VS Code, choose the Python environment/kernel if asked and select Run All. If dependencies were not installed automatically, open Terminal > New Terminal and run from the repository root:

```bash
python --version
python -m pip install -r requirements-notebook.txt
```

For a script run from the repository root:

```bash
python scripts/problem1d.py
```

The notebook/script path helper locates the repository root even if the notebook starts in notebooks/. Both save to results/problem1d/ and create problem1d_results.zip at the repository root. Codespaces settings have been checked against official documentation; the delivered numerical work was executed locally, not on your GitHub account.

**7. Save Codespaces work in GitHub.** Save the notebook and inspect changes. Stage only the files you intend to submit. For Problem 1(d):

```bash
git status
git add notebooks/problem1d.ipynb scripts/problem1d.py results/problem1d/
git commit -m "Run Problem 1d simulation with seed 42"
git push
```

Stage README.md or requirements files too if you changed them. If the rerun produced no differences, Git may correctly report nothing to commit. Verify the saved notebook and CSVs on the GitHub website. Then visit https://github.com/codespaces and use the codespace menu > Stop codespace. Closing its browser tab alone does not stop compute. Check current account allowances and storage usage; delete a codespace only after pushing the work you want to keep.

**8. Read Problem 1(d)'s outputs.** results/problem1d/summary.csv contains the sample and analytical means, standard deviations and first autocorrelations. correlations.csv contains contemporaneous correlations. euler_checks.csv checks E[M times gross return]=1. run_metadata.json records frequency, calibration, seed, library versions and estimator definitions. submission_paragraph.txt contains a draft interpretation of the actual run. The zip archives these small outputs with paths results/problem1d/.... Full raw observations are omitted by default; SAVE_PATHS=True exports them. Generated results ZIPs and optional raw paths are ignored by Git; the small CSVs and metadata are tracked.

**9. Keep the numerical conventions explicit.** Each of 100,000 rows is one annual observation. r_f is the log riskfree rate, delta_c is log consumption growth, m is the log SDF, and r_d is the log equity return. All stochastic series use one shared shock. Sample SD uses ddof=1. ACF1 uses the full-sample mean and the ratio stated in the notebook. The constant riskfree series has SD zero and undefined ACF. Its N/A is a valid answer. The IID simulation has no burn-in. The code records the exact NumPy/pandas versions used; requirements.txt pins the verified versions.

**10. Extend this repository for Problem 2.** Keep notebooks/problem1d.ipynb and results/problem1d/ as the IID benchmark. When we reach Problem 2(b), add notebooks/problem2b.ipynb and scripts/problem2b.py with results/problem2b/. When we reach bond yields in Problem 2(c), add notebooks/problem2c.ipynb and scripts/problem2c.py with results/problem2c/. Use the same root requirements and notebook environment. Reuse statistical helpers where appropriate, but first derive the AR(1), equity-pricing and bond-pricing equations. An AR(1) simulation needs its own initialization/stationarity treatment; do not automatically carry over the IID no-burn-in argument. Update the README table with live links after each notebook exists. Commit each completed problem with a descriptive message.

**11. Link this repository in the submitted problem set.** Replace YOUR_USERNAME in https://github.com/YOUR_USERNAME/financial-economics-ps5 with your actual account. The root README is the index for the marker. Include the numerical results and economic explanations directly in the written assignment as well. A suggested submission sentence is: Computational code and reproducible outputs are available in financial-economics-ps5 at [your repository URL]; Problem 1(d) is in notebooks/problem1d.ipynb and results/problem1d/, with Problem 2 indexed in the README when added.

**12. Ensure the intended marker can open the link.** A private repository's URL does not itself grant access. Follow the course's sharing instructions. For a private personal repository, the invitation route is Settings > Collaborators > Add people, then select the intended marker's actual GitHub account and send the invitation. They must accept it. Personal-repository collaborators have read and write access; do not describe this as a read-only invitation. No collaborator invitation or visibility change is performed by this project bundle.

**13. Preserve the submitted revision.** Before submitting, restart the notebook kernel, Run All, save, commit and push the intended notebooks and outputs. In a terminal, `git rev-parse HEAD` displays the commit SHA. You can record that SHA alongside the repo URL. To link a fixed notebook version, view notebooks/problem1d.ipynb on GitHub and press y outside a text field, then copy the permalink. It has the form https://github.com/YOUR_USERNAME/financial-economics-ps5/blob/COMMIT_SHA/notebooks/problem1d.ipynb . Later Problem 2 commits can then extend this same repository while that fixed Part D link remains unchanged. Private access requirements still apply.

**14. Economic interpretation and references.** The notebook derives all four simulation equations and population moments before the seven code cells. It also explains finite-sample error and the empirical shortcomings: the course describes moderate consumption/equity correlation and nonzero riskfree volatility, while this model predicts correlation one and a constant riskfree rate. The supplementary historical equity-volatility comparison converts the model to simple returns before comparing. This work simulates a calibrated model; it does not estimate a new empirical dataset.

Course sources: Howard Kung Assignment 1 Problem 1(d), pp.1-2; Consumption-based asset pricing part 1, slides 5, 49 and 57-62; Francisco Gomes L4 printed pp.143, 146 and 156. Supplementary historical benchmark: Mehra and Prescott (1985), Table 1, https://rajnishmehra.com/wp-content/uploads/2023/09/The-Equity-Premium-A-Puzzle.pdf .

Official setup references: [Create a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository), [upload files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository), [Colab FAQ](https://research.google.com/colaboratory/faq.html), [create a Codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository), [notebook kernels](https://docs.github.com/en/codespaces/developing-in-a-codespace/getting-started-with-github-codespaces-for-machine-learning), [source control](https://docs.github.com/en/codespaces/developing-in-a-codespace/using-source-control-in-your-codespace), [stop a Codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/stopping-and-starting-a-codespace), [Codespaces billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces), [invite collaborators](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/inviting-collaborators-to-a-personal-repository), [personal repository permissions](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/repository-access-and-collaboration/permission-levels-for-a-personal-account-repository), [permanent links](https://docs.github.com/en/repositories/working-with-files/using-files/getting-permanent-links-to-files).
