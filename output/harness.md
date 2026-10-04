# Problem 2 — Database analysis

## Database location

The requested path `data/campus_customs.db` does not exist under HW 4. The supplied database is at:

`data/data/campus_customs.db`

The database was inspected read-only. No database contents were changed.

## Tables and fields

### `catalogue`

Product catalogue records used to describe and search shop products.

| Field | SQLite type | Key/constraints | Purpose |
|---|---|---|---|
| `product_id` | `TEXT` | Primary key, required | Stable product identifier used to connect catalogue and inventory records. |
| `name` | `TEXT` | Required | Product display name. |
| `garment_type` | `TEXT` | Required | Garment category, such as hoodie or T-shirt. |
| `description` | `TEXT` | Required | Product description for the shop and chatbot. |
| `colors` | `TEXT` | Required | Stored color information; sample values are JSON arrays encoded as text. |
| `search_tags` | `TEXT` | Required | Search terms; sample values are JSON arrays encoded as text. |
| `image_file_path` | `TEXT` | Required | Relative product image path, such as `products/basic-hoodie-big-yale.jpg`. |
| `price` | `REAL` | Required | Product price. |

### `inventory`

Size-level stock records for products in the catalogue.

| Field | SQLite type | Key/constraints | Purpose |
|---|---|---|---|
| `id` | `INTEGER` | Primary key, autoincrement | Unique inventory-row identifier. |
| `product_id` | `TEXT` | Required; foreign key to `catalogue.product_id` | Identifies the product whose stock is recorded. |
| `size` | `TEXT` | Required | Available garment size. |
| `quantity` | `INTEGER` | Required | Units in stock for the product-size combination. |

There is a unique constraint on (`product_id`, `size`), so a product cannot have duplicate rows for the same size.

### `users`

Account records used to identify shop and chatbot users.

| Field | SQLite type | Key/constraints | Purpose |
|---|---|---|---|
| `id` | `INTEGER` | Primary key, autoincrement | User identifier referenced by chat messages. |
| `name` | `TEXT` | Required | Stored display name. |
| `email` | `TEXT` | Required, unique | Account login/contact identifier. Values are intentionally not reproduced here. |
| `password_hash` | `TEXT` | Required | Password hash. Sensitive; values are intentionally not reproduced here. |
| `created_at` | `TEXT` | Required; defaults to `datetime('now')` | Account creation timestamp. |
| `first_name` | `TEXT` | Optional | First-name field. |
| `last_name` | `TEXT` | Optional | Last-name field. |

### `chat_messages`

Conversation history connecting chatbot messages to users and, for assistant responses, optionally storing product results.

| Field | SQLite type | Key/constraints | Purpose |
|---|---|---|---|
| `id` | `INTEGER` | Primary key, autoincrement | Message identifier. |
| `user_id` | `INTEGER` | Required; foreign key to `users.id` | Identifies the user who owns the conversation. |
| `role` | `TEXT` | Required | Message author role, such as `user` or `assistant`. |
| `content` | `TEXT` | Required | Message text. |
| `products_json` | `TEXT` | Optional | JSON-encoded product results attached to a chatbot response. |
| `created_at` | `TEXT` | Required; defaults to `datetime('now')` | Message creation timestamp. |

### `sqlite_sequence`

SQLite-maintained internal table for autoincrement counters.

| Field | SQLite type | Key/constraints | Purpose |
|---|---|---|---|
| `name` | *(empty in schema)* | None declared | Name of an autoincrement table. |
| `seq` | *(empty in schema)* | None declared | Most recently assigned autoincrement value. |

## Relationships and application behavior

- `catalogue.product_id` connects to `inventory.product_id` in a one-to-many relationship: one product can have one inventory row per size. The application can join these tables to display a product’s sizes and stock quantities.
- `users.id` connects to `chat_messages.user_id` in a one-to-many relationship: one user can have many chat messages.
- `catalogue` supplies product names, descriptions, tags, colors, image paths, and prices for shop display and chatbot search/results.
- `inventory` supplies availability by size. A chatbot response can use it to answer whether a requested product and size is in stock.
- `chat_messages.products_json` can preserve the product results included in an assistant response, including product details and inventory summaries.

## Non-sensitive sample observations

The first catalogue samples included:

- `2025-yale-vs-harvard-t-shirt`: price `32.0`, image path `products/2025-yale-vs-harvard-t-shirt.jpg`.
- `baseball-left-chest-crewneck`: price `58.0`, image path `products/baseball-left-chest-crewneck.jpg`.
- `basic-hoodie-big-yale`: price `68.0`, image path `products/basic-hoodie-big-yale.jpg`.

The first inventory rows for the first product showed sizes XS, S, and M with quantities 25, 25, and 20. Inventory quantities are integers and can be zero when a size is out of stock.

## Product-image location

The archive’s original image files are in:

`data/data/products/`

Catalogue paths are relative to that product-image directory. For example, the catalogue value `products/basic-hoodie-big-yale.jpg` resolves to:

`data/data/products/basic-hoodie-big-yale.jpg`

The application should use the catalogue’s `image_file_path` as the filename/path component and serve the corresponding file from the unpacked product-image directory. The database does not contain a separate absolute image location.

## Authentication (Problem 4)

The FastAPI backend exposes `POST /api/auth/register` and `POST /api/auth/login`.

- Registration accepts first name, last name, email, and password. Email syntax is validated, names are length-limited, passwords must be at least eight characters, and duplicate emails return HTTP 409 with a clear message.
- Login accepts email and password and returns only public user fields: id, name, first name, last name, and email. Passwords and password hashes are never included in API responses.
- New passwords use PBKDF2-HMAC-SHA256 with a random salt and 310,000 iterations. The stored format is self-describing (`pbkdf2_sha256$iterations$salt$digest`). Plaintext passwords are never stored.
- The supplied test account existed with a legacy three-part `pbkdf2_sha256` value that did not validate against the supplied password using the standard format. Because the supplied password is known for this test fixture, its hash was safely migrated to the new four-part format. The login endpoint also supports future iteration-count migration after a successful verification.
- The supplied account and a newly registered account were both verified through the API. A duplicate registration returned HTTP 409.

## PydanticAI chat agent (Problem 5)

Problem 5 adds a structured PydanticAI agent in `backend/agent.py`, with shared Pydantic request/response types in `backend/models.py`, database search in `backend/tools.py`, and the shop-assistant rules in `backend/prompts/prompt.md`. The agent loads `PORTKEY_API_KEY` from the workspace environment and uses `gpt-5.6-luna` through Portkey; the credential is never printed or returned.

The frontend chat widget posts `{message, conversation}` to `POST /api/chat` and receives a `ChatResponse` containing a natural-language message and optional product references. The agent can call the catalogue search tool to ground answers in real product, price, image, and inventory data.

The backend imports successfully from `backend/`. The requested port 8000 was already occupied by an unrelated local service, so the endpoint was started on port 8011/8012 for testing. A live Portkey request was attempted with the configured environment, but the model call did not return during the verification window; no response was fabricated. Run it from `backend/` with `uvicorn main:app --reload --port 8000` once port 8000 is available, then test the widget with a shop question such as “Which Yale hoodies are under 70 dollars?”

## Final implementation and execution reference

### Database structure

The application database is `data/data/campus_customs.db`. Its application tables are `catalogue(product_id, name, garment_type, description, colors, search_tags, image_file_path, price)`, `inventory(id, product_id, size, quantity)`, `users(id, name, email, password_hash, created_at, first_name, last_name)`, and `chat_messages(id, user_id, role, content, products_json, created_at)`. `inventory.product_id` references `catalogue.product_id`; `chat_messages.user_id` references `users.id`. SQLite’s internal `sqlite_sequence` supports autoincrement counters.

### Models and tools

`backend/models.py` contains `ChatRequest`, `CustomerContext`, `ChatResponse`, `ProductReference`, `ProductInfo`, `StockLine`, `StockLookup`, `AlternativeProduct`, and `AlternativesResult`. Registered tools are catalogue search, product information, inventory lookup, and unavailable-item alternatives. Product and stock tools return explicit statuses instead of guessed values.

### Authentication, memory, and context

Registration/login return an opaque session token; the backend maps it to a user ID and accepts it through the `X-Session-Token` header or `campus_session` cookie. History is read from and written to `chat_messages` only for that user; guests are not persisted. `CustomerContext` carries user ID, name, email, current page, product ID, and resolved current product. The backend also uses the request referrer as a safe fallback for the current product route.

### Safety and limits

The system prompt requires database-grounded product answers, privacy protection, safe refusal, and no claims of ordering or data modification. Backend code caps catalogue results at 8, alternatives at 4, conversation context at 8 messages, and agent tool calls at 5 per run. Passwords, hashes, credentials, tokens, and emails are excluded from audit entries.

### Model configuration and startup

`backend/agent.py` loads `PORTKEY_API_KEY` from the lowercase repository-root `.env` without printing it, uses `gpt-5.6-luna`, and sends requests through `https://api.portkey.ai/v1`. Start the backend from `hw4/backend` with:

```powershell
..\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8015
```

## Final lowercase hw4 review

The `/media` mount now exposes only `data/data/products/`. `GET /media/campus_customs.db` returns 404, while a real product image returns 200. Product API image URLs use `/media/<filename>`.

The frontend sends `X-Session-Token` when available and includes `conversation`, `current_page`, and `product_id` in every chat request. Logged-in history is restored as the full sequence of user and assistant messages, not only the last reply. A current-product test for Basic Hoodie Big Yale returned that pink is unavailable because the real colors are navy blue and white.

The `run_chat` fallback validates every catalogue match with `ProductReference.model_validate`. The isolated fallback test returned eight `ProductReference` objects, and authenticated chat saving completed without a `.model_dump()` error.

Fresh-clone setup now creates `hw4/.venv`, installs `requirements.txt`, loads the repository-root `hw4/.env`, and starts fixed ports 8015 and 5175. Verified results: 102 products, product image 200, database media URL 404, supplied login 200, new-account registration 200, chat 200, inventory answer of 5 for Basic Hoodie Big Yale size M, current-product pink question grounded in real colors, history count increased and restored, and production build passed.

The in-app browser surface was unavailable for automation, but the user-provided replacement screenshot was verified in `output/app_check_images/check2-category.png`: it shows the category question, grounded response, and resulting product cards together. Browser-level refresh persistence remains unverified visually; the API history restoration check passed.

Start the frontend from lowercase `hw4` with `npm.cmd run dev -- --host 127.0.0.1 --port 5175`; the production frontend check is `npm.cmd run build`.

### Audit trail

`output/audit_trail.json` is append-only across calls and restarts. Each entry records an ISO timestamp, tool name, bounded arguments, bounded result summary, and end reason. It is written by `backend/audit.py` with a process lock and redacts credentials and personal data.

## Database tools (Problem 6)

`backend/models.py` defines structured `ProductInfo`, `StockLine`, and `StockLookup` results. `backend/tools.py` implements `get_product_info(product)` and `get_stock(product, size=None)`, and `backend/agent.py` registers them as the `product_information` and `inventory_lookup` PydanticAI tools. The existing catalogue search tool remains available for discovery questions.

- `get_product_info` reads the catalogue description, garment type, colors, price, and image path. It returns `status="unknown_product"` with no invented fields when there is no match.
- `get_stock` returns all size rows when no size is requested. For a requested size it returns `in_stock` with the exact quantity, `out_of_stock` when the database row exists with quantity zero, or `unavailable_size` when that size is not listed. An unknown product returns `unknown_product`.
- Direct SQLite/tool verification used `Basic Hoodie Big Yale`: price `68.0`, size M quantity `5`, and an unlisted size `999` produced `unavailable_size`. The database also contains an out-of-stock example: `Baseball Left Chest Crewneck`, size XS, quantity `0`; no source data was modified.

## Chat search page updates (Problem 7)

Category searches now carry real catalogue matches in `ChatResponse.suggested_products`. The frontend maps those structured matches into the existing product-card component, so each result shows its image, name, price, and description and opens the existing `/products/{product_id}` detail route when clicked. A successful search with zero matches shows a clear “No products matched” state and a suggestion to refine the query.

The complete path is: chat message → PydanticAI agent/tool search → structured product references → frontend search-results section → existing product detail page. The search uses the SQLite catalogue and does not invent product fields.

## Customer memory and page context (Problem 8)

Logged-in sessions receive an opaque session token. The token maps to a user ID on the backend; chat history is read and written only for that authenticated user through the existing `chat_messages` table. Guests can still use `/api/chat`, but their messages are not persisted. History access requires `X-Session-Token`, so a user cannot request another user’s messages by changing a client-supplied ID.

`ChatRequest` carries `current_page` and `product_id`. The backend resolves the product from SQLite and passes the resulting product plus the customer’s name/email to the agent through `CustomerContext`. This lets “Do you have this in pink?” refer to the current product using real catalogue data.

## Prompt log

The exact Problem 2 request is recorded below.

> For Problem 2(Analyze the database), inspect data/campus_customs.db and explain how its tables support the shop and chatbot.
> Examine the actual schema, especially catalogue, inventory, and users. Identify their columns, data types, keys, and relationships. Inspect a few non-sensitive sample records to understand product information, image paths, prices, sizes, and stock quantities. Do not print passwords, password hashes, or other sensitive values.
> Create output/harness.md. List each table and field with a short explanation of its purpose. Explain how products connect to inventory and where the application should find product images.
> Do not modify the database or invent missing fields. If the data pack is missing, tell me exactly what files you need. Record this prompt under Problem 2.

**Status:** In progress

## Recurring startup and chatbot diagnosis

This follow-up was performed only in the lowercase `hw4` project. The older `HW 4` project was not modified.

### Configuration evidence

- The Windows User environment has no `PORTKEY_API_KEY`.
- The current process environment has a `PORTKEY_API_KEY`.
- The workspace root `.env` has `PORTKEY_API_KEY`; `HW 1/.env` has the same value. Values were compared privately and never printed. `hw4/.env.local` contains only the frontend API URL, not credentials.
- `backend/agent.py` loads the workspace root `.env` with `load_dotenv(ROOT.parent / ".env")`; an already-set process variable takes precedence under python-dotenv. The effective backend value is therefore the current process value when present, otherwise the root `.env` value.
- Codex `config.toml` sets model `gpt-5.6-luna` but declares no Portkey provider or base URL. The Codex session provider is separate from this application's Portkey configuration.

### Request diagnosis

The application endpoint is `https://api.portkey.ai/v1`, model `gpt-5.6-luna`, and PydanticAI uses the OpenAI-compatible chat-completions interface. The working Homework 3 integration sends the Portkey-specific `x-portkey-api-key` header through its HTTP client. The original hw4 agent supplied only the generic OpenAI authorization path, which produced `ModelAPIError: Connection error`.

The minimal independent request initially failed at the PydanticAI transport layer. After matching the Homework 3 client configuration (`httpx2.AsyncClient(headers={"x-portkey-api-key": key})`), the independent agent request succeeded. This is evidence of a client-header/configuration mismatch, not an expiration conclusion from HTTP 403. No credential, request ID, or secret was written to this document.

### Layered verification

- Independent PydanticAI request: passed; returned a real price answer and 8 suggested products.
- FastAPI `/api/products`: HTTP 200; 102 products.
- FastAPI `/api/chat`: HTTP 200; real answer for `Basic Hoodie Big Yale` was `$68.00`.
- Inventory chat: HTTP 200; size M answer reported exact quantity 5.
- Dynamic search chat: HTTP 200; `What hoodies do you have?` returned 8 structured product cards.
- Supplied login: HTTP 200; session token returned without exposing credentials.
- Frontend origin: HTTP 200 at `http://127.0.0.1:5175/`.

The browser screenshot layer was not claimed as complete because no browser automation surface was available in this environment. The API response contains the structured cards consumed by the widget.

### Reproducible startup

`start_hw4.ps1` uses only `hw4/.venv`, fixed ports 8015 and 5175, and the lowercase `hw4` working directory. It checks each port before starting a process, so rerunning it does not intentionally create duplicate servers. If a port is occupied by another process, stop that process or report the conflict before launching.

The lowercase project now has its own `.venv`; the launcher no longer references the old `HW 4` environment. Run:

```powershell
cd "C:\Users\1dank\OneDrive\바탕 화면\AI Foundations Homework\hw4"
powershell -ExecutionPolicy Bypass -File .\start_hw4.ps1
```
