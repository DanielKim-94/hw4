import os
import httpx2 as httpx
from pathlib import Path

from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from pydantic_ai import UsageLimits
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from models import AlternativesResult, ChatResponse, CustomerContext, ProductInfo, StockLookup
from tools import alternative_products, get_product_info, get_stock, search_catalogue
from audit import audit_event

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT.parent / ".env")
MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
if not PORTKEY_API_KEY:
    raise RuntimeError("PORTKEY_API_KEY is not configured. Add it to the workspace .env or environment.")

SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "prompt.md").read_text(encoding="utf-8")
portkey_client = httpx.AsyncClient(
    headers={"x-portkey-api-key": PORTKEY_API_KEY}, timeout=30.0
)
provider = OpenAIProvider(
    api_key=PORTKEY_API_KEY,
    base_url="https://api.portkey.ai/v1",
    http_client=portkey_client,
)
shop_agent = Agent(OpenAIChatModel(MODEL_NAME, provider=provider), output_type=ChatResponse, deps_type=CustomerContext, system_prompt=SYSTEM_PROMPT)

@shop_agent.tool
def catalogue_search(ctx: RunContext[None], query: str) -> list[dict]:
    """Search real Campus Customs products, prices, image paths, and size stock."""
    return search_catalogue(query)

@shop_agent.tool
def product_information(ctx: RunContext[None], product: str) -> ProductInfo:
    """Retrieve the database-backed description, price, colors, and image path for a product."""
    return get_product_info(product)

@shop_agent.tool
def inventory_lookup(ctx: RunContext[None], product: str, size: str | None = None) -> StockLookup:
    """Retrieve exact database stock; distinguish unknown products, unavailable sizes, and zero stock."""
    return get_stock(product, size)

@shop_agent.tool
def alternatives_for_unavailable(ctx: RunContext[None], product: str) -> AlternativesResult:
    """Recommend real catalogue alternatives and explain the database-backed similarity."""
    return alternative_products(product)

def run_chat(message: str, conversation: list[dict[str, str]] | None = None, customer: CustomerContext | None = None) -> ChatResponse:
    history = conversation or []
    customer = customer or CustomerContext()
    context = customer.model_dump(exclude_none=True)
    prompt = "Customer/page context (use this to resolve references like 'this'):\n" + str(context) + "\n\nRecent conversation:\n" + "\n".join(f"{item.get('role', 'user')}: {item.get('content', '')}" for item in history[-8:]) + f"\n\nShopper: {message}"
    try:
        answer = shop_agent.run_sync(prompt, deps=customer, usage_limits=UsageLimits(tool_calls_limit=5)).output
    except Exception as exc:
        audit_event("agent_run", {"message": message}, {"error": type(exc).__name__}, "agent run failed")
        raise
    if not answer.suggested_products:
        matches = search_catalogue(message)
        answer.suggested_products = [{"product_id": item["product_id"], "name": item["name"], "price": item["price"], "image_url": item["image_url"], "garment_type": item["garment_type"], "description": item["description"]} for item in matches]
    audit_event("agent_run", {"message": message}, {"suggested_product_count": len(answer.suggested_products)}, "agent run completed")
    return answer
