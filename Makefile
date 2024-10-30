PROJECT_NAME=JUCHATS

test:
	/Users/tom/anaconda3/envs/py39/bin/pytest -n auto -vvv tests


env:
	@cat .env | base64 | tr -d '\n' | gh secret set  ${PROJECT_NAME}_ENV
	@echo "Environment variable updated"
	@gh secret list