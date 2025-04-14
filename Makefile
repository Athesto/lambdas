.PHONY: setup-generate-template generate-template validate-template
.SILENT:

setup-generate-template:
	python3 -m venv venv
	source venv/bin/activate && { \
		pip3 install -r scripts/generate-template/requirements.txt; \
		pip3 list; \
	}

generate-template:
	[ -n "$$VIRTUAL_ENV" ] || { echo "Virtual Environment not found" && exit 1; }
	source venv/bin/activate && python3 scripts/generate-template/main.py template.yaml

validate-template:
	[ -n "$$VIRTUAL_ENV" ] || { echo "Virtual Environment not found" && exit 1; }
	source venv/bin/activate && python3 scripts/generate-template/main.py template.generated.yaml
	@echo "Validating template.generated.yaml against template.yaml..."
	@diff template.yaml template.generated.yaml || { \
		echo "❌ Los archivos son diferentes. Ejecuta 'make generate-template' y revisa los cambios."; \
		exit 1; \
	}
	@echo "✅ Los archivos son iguales."
