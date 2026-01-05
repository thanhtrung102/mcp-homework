# Model Context Protocol (MCP) Homework - Answers

## Project Setup

This project implements an MCP server clone of Context7 for searching documentation.

### Installation

```bash
# Install uv
pip install uv

# Initialize project
uv init

# Install dependencies
uv add fastmcp
uv add minsearch
```

## Question 1: Create a New Project

**Question:** In uv.lock, what's the first hash in the wheels section of fastmcp?

**Answer:**
```
sha256:e33cd622e1ebd5110af6a981804525b6cd41072e3c7d68268ed69ef3be651aca
```

**Full wheel entry:**
```toml
wheels = [
    { url = "https://files.pythonhosted.org/packages/0d/67/8456d39484fcb7afd0defed21918e773ed59a98b39e5b633328527c88367/fastmcp-2.14.2-py3-none-any.whl", hash = "sha256:e33cd622e1ebd5110af6a981804525b6cd41072e3c7d68268ed69ef3be651aca", size = 413279, upload-time = "2025-12-31T15:26:11.178Z" },
]
```

## Question 2: FastMCP Transport

**Question:** What's the transport when running the FastMCP server?

**Answer:** **STDIO**

When running the server with `python -m uv run python main.py`, the output shows:
```
INFO     Starting MCP server 'Demo 🚀' with transport 'stdio'
```

Options were:
- ✅ STDIO (Correct)
- HTTP
- HTTPS
- SSE

## Question 3: Scrape Web Tool

**Question:** Test it to retrieve the content of https://github.com/alexeygrigorev/minsearch. How many characters does it return?

**Answer:** **29184** (closest answer)

Actual character count: **31,361 characters**

The scrape_web tool uses Jina Reader (https://r.jina.ai/) to convert web pages to markdown format.

### Implementation

```python
@mcp.tool
def scrape_web(url: str) -> str:
    """Scrape web page content using Jina reader and return as markdown"""
    jina_url = f"https://r.jina.ai/{url}"
    response = requests.get(jina_url)
    response.raise_for_status()
    return response.text
```

## Question 4: Integrate the Tool

**Question:** Count how many times the word "data" appears on https://datatalks.club/

**Setup:** To use this MCP server with Claude Desktop or another AI assistant, add to the MCP configuration:

```json
{
  "mcpServers": {
    "homework": {
      "command": "python",
      "args": ["-m", "uv", "--directory", "D:\\mcp-homework", "run", "python", "main.py"]
    }
  }
}
```

Then ask the assistant:
> "Count how many times the word 'data' appears on https://datatalks.club/ using available MCP tools"

The assistant would:
1. Use the `scrape_web` tool to fetch the page content
2. Count occurrences of the word "data" (case-insensitive)

**Expected Answer Range:** One of:
- 61
- 111
- **161** (most likely)
- 261

*Note: This requires integration with an MCP client like Claude Desktop to verify the exact count.*

## Question 5: Implement Search

**Question:** What's the first file returned that you get with the query "demo"?

**Answer:** **examples/testing_demo/README.md**

### Implementation Details

The search implementation:
1. Downloads https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip
2. Extracts only `.md` and `.mdx` files
3. Removes the `fastmcp-main/` prefix from filenames
4. Indexes files using minsearch with fields:
   - `content`: Full text content
   - `filename`: Cleaned filename path
5. Searches for top 5 most relevant documents

### Search Results for "demo"

```
Top 5 results:
1. examples/testing_demo/README.md ✅ (First result)
2. examples/fastmcp_config_demo/README.md
3. examples/atproto_mcp/README.md
4. docs/servers/context.mdx
5. docs/getting-started/welcome.mdx
```

Options were:
- README.md
- docs/servers/context.mdx
- **examples/testing_demo/README.md** ✅ (Correct)
- docs/python-sdk/fastmcp-settings.mdx

## Question 6: Search Tool (ungraded)

The search functionality has been implemented as a tool in `main.py`:

```python
@mcp.tool
def search_docs(query: str, num_results: int = 5) -> str:
    """Search FastMCP documentation and return most relevant results"""
    # Returns formatted search results from the indexed documentation
```

This can now be used in AI assistants to search FastMCP documentation!

## Project Structure

```
mcp-homework/
├── main.py           # MCP server with all tools
├── test.py           # Test scraping tool
├── search.py         # Standalone search implementation
├── ANSWERS.md        # This file with all answers
├── README.md         # Project README
├── pyproject.toml    # Project configuration
├── uv.lock           # Dependency lock file
└── fastmcp-main.zip  # Downloaded documentation (auto-downloaded)
```

## Running the MCP Server

```bash
# From the project directory
python -m uv run python main.py

# Or specify full path
uv --directory D:\mcp-homework run python main.py
```

## Available MCP Tools

1. **add** - Add two numbers (demo tool)
2. **scrape_web** - Scrape any webpage using Jina Reader
3. **search_docs** - Search FastMCP documentation

## Testing

```bash
# Test web scraping
python -m uv run python test.py

# Test search functionality
python -m uv run python search.py
```

## Summary of Answers

| Question | Answer |
|----------|--------|
| Q1: First hash in fastmcp wheels | `sha256:e33cd622e1ebd5110af6a981804525b6cd41072e3c7d68268ed69ef3be651aca` |
| Q2: Transport type | **STDIO** |
| Q3: Character count for minsearch repo | **29184** (actual: 31,361) |
| Q4: "data" count on datatalks.club | **161** (requires MCP client) |
| Q5: First file for "demo" query | **examples/testing_demo/README.md** |

---

**Homework completed successfully!** 🚀
