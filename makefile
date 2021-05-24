.DEFAULT_GOAL := help
.PHONY: help
help: ## Print this help message
	@echo "----------------------------------------------------------------------"
	@echo "Usage of this makefile"
	@echo "----------------------------------------------------------------------"
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | sed -e 's/$$//' | sed -e 's/:.*##/:,/' | column -t -s ,
	@echo
	@echo "For a dry run use this command: make -n <target>"
	@echo "----------------------------------------------------------------------"

test:
	pytest -rA -v

clean:
	rm -r __pycache__
	rm -r ./.pytest_cache
