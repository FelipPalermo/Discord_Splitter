all : run 

run : 
	source venv/bin/activate; \
	python3 src/main.py
	@trap 'deactivate; exit' INT;\ 

