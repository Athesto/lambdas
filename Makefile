.PHONY: setup-generate-template generate-template validate-template
.SILENT:

setup-generate-template:
	python3 -m venv venv
	. venv/bin/activate && { \
		pip3 install -r scripts/generate-template/requirements.txt; \
		pip3 list; \
	}

generate-template:
	. venv/bin/activate && python3 scripts/generate-template/main.py template.yaml

validate-template:
	. venv/bin/activate && python3 scripts/generate-template/main.py template.generated.yaml
	@echo "Validating template.generated.yaml against template.yaml..."
	@diff -y --color template.yaml template.generated.yaml || { \
		echo "❌ Los archivos son diferentes. Ejecuta 'make generate-template' y revisa los cambios."; \
		exit 1; \
	}
	@echo "✅ Los archivos son iguales."
