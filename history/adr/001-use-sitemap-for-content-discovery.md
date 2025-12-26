# ADR: Use Sitemap-Based Content Discovery for RAG Ingestion

## Context

The RAG ingestion pipeline was initially configured to process manually specified URLs, which resulted in incomplete content capture. Only the landing page and a few manually specified URLs were being ingested, missing important documentation pages like `https://ai-native-six.vercel.app/docs/chapter-1/why-humanoids`.

## Decision

We will implement sitemap-based content discovery to automatically extract all URLs from the Docusaurus-generated sitemap.xml file. This approach will:

- Provide comprehensive coverage of all documentation pages
- Eliminate the need for manual URL specification
- Automatically discover new content as it's added to the site
- Handle domain replacement for placeholder URLs in generated sitemaps

## Status

Accepted

## Alternatives Considered

1. **Manual URL specification**: Continue adding URLs manually - rejected as it's error-prone and doesn't scale
2. **Web crawling**: Implement a crawler to discover URLs by following links - rejected as it's more complex and potentially slower
3. **Static file parsing**: Parse Docusaurus config to extract all documentation paths - rejected as it requires deep integration with Docusaurus build process

## Implementation

- Added `extract_urls_from_sitemap()` function to parse sitemap.xml
- Updated configuration to support `USE_SITEMAP` and `SITEMAP_URL` environment variables
- Enhanced main pipeline to conditionally use sitemap URLs vs. manual URLs
- Added command-line support for sitemap-based ingestion
- Included error handling and retry logic for robust sitemap fetching

## Consequences

### Positive
- Comprehensive content coverage from all documentation pages
- Automatic discovery of new content without manual intervention
- Reduced configuration maintenance overhead
- Improved data quality with complete documentation set

### Negative
- Dependency on sitemap.xml availability and correctness
- Slightly longer initial pipeline startup time for URL extraction
- Potential for ingesting non-content pages (login, signup, etc.)

## Technical Details

- Sitemap parsing handles XML namespaces properly
- Domain replacement for placeholder URLs (your-docusaurus-site.example.com → actual domain)
- Retry logic with exponential backoff for robustness
- Support for both regular sitemaps and sitemap index files