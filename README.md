# data-extraction-vlm

A framework for extracting structured data from documents using Vision Language Models (VLMs).

## Features

- **Dynamic Model Creation:** Automatically generates Pydantic models for data extraction schemas based on configurable JSON files.
- **Multi-LLM Support:** Easily switch between different LLM backends (e.g., Groq, Gemini) via configuration.
- **Pluggable File Utilities:** Handles PDF-to-image conversion and file uploads (Azure Blob Storage, Gemini file upload).
- **Extensible Data Extractors:** Supports both serializable and non-serializable extraction workflows.
- **Prompt Customization:** Uses configurable prompt templates for LLM interaction.

## Project Structure

```
src/
  config.py                # Configuration mappings for LLMs, file utils, and extractors
  data_extractors.py       # Data extraction logic and base classes
  enum_config.py           # Enum definitions for LLMs and extractor types
  file_utils/              # File utility classes (PDF/image conversion, uploads)
  llm_clients/             # LLM client wrappers (Groq, Gemini, etc.)
  prompt_utils/            # Prompt templates, dynamic model creation, and schemas
run.py                     # Example script for dynamic model creation and extraction
extraction.py              # Main DataExtraction workflow class
extraction_input_state.py  # TypedDict for input state configuration
```

## Quick Start

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   - Set up your `.env` file with required API keys (e.g., `GROQ_API_KEY`, `GEMINI_API_KEY`).

3. **Run dynamic model creation:**
   ```sh
   python run.py
   ```

4. **(Optional) Run extraction:**
   - Uncomment and configure the `ExtractionInputState` section in `run.py` to perform data extraction.

## Configuration

- **Prompt and schema configs:**  
  Located in `src/prompt_utils/configs/` and `src/prompt_utils/schemas/`.
- **Supported LLMs:**  
  See [`src/enum_config.py`](src/enum_config.py) and [`src/llm_clients/`](src/llm_clients/).
- **File utilities:**  
  See [`src/file_utils/`](src/file_utils/).

## License

Apache 2.0