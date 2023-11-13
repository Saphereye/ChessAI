.SILENT:

all: run

install:
	pip install -r requirements.txt

requirements:
	pip freeze > requirements.txt

run:
	python3 main.py

list_bots:
	for file_path in $$(find "./bots" -type f ! -path "./bots/__pycache__/*"); do \
		file_name=$$(basename -- "$$file_path"); \
		file_name_without_extension=$${file_name%.*}; \
		file_name_without_underscores=$$(echo "$$file_name_without_extension" | tr _ ' '); \
		echo "$$file_name_without_underscores"; \
	done

profile:
	python3 chess_profile.py > profiling/profile.txt