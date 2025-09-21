import yaml
from coe import ClassicalOrbitalElements

def main():
    # Load state vector from YAML
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    position = config["state_vector"]["position"]
    velocity = config["state_vector"]["velocity"]

    coe_calc = ClassicalOrbitalElements(position, velocity)
    coe_calc.calculate()
    coe_calc.summary()
    coe_calc.save_to_yaml("orbit_output.yaml")

if __name__ == "__main__":
    main()
