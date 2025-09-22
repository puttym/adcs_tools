I want a Python package that computes Classical Orbital Elements (COEs) from a state vector (position r, velocity v). Please provide design first, then the implementation and tests.

### REQUIREMENTS

Input:

- Read one or many state vectors from a YAML file. Each state must include:
    - name (optional)
    - r: 3-element list (km)
    - v: 3-element list (km/s)
    - mu (optional; default MU_EARTH)

Outputs:

- Compute the classical orbital elements:
    1. Specific angular momentum
    2. Inclination
    3. RAAN
    4. Eccentricity vector
    5. Argument of perigee
    6. True anomaly
    7. Semi-major axis (additional)
- Store computed COEs in a Python dict (full float64 precision).
- Display a pretty table on the console for humans (rounded to 2 decimals).
- Save a YAML output with full float64 precision (no NumPy tags).

### DESIGN & STRUCTURE

- Modular package structure (core computation, I/O, display).
- One main class `ClassicalOrbitalElements` with a clear public API:
    - `__init__(position, velocity, mu=MU_EARTH)` : validate inputs
    - `calculate() -> Dict[str, float]` : returns full-precision COE dict
    - `summary(decimals=2) -> Dict[str, float]` : prints a neatly formatted table for quick check
    - `save_to_yaml(filename)` : writes full-precision YAML
    - `safe_arccos(x)`: Numerically safe arccos with clamping to [-1, 1]
- Top-level helpers for reading input YAML and writing output YAML.
- `main.py` CLI to run batch/one-case processing.

### ERROR HANDLING (explicit)

- Use a small custom exception hierarchy:
    - `COEError` (base)
    - `InputValidationError` (invalid shapes/types/values)
    - `InputParseError` (YAML parse issues)
    - `ComputationError` (numerical failures)
- Input validation rules (raise `InputValidationError` with clear message):
    - `r` and `v` must be sequences of length 3.
    - All entries must be finite numbers (no `NaN`/`Inf`).
    - `r` and `v` cannot be the zero vector.
- File & parse errors:
    - If input file missing => raise or propagate `FileNotFoundError`.
    - If YAML is malformed => wrap `yaml.YAMLError` into `InputParseError` with a readable message and line info if available.
- Numerical edge cases:
    - Undefined orbital elements (e.g., ω for circular or RAAN for equatorial): return `None` in the dict and write `null` to YAML. Document this behavior.
    - If the user prefers strict behavior, allow a `strict` flag to raise an exception instead of returning `None`.
- CLI behavior:
    - On fatal errors, print a one-line human-friendly error and exit with non-zero status.
    - `-verbose` prints full traceback for debugging.

### TESTING (pytest)

- Use pytest and YAML-driven test cases.
- Tests must include assertions that the code raises the correct exceptions with helpful messages for:
    - Missing required keys.
    - Wrong-length vectors.
    - Non-numeric entries.
    - Zero vectors.
    - Malformed YAML input.
- Also include normal and degeneracy cases (circular, equatorial, polar, hyperbolic if supported).
- Tests should validate both dict outputs (full precision checks with tolerances) and display output (string contains rounded numbers and headers).
- For YAML parse tests, include a deliberately corrupted YAML file.

### DOCUMENTATION & USABILITY

- Google-style docstrings on all public classes/methods explaining exceptions raised and return types.
- README with sample input YAML, CLI usage, and examples of error messages and expected YAML `null` values for undefined elements.

### DELIVERABLES

1. Package with modular files: core class, io helpers, display helpers.
2. `main.py` driver with CLI args (`-input`, `-output`, `-index`, `-verbose`, `-strict`).
3. Unit tests and test YAML files in a `tests/` folder.
4. README and example YAMLs.

### DEFAULTS & POLICIES (unless I specify otherwise)

- Represent undefined orbital elements as `null` in YAML.
- Abort processing on malformed entries in multi-case YAML (fail-fast) unless `-skip-bad` is provided.
- Console display: 2 decimal places; YAML: full float64.
- By default compute for any `e` (including hyperbolic); do not raise for e >= 1.

---

### A few quick implementation tips (for whoever writes the code)

Validate inputs early (in `__init__`), so `compute()` can assume valid numbers.

Convert NumPy scalars to native Python floats before YAML dump (or use a small helper to recursively convert).

Use `argparse` for the CLI; return non-zero exit codes on exceptions after printing a friendly message.

Write pytest cases to assert `with pytest.raises(InputValidationError, match="r must be a 3-element"):` etc.