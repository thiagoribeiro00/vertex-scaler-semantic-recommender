from kfp import dsl
from kfp.dsl import component, Output, Artifact, Dataset

@component(base_image="python:3.10", packages_to_install=["pandas", "sentence-transformers"])
def extract_and_embed(
    products_dataset: str,
    output_embeddings: Output[Artifact]
):
    import pandas as pd
    from sentence_transformers import SentenceTransformer
    import os

    df = pd.read_csv(products_dataset)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Simple logic to simulate embedding generation
    descriptions = df.iloc[:100]['product_id'].tolist() # Dummy logic for speed
    embeddings = model.encode(descriptions)
    
    with open(output_embeddings.path, "w") as f:
        f.write("Simulated Embeddings Data")

@component(base_image="python:3.10", packages_to_install=["google-cloud-aiplatform"])
def update_vertex_index(
    embeddings: Artifact,
    index_id: str
):
    print(f"Updating Vertex AI Index {index_id} with new embeddings...")

@dsl.pipeline(
    name="ikea-recommendation-pipeline",
    description="Pipeline to update semantic embeddings in Vertex AI"
)
def recommendation_pipeline(
    project_id: str,
    location: str,
    index_id: str,
    dataset_url: str
):
    embedding_task = extract_and_embed(products_dataset=dataset_url)
    update_task = update_vertex_index(
        embeddings=embedding_task.outputs['output_embeddings'],
        index_id=index_id
    )
