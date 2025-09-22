## Purpose

Create a Python class that computes the six Classical Orbital Elements (COE) from the state vector of a celestial body.

## Inputs

- YAML file containing the state vector:
    - Position vector (km)
    - Velocity vector (km/s)

## Outputs

1. Python dictionary (full precision)
2. Pretty table on terminal (2 decimal places)
3. YAML file (full float64 precision)

## Class Design

**Class:** ClassicalOrbitalElements

**Methods:**

- `__init__(position, velocity, mu=MU_EARTH)`
    
    Initializes the object with position, velocity, and gravitational parameter.
    
- `_validate_input()`
    
    Checks that position and velocity vectors are valid (non-zero, finite, correct type).
    
- `calculate()`
    
    Computes the six classical orbital elements:
    
    - h, i, RAAN, e, omega, nu
- `summary()`
    
    Displays the COE dictionary as a pretty table (2 decimal places).
    
- `save_to_yaml(filename)`
    
    Writes the COE dictionary to a YAML file with full float64 precision.
    

## Error Handling

- Invalid/missing YAML keys → raise descriptive error
- Non-numeric or malformed input → raise error
- Handle edge cases:
    - Circular orbits (e ~ 0 → omega undefined)
    - Equatorial orbits (i ~ 0 → RAAN undefined)
    - Parabolic orbits (e ~ 1)
    - Very high eccentricity → numerical stability issues

## Implementation

- Use NumPy for vector math
- Use PyYAML for input/output
- Use `tabulate` (or similar) for pretty tables
- Code must be modular and documented in Google style

## Testing Strategy

- Unit tests written with Pytest
- Input from YAML file containing edge cases
- Outputs verified in dict + pretty table
- Human-readable error messages verified

## Data Flow

1. **Load Input**
    - From: YAML file
    - To: `__init__`
2. **Validate**
    - From: `__init__`
    - To: `_validate_input`
3. **Compute**
    - From: `_validate_input`
    - To: `calculate`
    - Output: `coe_dict`
4. **Human-Readable Output**
    - From: `coe_dict`
    - To: `summary`
    - Output: CLI table (2 decimals)
5. **Machine-Readable Output**
    - From: `coe_dict`
    - To: `save_to_yaml`
    - Output: YAML file (full precision)