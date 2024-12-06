from index import Index
from pdf_crawler import PdfCrawler
from pipeline import Pipeline
import argparse

def build_index(limit):


    # initialize the pipeline 
    pipeline = Pipeline()
    
    # # start the pipeline with the pdf crawler and a limit of  pdfs
    pipeline.start(PdfCrawler, limit)
    
    # # save the index after the pipeline is done
    pipeline.index.save()

    del pipeline # free memory  




if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50, help="Maximum number of PDFs to download")
    args = parser.parse_args()
    build_index(limit=args.limit)
