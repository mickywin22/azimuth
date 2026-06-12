"""azimuth L2 synthesis package.

The ``azimuth-curator`` fleet role reads the week's L1 source notes
(``vault/01 Sources/``) and evolves the ``Energy Supply Weekly`` L2 brief
(``vault/02 Briefs/``). ``synthesis.lint`` is the blocking quality gate
(spec.md F2): pure, stdlib-only verdict logic so the same checks run in CI
and locally. The thin ``scripts/check_synthesis.py`` CLI wires git-diff +
file reads to these pure functions.
"""
