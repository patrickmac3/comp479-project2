from build_index import build_index
from clustering import cluster
import argparse




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50, help="Maximum number of PDFs to download")
    parser.add_argument("--k", type=int, default=7, help="Number of clusters")
    parser.add_argument("--top", type=int, default=20, help="Number of top terms per cluster")
    # parser.add_argument("--index", type=str, default="index/index.json", help="Index file path (json)")
    # parser.add_argument("--mapper", type=str, default="index/mapper.json", help="Mapper file path (json)")
    args = parser.parse_args()
    build_index(limit=args.limit)
    cluster(args.k, args.top, index_path="index/mapper.json", mapper_path="index/mapper.json")