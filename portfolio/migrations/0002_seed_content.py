"""
Seed the portfolio with the 6 rubric-required projects, skills, personal
builds, and experience entries. All content is editable from Django admin.
"""
from django.db import migrations
from django.utils.text import slugify


PROJECTS = [
    {
        "title": "HandyMan Pricing Agent",
        "category": "langchain",
        "featured": True,
        "order": 10,
        "static_image": "media/handyman-terminal.png",
        "image_alt": "HandyMan Pricing Agent terminal output",
        "github_link": "",
        "demo_link": "",
        "one_sentence_summary": (
            "A LangChain agent that reads a handyman company's pricing data and "
            "returns structured quote estimates for incoming customer requests."
        ),
        "business_problem": (
            "Small service businesses lose hours every week answering "
            "pricing questions manually, and inconsistent quoting creates "
            "confusion for both customer and crew. This project connects "
            "AI directly to a real business workflow by turning a live "
            "pricing sheet into fast, structured quote output."
        ),
        "tools_used": (
            "Python, LangChain, Google Gemini, Google Sheets API, JSON parsing, "
            "dotenv, virtual environments"
        ),
        "key_features": (
            "Reads pricing data from a connected Google Sheet\n"
            "Parses customer requests into structured quote payloads\n"
            "Tool-calling agent with pricing, scheduling, and calendar tools\n"
            "Returns clean JSON the rest of a business workflow can consume\n"
            "Secrets isolated in .env so the repo stays safe to share"
        ),
        "role_contribution": (
            "I designed the agent's system prompt, wrote the pricing tool "
            "wrapper around the Sheets API, and stitched the multi-tool "
            "workflow together so the agent could route between quoting, "
            "scheduling, and calendar booking based on intent."
        ),
        "biggest_challenge": (
            "Getting the agent to stop free-styling pricing and instead defer "
            "to the sheet for every quote. The fix was tightening the system "
            "prompt and forcing tool use for any number that touched dollars."
        ),
        "what_i_learned": (
            "Real agent work is mostly tool design and prompt discipline. "
            "The model is the easy part. The seams between the model, the "
            "data source, and the business rules are where the value lives."
        ),
    },
    {
        "title": "Personal Document Brain",
        "category": "n8n",
        "featured": True,
        "order": 20,
        "static_image": "media/n8n-workflow.png",
        "image_alt": "n8n workflow connecting research sources to Obsidian",
        "github_link": "",
        "demo_link": "",
        "one_sentence_summary": (
            "An AI-powered knowledge workflow that turns scattered files, "
            "notes, research, and project materials into an interconnected "
            "Obsidian reference system."
        ),
        "business_problem": (
            "AI tools are powerful but they forget context constantly. I "
            "wanted a system that could preserve what I learn, link ideas "
            "across projects, and turn scattered information into a living "
            "knowledge base instead of a giant disconnected notebook."
        ),
        "tools_used": (
            "n8n, Claude API, JavaScript nodes, Google Drive, Obsidian, "
            "markdown, AI research workflows, automation"
        ),
        "key_features": (
            "Ingests documents, notes, and research from multiple sources\n"
            "Uses Claude to summarize, tag, and cross-link content\n"
            "Writes into Obsidian as connected markdown nodes\n"
            "Builds a graph view that surfaces relationships between ideas\n"
            "Runs on a schedule so the system maintains itself"
        ),
        "role_contribution": (
            "I designed the workflow end to end: source connectors, Claude "
            "prompting strategy, the markdown output schema, and the link "
            "graph that turns isolated notes into a navigable second brain."
        ),
        "biggest_challenge": (
            "Keeping the system from drifting into noise. The fix was strict "
            "templates for every note type and a tagging convention the "
            "agent had to follow before it was allowed to write anything."
        ),
        "what_i_learned": (
            "A second brain is not a bigger notebook. The value is in the "
            "edges between notes, not the notes themselves. Designing for "
            "connection first changes how you build the whole pipeline."
        ),
    },
    {
        "title": "Conversational Chatbot",
        "category": "chatbot",
        "featured": False,
        "order": 30,
        "static_image": "media/chatbot.png",
        "image_alt": "Chatbot conversation",
        "github_link": "",
        "demo_link": "",
        "one_sentence_summary": (
            "A focused conversational AI that demonstrates how a chatbot can "
            "guide users, answer questions, and structure information through "
            "a careful prompt and a clear interface."
        ),
        "business_problem": (
            "Most chatbots either over-promise or wander off topic. The goal "
            "here was to build something disciplined: a small assistant with "
            "a clear scope that stays useful instead of generic."
        ),
        "tools_used": (
            "Python, LangChain, Google Gemini, prompt engineering, dotenv"
        ),
        "key_features": (
            "Tightly scoped system prompt that defines tone and boundaries\n"
            "Clean message loop with conversation memory\n"
            "Falls back gracefully when asked something out of scope\n"
            "Foundation for the optional 'Ask Seth' widget on this site"
        ),
        "role_contribution": (
            "Wrote the chatbot from the prompt outward, iterating until the "
            "agent felt direct, polite, and useful inside its scope."
        ),
        "biggest_challenge": (
            "Keeping personality and clarity in the same prompt. Too much "
            "personality and the bot wanders; too much rigidity and it "
            "feels like a form. The balance came from short, sharp rules."
        ),
        "what_i_learned": (
            "The interface is the prompt. Most of what users feel about a "
            "chatbot is decided in the first paragraph of the system message."
        ),
    },
    {
        "title": "Google AI Studio Media Project",
        "category": "ai_studio",
        "featured": False,
        "order": 40,
        "static_image": "media/google-ai-studio-media.png",
        "image_alt": "Google AI Studio media generation",
        "github_link": "",
        "demo_link": "",
        "one_sentence_summary": (
            "A media generation and prompt-engineering project focused on "
            "using AI to create usable creative assets with stronger visual "
            "consistency."
        ),
        "business_problem": (
            "Creative output for small ventures is expensive and slow. "
            "AuraAnn Skincare and MineralsRx need a steady stream of brand "
            "visuals, product imagery, and content. AI-driven generation "
            "shortens the loop between idea and asset without losing brand "
            "consistency."
        ),
        "tools_used": (
            "Google AI Studio, Gemini, AI image and media generation, "
            "prompt engineering, Canva"
        ),
        "key_features": (
            "Reusable prompt templates for product and lifestyle visuals\n"
            "A consistent visual language across iterations\n"
            "Workflow that pairs generation with light editing in Canva\n"
            "Reduces time from concept to publishable asset"
        ),
        "role_contribution": (
            "Built the prompt library and the generation workflow used for "
            "AuraAnn and MineralsRx content. Iterated on prompts until the "
            "outputs felt on-brand instead of generic AI."
        ),
        "biggest_challenge": (
            "Avoiding the generic 'AI look.' The fix was prompt structure: "
            "lock the brand cues first, then let the model improvise inside "
            "those guardrails."
        ),
        "what_i_learned": (
            "Creative AI is a brand discipline, not a generation problem. "
            "The model can produce anything; the prompt teaches it what to "
            "produce on purpose."
        ),
    },
    {
        "title": "scikit-learn Predictive Model",
        "category": "ml",
        "featured": False,
        "order": 50,
        "static_image": "media/ml-results.png",
        "image_alt": "Machine learning model results",
        "github_link": "",
        "demo_link": "",
        "one_sentence_summary": (
            "A supervised machine learning project using Python and "
            "scikit-learn to train, test, and evaluate a predictive model."
        ),
        "business_problem": (
            "Most business decisions hinge on a forecast of some kind. "
            "This project builds the muscle of going from raw data to a "
            "validated model that can support those decisions."
        ),
        "tools_used": (
            "Python, scikit-learn, pandas, NumPy, train and test split, "
            "model evaluation metrics, matplotlib"
        ),
        "key_features": (
            "Loads and explores the dataset before modeling\n"
            "Trains a baseline model and evaluates with proper metrics\n"
            "Visualizes results and residuals to inspect performance\n"
            "Documents tradeoffs between accuracy and interpretability"
        ),
        "role_contribution": (
            "Built the full pipeline: load, clean, split, train, evaluate. "
            "Compared a few models on the same data to see where each one "
            "earns its keep."
        ),
        "biggest_challenge": (
            "Resisting the urge to chase accuracy. The model that scores "
            "highest on the test set is not always the model you want in "
            "front of a real decision."
        ),
        "what_i_learned": (
            "ML feels like coding but acts like science. The discipline is "
            "in the questions you ask of the data before you fit anything."
        ),
    },
    {
        "title": "Campus SkillSwap",
        "category": "django",
        "featured": True,
        "order": 60,
        "static_image": "media/campus-skillswap.png",
        "image_alt": "Campus SkillSwap home page",
        "github_link": "",
        "demo_link": "/skillswap/",
        "one_sentence_summary": (
            "A campus-focused Django web app where students can post, "
            "browse, and exchange skills."
        ),
        "business_problem": (
            "Students teach each other constantly, but there's no good "
            "way to find someone with a specific skill at the moment you "
            "need them. SkillSwap turns that ad-hoc network into a "
            "browsable marketplace inside one campus."
        ),
        "tools_used": (
            "Python, Django, SQLite, HTML, CSS, Bootstrap, Django auth, "
            "Django admin, Django ORM, custom forms"
        ),
        "key_features": (
            "User authentication with signup, login, and dashboards\n"
            "Post, edit, and delete your own skills with full CRUD\n"
            "Browse skills posted by everyone on campus\n"
            "Per-user dashboard for managing your own listings\n"
            "Django admin for moderating the marketplace"
        ),
        "role_contribution": (
            "Built the full Django app: models, views, forms, templates, "
            "URL routing, auth flow, and the styling layer. Now featured "
            "as a live demo inside this portfolio at /skillswap/."
        ),
        "biggest_challenge": (
            "Getting the auth-protected create and edit flows to feel "
            "natural. The fix was treating each form like its own small "
            "user journey instead of a generic CRUD page."
        ),
        "what_i_learned": (
            "Django rewards small, focused apps. Once the model and URL "
            "shape settle, almost everything else falls into place. The "
            "real work is in the user experience around the data."
        ),
    },
]


SKILLS = [
    # AI and Automation
    ("AI prompting", "ai", 10, "Designing prompts that produce useful, on-brand output"),
    ("LangChain agents", "ai", 20, "Tool-using agents wired to real business data"),
    ("n8n workflows", "ai", 30, "Multi-step automations that connect tools and APIs"),
    ("Claude API", "ai", 40, "Production-grade prompting and orchestration"),
    ("Google Gemini", "ai", 50, "Multimodal AI for content and reasoning tasks"),
    ("Google AI Studio", "ai", 60, "Media generation and rapid prompt iteration"),

    # Full-Stack and Web
    ("Django", "web", 10, "Models, views, templates, auth, and admin"),
    ("Python", "web", 20, "Backend logic, scripting, automation"),
    ("HTML / CSS", "web", 30, "Hand-written, dark-themed, responsive UI"),
    ("Bootstrap", "web", 40, "Used selectively, customized heavily"),
    ("JavaScript", "web", 50, "Light interactivity and animations"),
    ("Whitenoise / Railway / Render", "web", 60, "Static files and deployment"),

    # Machine Learning and Data
    ("scikit-learn", "ml", 10, "Classification, regression, evaluation"),
    ("pandas / NumPy", "ml", 20, "Data wrangling, transforms, analysis"),
    ("Model evaluation", "ml", 30, "Metrics, train and test splits, residuals"),
    ("Google Sheets API", "ml", 40, "Treating sheets as a programmable data source"),

    # Business and Creative Strategy
    ("Venture creation", "biz", 10, "Top 50 in Baylor's New Venture Competition"),
    ("Brand strategy", "biz", 20, "AuraAnn Skincare, MineralsRx, Lyme Revive Foundation"),
    ("AI for creative ops", "biz", 30, "Faster, more consistent content systems"),
    ("Problem solving", "biz", 40, "Across technical and business contexts"),
    ("Systems thinking", "biz", 50, "Designing for the seams between tools"),
    ("Communication", "biz", 60, "Honors College and BIC writing rigor"),
]


PERSONAL_BUILDS = [
    (
        "LymeReviveFoundation.org",
        "A nonprofit education platform built to organize complex Lyme "
        "disease information into a clearer public resource.",
        "https://lymerevivefoundation.org",
        10,
    ),
    (
        "AuraAnnSkincare.com",
        "A skincare venture where I use AI for brand strategy, content, "
        "customer education, and digital growth.",
        "https://auraannskincare.com",
        20,
    ),
    (
        "MineralsRx.com",
        "A wellness product platform where I support product education, "
        "digital systems, and business infrastructure.",
        "https://mineralsrx.com",
        30,
    ),
    (
        "Shopify Business Hub",
        "A custom UI concept that uses Shopify API data to turn store "
        "activity into a more useful internal business dashboard.",
        "",
        40,
    ),
    (
        "AI Research Workflows",
        "Automation systems that research, summarize, organize, and "
        "connect information across projects.",
        "",
        50,
    ),
]


EXPERIENCES = [
    (
        "Founder",
        "AuraAnn Skincare",
        "Waco, TX",
        "2024",
        "",
        "Top 50 — Baylor New Venture Competition\n"
        "Lead brand, product education, and AI-driven content systems\n"
        "Built digital infrastructure across web, social, and customer ops",
        10,
    ),
    (
        "Founder · Operations",
        "Lyme Revive Foundation",
        "Waco, TX",
        "2024",
        "",
        "Built lymerevivefoundation.org as a public education platform\n"
        "Designed n8n + Obsidian research workflow that organizes Lyme "
        "literature into a connected knowledge base\n"
        "Framed all messaging as education, not medical advice",
        20,
    ),
    (
        "Operator",
        "MineralsRx",
        "Remote",
        "2024",
        "",
        "Support product education, digital systems, and business infra\n"
        "Pair AI tools with content workflows for faster iteration",
        30,
    ),
    (
        "Histor",
        "Tau Kappa Epsilon — Baylor Chapter",
        "Waco, TX",
        "2024",
        "2025",
        "Led chapter history work and alumni engagement\n"
        "Built systems for keeping alumni connected to active members",
        40,
    ),
    (
        "Student",
        "Baylor University · Honors College",
        "Waco, TX",
        "Aug 2022",
        "May 2026",
        "MIS and Entrepreneurship and Corporate Innovation\n"
        "Honors College and Baylor Interdisciplinary Core (BIC)\n"
        "Focused coursework in AI, machine learning, Django, and venture work",
        50,
    ),
]


def seed(apps, schema_editor):
    Project = apps.get_model("portfolio", "Project")
    Skill = apps.get_model("portfolio", "Skill")
    PersonalBuild = apps.get_model("portfolio", "PersonalBuild")
    Experience = apps.get_model("portfolio", "Experience")

    for data in PROJECTS:
        slug = slugify(data["title"])[:140]
        Project.objects.update_or_create(slug=slug, defaults={**data, "slug": slug})

    for name, group, order, desc in SKILLS:
        Skill.objects.update_or_create(
            name=name, group=group,
            defaults={"order": order, "description": desc},
        )

    for name, summary, url, order in PERSONAL_BUILDS:
        PersonalBuild.objects.update_or_create(
            name=name,
            defaults={"summary": summary, "url": url, "order": order},
        )

    for role, org, loc, start, end, desc, order in EXPERIENCES:
        Experience.objects.update_or_create(
            role=role, organization=org,
            defaults={
                "location": loc, "start_date": start, "end_date": end,
                "description": desc, "order": order,
            },
        )


def unseed(apps, schema_editor):
    for model_name in ("Project", "Skill", "PersonalBuild", "Experience"):
        apps.get_model("portfolio", model_name).objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0001_initial")]
    operations = [migrations.RunPython(seed, reverse_code=unseed)]
