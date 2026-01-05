# MCP Homework - FastMCP Documentation Search Server

A Model Context Protocol (MCP) server implementation that provides tools for web scraping and documentation search, built as a clone of Context7.

## Features

- **Web Scraping**: Scrape any webpage using Jina Reader and convert to markdown
- **Documentation Search**: Search FastMCP documentation using minsearch
- **MCP Integration**: Works with Claude Desktop, Claude Code, and other MCP-compatible clients

## Installation

```bash
# Install uv package manager
pip install uv

# Clone/navigate to this directory
cd mcp-homework

# Dependencies are managed by uv - they'll be installed automatically when running
```

## Usage

### Running the MCP Server

```bash
# From the project directory
python -m uv run python main.py
```

### Integrating with Claude Desktop

Add to your Claude Desktop MCP configuration file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fastmcp-docs": {
      "command": "python",
      "args": ["-m", "uv", "--directory", "D:\\mcp-homework", "run", "python", "main.py"]
    }
  }
}
```

*Note: Update the path to match your installation directory*

### Available Tools

Once integrated, you can use these tools in your AI assistant:

#### 1. scrape_web(url: str) -> str
Scrape any webpage and convert it to markdown format.

```
Example: "Use scrape_web to get the content of https://github.com/alexeygrigorev/minsearch"
```

#### 2. search_docs(query: str, num_results: int = 5) -> str
Search FastMCP documentation for relevant information.

```
Example: "Search the FastMCP docs for information about 'authentication'"
```

#### 3. add(a: int, b: int) -> int
Simple demo tool to add two numbers.

```
Example: "Add 5 and 7 using the add tool"
```

## Testing

### Test Web Scraping
```bash
python -m uv run python test.py
```

### Test Search Functionality
```bash
python -m uv run python search.py
```

## Project Structure

```
mcp-homework/
├── main.py              # MCP server with all tools
├── test.py              # Web scraping test
├── search.py            # Search functionality test
├── ANSWERS.md           # Homework answers
├── README.md            # This file
├── pyproject.toml       # Project configuration
├── uv.lock              # Dependency lock file
└── fastmcp-main.zip     # Documentation archive (auto-downloaded)
```

## Dependencies

- **fastmcp**: MCP server framework
- **minsearch**: Minimalistic text search engine
- **requests**: HTTP library for web scraping

## How It Works

### Web Scraping
Uses [Jina Reader](https://jina.ai/reader) to convert any webpage to clean markdown by prepending `https://r.jina.ai/` to the URL.

### Documentation Search
1. Downloads the FastMCP repository as a zip file
2. Extracts all `.md` and `.mdx` files
3. Indexes content using minsearch (TF-IDF + sklearn)
4. Returns top-k most relevant documents for queries

## Development

Built with:
- Python 3.14+
- uv for dependency management
- FastMCP 2.14.2
- minsearch 0.0.7

## License

This is a homework project for the AI Dev Tools course.

## Homework Answers

See [ANSWERS.md](ANSWERS.md) for complete homework solutions.
