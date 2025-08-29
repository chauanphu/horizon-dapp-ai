import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlResult, CrawlerRunConfig, LLMConfig
from crawl4ai import LLMExtractionStrategy
# from neo4j import GraphDatabase
import litellm
from .models import KnowledgeGraph

litellm._turn_on_debug()
CRYPTO_SITES = [
    "https://coin98.net/jump-trading-crypto",
    "https://www.coindesk.com/",
    "https://cointelegraph.com/",
    "https://decrypt.co/",
    "https://bitcoinmagazine.com/",
    "https://thedefiant.io/",
]

OLLAMA_MODEL = "ollama/gemma3:12b"   # or "llama3:8b", etc.
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "neo4j_password"


extra_args = {"temperature":0, "top_p": 0.9, "max_tokens": 2000}

llm_config=LLMConfig(
    provider=OLLAMA_MODEL
)

llm_strat = LLMExtractionStrategy(
    llm_config=llm_config,
    schema=KnowledgeGraph.model_json_schema(),
    extraction_type="schema",
    instruction="Extract entities and relationships related to cryptocurrencies from the content. Return valid JSON",
    chunk_token_threshold=800,
    apply_chunking=True,
    input_format="html",
    extra_args=extra_args
)

crawl_config = CrawlerRunConfig(
    extraction_strategy=llm_strat,
    cache_mode=CacheMode.BYPASS,
    excluded_tags=["script", "style", "noscript", "header", "footer", "svg", "img", "button", "form"],
)

async def main():
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        url = CRYPTO_SITES[0]
        results: CrawlResult = await crawler.arun(url=url, config=crawl_config)

        if results.success:
            print("Crawl succeeded.")
            with open("kb_result.json", "w", encoding="utf-8") as f:
                f.write(results.extracted_content)
            llm_strat.show_usage()
        else:
            print("Crawl failed:", results.error_message)

if __name__ == "__main__":
    asyncio.run(main())