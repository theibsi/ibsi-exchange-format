---
name: Version Release
about: Version release checklist
title: ''
labels: release
assignees: ''

---

- [ ] Update version
  - [ ] `pyproject.toml`
  - [x] `.\docs_source\source\conf.py` (*currently not applicable*)
- [ ] Check that all unit tests successfully pass.
  - [ ] Run `python -m pytest test`
- [ ] Update `NEWS.md`.
- [ ] Update `README.md` if required.
- [x] Check long-form documentation locally (*currently not applicable*).
  - [x] Open a terminal.
  - [x] Navigate to `.\docs_source`.
  - [x] Run `make` script: `.\make html`
  - [x] Check locally build html pages for obvious errors.
- [x] Copy updated documentation to the `docs` folder. (*currently not applicable*)
  - [x] Empty the `docs` directory, except for `.nojekyll`. *This prevents documentation files from being processed again by GitHub*
  - [x] Copy the contents of `docs_source\build\html` into `docs`. `index.html` should be in the root of the `docs` folder, as GitHub will use this as the landing page.
- [ ] Package for PyPI
  - [ ] Open a terminal.
  - [ ] Navigate to the root directory.
  - [ ] Build package: `python -m build`.
  - [ ] Check package content in `dist\*.tar.gz`.
  - [ ] Upload package to testPyPI:
    - [ ] Run `python -m twine upload --repository testpypi dist\*`
  - [ ] Check package on testPyPI:
	- [ ] Check landing page for obvious errors.
	- [ ] Create virtual environment or temporary conda environment
	- [ ] Install mirp: `pip install ibsi.format --index-url https://test.pypi.org/ibsi.format/ --no-deps`
  - [ ] Upload package to PyPI:
    - [ ] Run `python -m twine upload dist\*`
- [ ] Merge with main branch.
- [ ] Create release.
  - [ ] Copy `NEWS.md`.
  - [ ] Attach package and wheel files from `dist` as binary files.
