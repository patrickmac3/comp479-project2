import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from index import Index 
from scipy.sparse import dok_matrix
import argparse


def cluster(number_of_clusters=7, n_terms=50, index_path="index_main/index.json" , mapper_path="index_main/mapper.json"):
    index = Index(load=True, index_path=index_path, mapper_path=mapper_path)   

    # Get document IDs and set the number of documents
    doc_ids = list(index.mapper.keys())
    num_docs = len(doc_ids)

    # Filter tokens based on frequency threshold
    tokens = [
        token for token, docs in index.index.items() if len(docs) < 0.750 * num_docs
    ]

    # If no tokens are left after filtering, raise an exception
    if not tokens:
        raise ValueError("All tokens were filtered out. Adjust the threshold.")

    # Create document-term matrix (DTM)
    token_to_index = {token: i for i, token in enumerate(tokens)}
    # dtm = np.zeros((len(doc_ids), len(tokens)), dtype=int)

    dtm = dok_matrix((len(doc_ids), len(tokens)), dtype=int)


    # Populate the document-term matrix
    for token in tokens:
        for doc_id, freq in index.index[token].items():
            row = int(doc_id) - 1
            col = token_to_index[token]  
            dtm[row, col] = freq




    # Apply TF-IDF transformation
    transformer = TfidfTransformer()
    tfidf_matrix = transformer.fit_transform(dtm)

    kmeans = KMeans(n_clusters=number_of_clusters, random_state=42)
    labels = kmeans.fit_predict(tfidf_matrix)

    def get_top_terms_per_cluster(model, n_terms=10):
        """Function to get top terms per cluster based on TF-IDF scores."""
        top_terms = {}
        # Sort the centroids of each cluster
        order_centroids = model.cluster_centers_.argsort()[:, ::-1]
        # Get top n terms for each cluster
        for i in range(model.n_clusters):
            top_terms[i] = [(tokens[ind], model.cluster_centers_[i, ind]) for ind in order_centroids[i, :n_terms]]
        return top_terms
    
    top_terms = get_top_terms_per_cluster(kmeans, n_terms=n_terms)

    print("\ntop terms per cluster:")
    
    with open(f'clustering/top_{n_terms}_terms_{number_of_clusters}_clusters.txt', 'w') as f:
        for cluster in top_terms.keys():
            print(f"\nCluster {cluster}:")
            f.write(f"\nCluster {cluster}:\n")
            for term, score in top_terms[cluster]:
                f.write(f"{term}: {score}\n")
                print(f"{term}: {score}")


    # Save the cluster labels to a CSV file
    cluster_data = pd.DataFrame({'doc_id': doc_ids, 'cluster': labels})
    cluster_data = cluster_data.groupby('cluster')['doc_id'].apply(list).reset_index()
    cluster_data.to_json(f'clustering/cluster_{number_of_clusters}.json', orient='records', indent=4) 
    cluster_data.to_csv(f'clustering/cluster_{number_of_clusters}.csv', index=False)
    print("\nClusters savced to CSV and JSON files.")




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=7, help="Number of clusters")
    parser.add_argument("--top", type=int, default=20, help="Number of top terms per cluster")
    # parser.add_argument("--index", type=str, default="index_main/index.json", help="Index file path (json)")
    # parser.add_argument("--mapper", type=str, default="index_main/mapper.json", help="Mapper file path (json)")
    args = parser.parse_args()
    cluster(args.k, args.top)