# Sitemap-Based Data Ingestion

## Overview
The RAG ingestion pipeline now supports extracting URLs from a sitemap.xml file to comprehensively capture all documentation pages, not just manually specified URLs.

## Configuration Options

### Environment Variables
- `USE_SITEMAP`: Set to `true` to enable sitemap-based URL extraction (default: `false`)
- `SITEMAP_URL`: The URL to the sitemap.xml file (default: `https://ai-native-six.vercel.app/sitemap.xml`)
- `DOCUSAURUS_URLS`: Comma-separated list of URLs (used when USE_SITEMAP is false)

### Command Line Options
- `--use-sitemap`: Enable sitemap-based URL extraction
- `--sitemap <URL>`: Specify the sitemap URL to use
- `--urls <URLs>`: Comma-separated list of URLs to process (overrides environment variable)

## Usage Examples

### Using Environment Variables
```bash
export USE_SITEMAP=true
export SITEMAP_URL=https://ai-native-six.vercel.app/sitemap.xml
python main.py
```

### Using Command Line Arguments
```bash
python main.py --use-sitemap --sitemap https://ai-native-six.vercel.app/sitemap.xml
```

## Benefits
- Automatically discovers all documentation pages from the sitemap
- Captures comprehensive content instead of just manually specified URLs
- Handles domain replacement for placeholder URLs in sitemaps
- Provides retry logic for robust sitemap fetching

## Implementation Details
- Parses XML sitemaps with proper namespace handling
- Replaces placeholder domains (your-docusaurus-site.example.com) with actual domains
- Handles both regular sitemaps and sitemap index files
- Includes error handling and retry logic