from index import Index
from pdf_crawler import PdfCrawler
from pipeline import Pipeline
import argparse

def build_index(limit, index_path, mapper_path):


    # initialize the pipeline 
    pipeline = Pipeline()
    
    # # start the pipeline with the pdf crawler and a limit of  pdfs
    pipeline.start(PdfCrawler, limit, index_path, mapper_path)
    
    # # save the index after the pipeline is done
    pipeline.index.save()

    del pipeline # free memory  




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=400, help="Maximum number of PDFs to download")
    parser.add_argument("--index", type=str, default="index/index.json", help="Index file path (json)")
    parser.add_argument("--mapper", type=str, default="index/mapper.json", help="Mapper file path (json)")
    args = parser.parse_args()
    build_index(limit=args.limit, index_path=args.index, mapper_path=args.mapper)
