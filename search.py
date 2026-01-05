import os
import zipfile
import requests
from pathlib import Path
import minsearch

def download_and_index():
    """Download FastMCP repo, extract md/mdx files, and index them with minsearch"""

    # Download the zip file if not already downloaded
    zip_path = "fastmcp-main.zip"
    if not os.path.exists(zip_path):
        print("Downloading FastMCP repository...")
        url = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
        response = requests.get(url)
        response.raise_for_status()
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {zip_path}")
    else:
        print(f"{zip_path} already exists, skipping download")

    # Extract and process md/mdx files
    documents = []
    print("\nProcessing markdown files...")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.filelist:
            filename = file_info.filename

            # Only process md and mdx files
            if filename.endswith('.md') or filename.endswith('.mdx'):
                # Remove the first part of the path (fastmcp-main/)
                clean_filename = filename.replace('fastmcp-main/', '', 1)

                # Read the content
                with zip_ref.open(file_info) as f:
                    try:
                        content = f.read().decode('utf-8')
                        documents.append({
                            'filename': clean_filename,
                            'content': content
                        })
                        print(f"  Indexed: {clean_filename}")
                    except Exception as e:
                        print(f"  Error reading {clean_filename}: {e}")

    print(f"\nTotal documents indexed: {len(documents)}")

    # Create minsearch index
    index = minsearch.Index(
        text_fields=['content', 'filename'],
        keyword_fields=[]
    )

    # Fit the index with documents
    index.fit(documents)

    return index, documents

def search(index, query: str, top_k: int = 5):
    """Search the index and return top_k most relevant documents"""
    results = index.search(
        query=query,
        filter_dict={},
        boost_dict={},
        num_results=top_k
    )
    return results

if __name__ == "__main__":
    # Build the index
    index, documents = download_and_index()

    # Test with the query "demo"
    print("\n" + "="*80)
    print("Searching for: 'demo'")
    print("="*80)

    results = search(index, "demo", top_k=5)

    print(f"\nTop 5 results:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc['filename']}")
        print(f"   Content preview: {doc['content'][:100]}...")

    if results:
        print(f"\n{'='*80}")
        print(f"ANSWER: The first file returned is: {results[0]['filename']}")
        print(f"{'='*80}")
