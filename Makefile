ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.PHONY: help install run build test docker-up docker-down clean gcp-upload pipeline deploy

help:
	@echo "Usage:"
	@echo "  make install      Install project dependencies"
	@echo "  make run          Run the FastAPI application locally"
	@echo "  make build        Build the Docker image"
	@echo "  make test         Run unit tests"
	@echo "  make docker-up    Start the services using docker-compose"
	@echo "  make docker-down  Stop the services using docker-compose"
	@echo "  make gcp-upload   Upload local embeddings to GCP Storage"
	@echo "  make pipeline     Run the embedding generation pipeline"
	@echo "  make deploy       Deploy the application to GCP Cloud Run"
	@echo "  make clean        Remove cache and compiled files"

install:
	pip install -r requirements.txt

run:
	python -m uvicorn ikea_recommender.app.main:app --reload

build:
	docker build -t ikea-smartsuggest .

test:
	python -m pytest ikea_recommender/tests/ -v

docker-up:
	docker-compose up --build -d

docker-down:
	docker-compose down

pipeline:
	python -m ikea_recommender.pipelines.embedding_pipeline

gcp-upload:
	@echo "Uploading to gs://$(GCP_BUCKET_NAME)..."
	gsutil cp data/product_embeddings.npy gs://$(GCP_BUCKET_NAME)/indexing/product_embeddings.npy
	gsutil cp data/product_ids.csv gs://$(GCP_BUCKET_NAME)/indexing/product_ids.csv

deploy:
	@echo "Building and deploying to Cloud Run..."
	gcloud builds submit --tag gcr.io/$(GCP_PROJECT_ID)/ikea-smartsuggest
	gcloud run deploy ikea-smartsuggest-api \
		--image gcr.io/$(GCP_PROJECT_ID)/ikea-smartsuggest \
		--platform managed \
		--region $(GCP_LOCATION) \
		--allow-unauthenticated \
		--memory 2Gi \
		--cpu 2 \
		--set-env-vars GCP_PROJECT_ID=$(GCP_PROJECT_ID),GCP_LOCATION=$(GCP_LOCATION),BASE_DATA_PATH=./data

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
