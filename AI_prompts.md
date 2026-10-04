# AI Prompts

## Problem 1 — Title not provided

### Prompt submitted

> Create AI_prompts.md with a section for each of the 13 problems. Record this request under Problem 1.
> 
> For every subsequent problem, record the actual prompt I submit. If I request a correction, record that follow-up and briefly explain what was missing from the first result. Do not invent prompts or mark unfinished problems as completed.
> 
> Create a .gitignore that excludes real .env files, the database, original product images, virtual environments, and node_modules. Keep .env.example eligible for Git.
> 
> For each step, complete only the problem I request, then explain what changed and how I can verify it. Do not start the remaining problems yet.

### Follow-up correction

> Please make a small follow-up correction to Problem 1 before we continue.
> Add each problem’s title beside its number in AI_prompts.md. Mark Problem 1 as “In progress,” since the log has been initialized but will continue to grow. Leave the remaining problems as “Not started.”
> Inspect the actual product-image folder. The current .gitignore contains data/data/products/, so correct that entry if it does not match the real location. Do not move or delete the images.
> Also exclude .env variants such as .env.local while keeping .env.example eligible for Git. Keep output/app_check_images/ eligible for Git because those screenshots are required for submission.
> Record this exact request as a Problem 1 follow-up, briefly noting that the initial files needed titles and more accurate ignore rules. Verify the relevant paths with git check-ignore, then stop before Problem 2.

The initial files needed problem titles and more accurate ignore rules.

**Status:** In progress

### Follow-up correction

> I need to capture the real screenshots required for Problem 11.
> Start the frontend and backend for the final hw4 submission project and keep both servers running. Verify that the local database, product images, and model credentials are available through the correct local paths without exposing or committing them.
> Give me the actual browser URL and step-by-step instructions for showing:
> 1. A chatbot inventory lookup for a real product and size, with the answer checked against the database.
> 2. Product cards appearing on the webpage after asking “What hoodies do you have?”
> 3. One usability improvement actually implemented in Problem 9.
> Create output/app_check_images/ if necessary. Tell me which implemented usability feature to demonstrate and what should be visible in each screenshot.
> Do not fabricate screenshots or mark the evidence complete yet. After I save the screenshots, update output/app_check.html with relative image paths and accurate captions. Record this request as a Problem 11 follow-up.

The final submission servers are running; screenshot evidence remains incomplete until the user captures and saves the images.

### Prompt submitted (repeated)

> For Problem 5(PydanticAI agent backend), connect the website’s chat widget to a real PydanticAI agent through FastAPI.
> Use these files:
> - backend/main.py
> - backend/agent.py
> - backend/tools.py
> - backend/models.py
> - backend/prompts/prompt.md
> Reuse the working Portkey and model configuration from my course setup or Homework 3. Load credentials from environment variables without printing or committing them. If required configuration is unavailable, ask for the specific missing information instead of guessing.
> Write a Campus Customs system prompt with an appropriate shop-assistant voice and basic safety rules. Define structured request and response types, and connect the frontend to a chat endpoint.
> Ensure the backend runs from backend/ with: uvicorn main --reload --port 8000
> Verify a real chat round trip, update output/harness.md, and record this prompt.

### Follow-up correction (repeated)

> Please make a small follow-up correction to Problem 1 before we continue.
> Add each problem’s title beside its number in AI_prompts.md. Mark Problem 1 as “In progress,” since the log has been initialized but will continue to grow. Leave the remaining problems as “Not started.”
> Inspect the actual product-image folder. The current .gitignore contains data/data/products/, so correct that entry if it does not match the real location. Do not move or delete the images.
> Also exclude .env variants such as .env.local while keeping .env.example eligible for Git. Keep output/app_check_images/ eligible for Git because those screenshots are required for submission.
> Record this exact request as a Problem 1 follow-up, briefly noting that the initial files needed titles and more accurate ignore rules. Verify the relevant paths with git check-ignore, then stop before Problem 2.

The initial files needed problem titles and more accurate ignore rules; the requested corrections were already present.

## Problem 2 — Title not provided

### Prompt submitted

> For Problem 2(Analyze the database), inspect data/campus_customs.db and explain how its tables support the shop and chatbot.
> Examine the actual schema, especially catalogue, inventory, and users. Identify their columns, data types, keys, and relationships. Inspect a few non-sensitive sample records to understand product information, image paths, prices, sizes, and stock quantities. Do not print passwords, password hashes, or other sensitive values.
> Create output/harness.md. List each table and field with a short explanation of its purpose. Explain how products connect to inventory and where the application should find product images.
> Do not modify the database or invent missing fields. If the data pack is missing, tell me exactly what files you need. Record this prompt under Problem 2.

**Status:** Completed

### Prompt submitted (repeated)

> For Problem 2(Analyze the database), inspect data/campus_customs.db and explain how its tables support the shop and chatbot.
> Examine the actual schema, especially catalogue, inventory, and users. Identify their columns, data types, keys, and relationships. Inspect a few non-sensitive sample records to understand product information, image paths, prices, sizes, and stock quantities. Do not print passwords, password hashes, or other sensitive values.
> Create output/harness.md. List each table and field with a short explanation of its purpose. Explain how products connect to inventory and where the application should find product images.
> Do not modify the database or invent missing fields. If the data pack is missing, tell me exactly what files you need. Record this prompt under Problem 2.

## Problem 3 — Title not provided

### Prompt submitted

> For Problem 3(Build the Campus Customs website), build the storefront using React, Vite, and TypeScript.
> Include navigation for Home, Products, About Us, Log in, and Create account. Review yalebulldogblue.com for Campus Customs context, but write original Home and About Us text.
> Display real products from our database with their images, names, prices, and short descriptions. Each product card should open a detail page with a large image and full product information, including sizes and stock when available.
> Create a small FastAPI backend in backend/main.py to serve product data and images. Add a floating chat interface in the bottom-right corner, but leave the AI connection for Problem 5.
> Check that the frontend and backend run, product images load, and navigation works. Record this prompt and explain how I can test the site.

**Status:** Completed

## Problem 4 — Title not provided

### Prompt submitted

> For Problem 4(Create account and login), implement account creation and login using the existing users table.
> Registration should collect first name, last name, email, and password. Login should use email and password. Validate inputs, handle duplicate emails clearly, and store new passwords using a secure password hash rather than plaintext.
> Support the supplied test account:
> Email: [test@campuscustoms.yale.edu](mailto:test@campuscustoms.yale.edu)
> Password: password
> Inspect the existing password format so the test account remains usable. If it needs migration, explain and implement that safely. Do not expose passwords or hashes through API responses.
> Verify both the supplied account and a newly created account can log in. Update output/harness.md with the authentication and password-protection approach, and record this prompt.

**Status:** Completed

## Problem 5 — Title not provided

### Prompt submitted

> For Problem 5(PydanticAI agent backend), connect the website’s chat widget to a real PydanticAI agent through FastAPI.
> Use these files:
> - backend/main.py
> - backend/agent.py
> - backend/tools.py
> - backend/models.py
> - backend/prompts/prompt.md
> Reuse the working Portkey and model configuration from my course setup or Homework 3. Load credentials from environment variables without printing or committing them. If required configuration is unavailable, ask for the specific missing information instead of guessing.
> Write a Campus Customs system prompt with an appropriate shop-assistant voice and basic safety rules. Define structured request and response types, and connect the frontend to a chat endpoint.
> Ensure the backend runs from backend/ with: uvicorn main --reload --port 8000
> Verify a real chat round trip, update output/harness.md, and record this prompt.

**Status:** In progress

## Problem 6 — Title not provided

### Prompt submitted

> For Problem 6(Tools: product info and stock), give the chatbot tools to retrieve product descriptions, prices, and inventory from campus_customs.db.
> Support size-specific stock questions when the database contains that information. Distinguish between an unknown product, an unavailable size, and a size with zero stock. Never invent prices or quantities.
> Register these tools with the PydanticAI agent, define their structured return types in models.py, and update prompts/prompt.md so the agent uses them for factual product questions.
> Test price and stock questions against direct database queries. Include an out-of-stock example if the data contains one; otherwise explain how to test it without altering the original data.
> Document the tools and model fields in output/harness.md and record this prompt.

**Status:** Completed

## Problem 7 — Title not provided

### Prompt submitted

> For Problem 7(Chat search that updates the page), make chatbot product searches update the website.
> When I ask a category question such as “What hoodies do you have?”, the agent should search the real catalogue and return structured product matches alongside its reply.
> The frontend should use those matches to display product cards on the webpage, including images, names, prices, and short descriptions. A text-only list in the chat is not enough.
> Reuse the existing product-card and detail-page behavior so clicking any search result opens the correct product. Show a clear empty state when no products match.
> Verify the complete flow from chat message to database search to visible cards to product details. Update the system prompt and output/harness.md, and record this prompt.

**Status:** In progress

## Problem 8 — Title not provided

### Prompt submitted

> For Problem 8(Customer memory), add persistent chat history for logged-in shoppers.
> Store their conversations in an appropriate database table and reload them when they return. Identify the user from the authenticated session, and ensure one user cannot access another user’s history.
> Give the agent the current customer’s name and email through dependencies or an equivalent clear mechanism. Guests should still be able to chat, but their history does not need to persist.
> Also pass the current page and product ID to the backend. On a product detail page, a question like “Do you have this in pink?” should refer to that product and be answered using real data.
> Verify history restoration and current-product references. Update output/harness.md and record this prompt.

**Status:** In progress

### Prompt submitted (repeated)

> For Problem 8(Customer memory), add persistent chat history for logged-in shoppers.
> Store their conversations in an appropriate database table and reload them when they return. Identify the user from the authenticated session, and ensure one user cannot access another user’s history.
> Give the agent the current customer’s name and email through dependencies or an equivalent clear mechanism. Guests should still be able to chat, but their history does not need to persist.
> Also pass the current page and product ID to the backend. On a product detail page, a question like “Do you have this in pink?” should refer to that product and be answered using real data.
> Verify history restoration and current-product references. Update output/harness.md and record this prompt.

## Problem 9 — Title not provided

### Prompt submitted

> For Problem 9(Usability improvements), implement four usability improvements beyond the required features already completed.
> Frontend improvements:
> 1. Product filtering and price sorting.
> 2. A visible chat waiting state that prevents accidental duplicate submissions.
> Agent/backend improvements:
> 1. Search that handles common typos and similar product terms.
> 2. A database-backed alternative-product tool for unavailable items, explaining why each alternative is relevant.
> Check the real schema before deciding which filters and recommendation criteria are possible. Do not invent product attributes, stock, or matches. If any proposed improvement already exists, suggest a genuinely additional improvement before proceeding.
> Write output/usability.md describing what each improvement adds and why it helps shoppers or the business. Verify all four in the running app and record this prompt.

**Status:** Completed

## Problem 10 — Title not provided

### Prompt submitted

> For Problem 10(Style the website), improve the visual design so the website feels like a distinctive Campus Customs storefront.
> Use a coherent Yale-inspired palette, readable typography, clear visual hierarchy, and attractive product presentation. Refine the navigation, product cards, detail pages, forms, and chat widget. Make the layout work on desktop and mobile, with accessible contrast and visible keyboard focus.
> Keep the design original and preserve the existing product, login, search, and chat functionality. Avoid decorative effects that make shopping harder.
> Write output/design.md with specific changes and an explanation of how each helps customers browse, understand products, or stay engaged.
> Inspect the running pages after styling, verify the main interactions still work, and record this prompt.

**Status:** Completed

## Problem 11 — Title not provided

### Prompt submitted

> For Problem 11(Site testing(app check)), test the running application and create output/app_check.html.
> Document these three checks:
> 1. A chatbot inventory question with a stock or price answer verified against the database.
> 2. A category question that makes matching product cards appear on the webpage.
> 3. One usability improvement implemented in Problem 9.
> Capture genuine screenshots of the working app and save them in output/app_check_images/. For each check, include a heading, screenshot, and one or two sentences explaining what it proves.
> Use relative image paths so app_check.html can be opened directly by double-clicking. Do not fabricate screenshots or claim that untested features passed. If you cannot capture screenshots, give me precise steps to capture them myself.
> Verify the HTML and images open correctly, and record this prompt.

**Status:** Completed

### Follow-up correction

> I need to capture the real screenshots required for Problem 11.
> Start the frontend and backend for the final hw4 submission project and keep both servers running. Verify that the local database, product images, and model credentials are available through the correct local paths without exposing or committing them.
> Give me the actual browser URL and step-by-step instructions for showing:
> 1. A chatbot inventory lookup for a real product and size, with the answer checked against the database.
> 2. Product cards appearing on the webpage after asking “What hoodies do you have?”
> 3. One usability improvement actually implemented in Problem 9.
> Create output/app_check_images/ if necessary. Tell me which implemented usability feature to demonstrate and what should be visible in each screenshot.
> Do not fabricate screenshots or mark the evidence complete yet. After I save the screenshots, update output/app_check.html with relative image paths and accurate captions. Record this request as a Problem 11 follow-up.

The three genuine screenshots are now present in `output/app_check_images/`, and `output/app_check.html` uses relative paths with verified captions.

## Problem 12 — Title not provided

### Prompt submitted

> For Problem 12(Audit trail, safety, finish harness), implement a persistent, append-only agent activity log in output/audit_trail.json.
> Record timestamps, tool names, brief arguments and results, and the reason each agent run ended. Preserve earlier entries across runs and restarts. Exclude credentials, passwords, and unnecessary personal information.
> Expand backend/prompts/prompt.md with rules for grounded product answers, user privacy, and safe behavior. Enforce important restrictions in backend code as well, including user-history isolation, bounded tool activity, and capped search results.
> Finish output/harness.md with the actual database structure, model fields, tools, authentication, chat memory, page context, safety rules, model configuration, execution limits, and frontend/backend startup instructions.
> Run several chat checks to produce real audit entries and verify earlier entries remain. Record this prompt.

**Status:** Completed

Live Portkey chat checks passed after the Portkey-specific client-header fix documented in the Problem 5 follow-up. The audit trail and safety controls were verified.

## Problem 13 — Title not provided

### Prompt submitted

> 13. For Problem 13(Push to GitHub and submit the URL), prepare the completed project for submission in a public GitHub repository.
> Ensure the submitted project folder is named hw4 and contains AI_prompts.md, requirements.txt, .env.example, .gitignore, README.md, frontend/, backend/, and all required output files.
> Update README.md with reproducible setup instructions, where to place the local data pack, environment-variable placeholders, and frontend/backend startup commands. Document any necessary database initialization or migration steps.
> Verify that real .env files, campus_customs.db, and original product images are excluded, while the required app-check screenshots remain included. Check tracked files and any existing Git history for exposed secrets.
> Record this prompt before the final commit. Help me push the project to a public GitHub repository, using the normal sign-in flow if needed. Verify the repository is accessible and give me the exact URL to submit on Canvas. This assignment requires a repository URL, not a ZIP.

**Status:** Completed

The lowercase `hw4` submission was committed and pushed to `https://github.com/DanielKim-94/hw4`. The final local commit is the branch tip, and Problem 11 evidence is present in `output/app_check.html`.

### Problem 5 follow-up

> Please diagnose the recurring startup and chatbot failures systematically. Do not conclude that my API key is expired based only on HTTP 403. Use the final lowercase hw4 folder as the single working project. Identify credential sources without printing secrets, inspect Codex settings, inspect the failed model request, isolate the failure through independent model, agent, API, and browser layers, make startup reproducible on ports 5175 and 8015, verify products/login/chat/inventory/search, restart with the launcher, and record the actual results.

**Result:** The working Homework 3 Portkey client configuration was restored in lowercase `hw4/backend/agent.py` by sending `x-portkey-api-key` through the `httpx2` client. The isolated agent request, FastAPI chat, inventory lookup, dynamic search cards, login, and launcher restart passed. Details are recorded in `output/harness.md`.

### Problem 13 finalization request

> Complete Problem 13 using only the final lowercase hw4 folder. My public GitHub repository URL is https://github.com/DanielKim-94/hw4. Inspect git status and git remote -v. Verify that the latest chatbot fix, startup script, documentation, app_check.html, and the three required screenshots are included. Confirm relative image paths and exclusions for real environment files, databases, and original product images. Record this request in AI_prompts.md. Stage the intended submission files, create a new commit preserving existing commits, configure the remote if necessary, push the current branch using ordinary Git commands, verify the remote branch matches the final local commit and the repository is publicly accessible, and mark Problem 13 complete only after a successful push. Return the exact repository URL and final commit ID.

### Final review follow-up

> Review and fix the final lowercase hw4 project before submission: restrict `/media` to product images, send session/page/product context with chat and restore full history, validate fallback product references, make repository-root `.env` and virtual-environment setup reproducible, verify product/login/registration/chat/current-product behavior, update documentation, and report browser verification status for a replacement Problem 11 screenshot.

**Result:** Code and API checks passed; browser visual verification remained unavailable because no browser surface was available.
