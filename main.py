from fastmcp import FastMCP
import requests
import os
import zipfile
import minsearch

mcp = FastMCP("Demo 🚀")

# Initialize index as None - will be loaded when needed
index = None
documents = []

def _load_index():
    """Load the FastMCP documentation index"""
    global index, documents

    if index is not None:
        return index

    # Download the zip file if not already downloaded
    zip_path = "fastmcp-main.zip"
    if not os.path.exists(zip_path):
        url = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
        response = requests.get(url)
        response.raise_for_status()
        with open(zip_path, 'wb') as f:
            f.write(response.content)

    # Extract and process md/mdx files
    documents = []
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file_info in zip_ref.filelist:
            filename = file_info.filename
            if filename.endswith('.md') or filename.endswith('.mdx'):
                clean_filename = filename.replace('fastmcp-main/', '', 1)
                with zip_ref.open(file_info) as f:
                    try:
                        content = f.read().decode('utf-8')
                        documents.append({
                            'filename': clean_filename,
                            'content': content
                        })
                    except:
                        pass

    # Create and fit minsearch index
    index = minsearch.Index(
        text_fields=['content', 'filename'],
        keyword_fields=[]
    )
    index.fit(documents)

    return index

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool
def scrape_web(url: str) -> str:
    """Scrape web page content using Jina reader and return as markdown"""
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    response.raise_for_status()
    return response.text

@mcp.tool
def search_docs(query: str, num_results: int = 5) -> str:
    """Search FastMCP documentation and return most relevant results"""
    idx = _load_index()

    results = idx.search(
        query=query,
        filter_dict={},
        boost_dict={},
        num_results=num_results
    )

    # Format results as a readable string
    output = f"Found {len(results)} results for query: '{query}'\n\n"
    for i, doc in enumerate(results, 1):
        output += f"{i}. {doc['filename']}\n"
        output += f"   Preview: {doc['content'][:200]}...\n\n"

    return output

if __name__ == "__main__":
    mcp.run()
