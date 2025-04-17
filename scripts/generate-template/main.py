#!/usr/bin/env python3
from pathlib import Path
import sys

import yaml

def main():
    yaml.add_multi_constructor('!', cloudformation_tag, Loader=yaml.SafeLoader)
    # Load template base
    with open("infra/template.base.yaml") as base_file:
        template = yaml.safe_load(base_file)

    # Asegurar que haya una sección Resources
    template.setdefault("Resources", {})

    files = sorted((path for path in Path("lambdas").rglob("template.yaml")))

    # Buscar todos los templates locales en cada lambda
    for path in files:
        with open(path) as f:
            fragment = yaml.safe_load(f)
            resources = fragment.get("Resources", {})
            template["Resources"].update(resources)

    # Escribir el template final
    with open(sys.argv[1], "w") as out_file:
        yaml.dump(template, out_file, sort_keys=False)

# Soporte para tags tipo !Join, !Sub, !Ref, etc.
def cloudformation_tag(loader, tag_suffix, node):
    tag_name = tag_suffix if tag_suffix == "Ref" else f"Fn::{tag_suffix}"
    if isinstance(node, yaml.ScalarNode):
        return {tag_name: loader.construct_scalar(node)}
    elif isinstance(node, yaml.SequenceNode):
        return {tag_name: loader.construct_sequence(node)}
    elif isinstance(node, yaml.MappingNode):
        return {tag_name: loader.construct_mapping(node)}

# Registrar soporte de funciones intrínsecas con !X

if __name__ == "__main__":
    main()
