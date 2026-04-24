"""
Custom management command: python manage.py seed_data

Creates 5 student users and 15 skill posts spread across all categories.
Safe to run multiple times — skips users/skills that already exist.

Run with:
    python manage.py seed_data
Clear and re-seed with:
    python manage.py seed_data --reset
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from skills.models import Skill


# ── Mock users ──────────────────────────────────────────────────────────────
USERS = [
    {"username": "maya_chen",   "email": "maya@campus.edu",   "password": "SkillSwap2024!"},
    {"username": "jake_torres", "email": "jake@campus.edu",   "password": "SkillSwap2024!"},
    {"username": "priya_k",     "email": "priya@campus.edu",  "password": "SkillSwap2024!"},
    {"username": "alex_w",      "email": "alex@campus.edu",   "password": "SkillSwap2024!"},
    {"username": "sofia_d",     "email": "sofia@campus.edu",  "password": "SkillSwap2024!"},
]

# ── Mock skills ─────────────────────────────────────────────────────────────
SKILLS = [
    # ---- Tutoring ----------------------------------------------------------
    {
        "owner":    "maya_chen",
        "title":    "Calculus I & II Tutoring — Exam Rescue",
        "description": (
            "Struggling with limits, derivatives, or integrals? I passed both "
            "Calc I and II with an A and tutored 12 students last semester. "
            "I break down every concept into plain English before touching the "
            "math. We can work through practice problems, review homework, or "
            "do a focused cram session before your exam. Flexible scheduling "
            "including evenings. Available in the library or via Zoom."
        ),
        "category": "tutoring",
        "price":    "20.00",
        "is_free":  False,
        "contact_preference": "discord",
        "is_available": True,
    },
    {
        "owner":    "priya_k",
        "title":    "Spanish Conversation & Grammar (A1–B2)",
        "description": (
            "Native-level Spanish speaker, raised bilingual. I can help with "
            "grammar drills, conversational practice, writing assignments, or "
            "just chatting if you want to get comfortable speaking. Great for "
            "students in Span 101–301 or anyone prepping for a study abroad "
            "semester. Completely free — I just love the language and want "
            "more people to speak it well."
        ),
        "category": "tutoring",
        "price":    None,
        "is_free":  True,
        "contact_preference": "inperson",
        "is_available": True,
    },
    {
        "owner":    "alex_w",
        "title":    "Statistics & Data Analysis Tutoring",
        "description": (
            "Stats making your head spin? I'm a junior in the stats program "
            "and TA for Intro to Probability. I can help with hypothesis "
            "testing, regression, ANOVA, confidence intervals, and reading "
            "output from R or SPSS. I've helped students go from a D to a B+ "
            "in a single month. Bring your problem sets and let's work through "
            "them together."
        ),
        "category": "tutoring",
        "price":    "18.00",
        "is_free":  False,
        "contact_preference": "email",
        "is_available": True,
    },

    # ---- Coding & Tech -----------------------------------------------------
    {
        "owner":    "maya_chen",
        "title":    "Python & Django Help for Beginners",
        "description": (
            "Just finished building a full Django web app and happy to share "
            "what I learned. I can help you understand Python basics, set up a "
            "Django project, build models and views, debug template errors, or "
            "just talk through why something isn't working. Patient, "
            "beginner-friendly, no judgment. Perfect for CS 101 or anyone "
            "doing their first web project."
        ),
        "category": "coding",
        "price":    "15.00",
        "is_free":  False,
        "contact_preference": "discord",
        "is_available": True,
    },
    {
        "owner":    "alex_w",
        "title":    "React & Next.js Frontend Dev Help",
        "description": (
            "Frontend dev with 2 years of React experience and several "
            "deployed Next.js projects. I can help you debug hooks, set up "
            "routing, style with Tailwind, connect to an API, or understand "
            "why your state isn't updating. Also happy to review your project "
            "repo and give structured feedback. Remote sessions via Discord "
            "screenshare."
        ),
        "category": "coding",
        "price":    "22.00",
        "is_free":  False,
        "contact_preference": "discord",
        "is_available": True,
    },
    {
        "owner":    "jake_torres",
        "title":    "Free Git & GitHub Crash Course",
        "description": (
            "Tired of accidentally nuking your project or having no idea what "
            "'detached HEAD' means? I'll walk you through everything: init, "
            "commit, branch, merge, pull requests, and how to recover from "
            "mistakes. One session is usually enough to make it click. Totally "
            "free — every dev should know this stuff and it shouldn't cost you "
            "anything to learn it."
        ),
        "category": "coding",
        "price":    None,
        "is_free":  True,
        "contact_preference": "inperson",
        "is_available": True,
    },

    # ---- Design & Creative -------------------------------------------------
    {
        "owner":    "jake_torres",
        "title":    "Logo & Brand Identity Design",
        "description": (
            "Graphic design student with a focus on brand identity. I'll "
            "create a logo + color palette + font pairing that actually looks "
            "professional. Good for student clubs, startup side projects, "
            "personal portfolios, or anything you want to look polished. "
            "Turnaround is 3–5 days with two rounds of revisions included. "
            "Send me a brief and I'll quote you based on scope."
        ),
        "category": "design",
        "price":    "35.00",
        "is_free":  False,
        "contact_preference": "email",
        "is_available": True,
    },
    {
        "owner":    "sofia_d",
        "title":    "Portrait & Event Photography",
        "description": (
            "Photography major with a Canon R6 and two years of shooting "
            "portraits, club events, and campus life. I can shoot headshots "
            "for your LinkedIn, photos for a club event, or candid lifestyle "
            "shots for social media. Edited gallery delivered within 48 hours. "
            "DM me with your date and I'll check availability. Rates are per "
            "hour of shooting."
        ),
        "category": "design",
        "price":    "40.00",
        "is_free":  False,
        "contact_preference": "phone",
        "is_available": True,
    },

    # ---- Writing & Editing -------------------------------------------------
    {
        "owner":    "priya_k",
        "title":    "Essay Editing & Proofreading",
        "description": (
            "English and Journalism double major. I'll read your essay, "
            "research paper, personal statement, or cover letter and give you "
            "detailed line-by-line feedback on clarity, structure, grammar, "
            "and argument strength. I don't just fix typos — I help you make "
            "your ideas land. 24-hour turnaround for papers under 2,000 words. "
            "Send me your draft and I'll take a look."
        ),
        "category": "writing",
        "price":    "12.00",
        "is_free":  False,
        "contact_preference": "email",
        "is_available": True,
    },
    {
        "owner":    "maya_chen",
        "title":    "Free Cover Letter & Resume Review",
        "description": (
            "Landed internships at two companies last year and happy to pay it "
            "forward. I'll review your resume or cover letter and give honest "
            "feedback on formatting, word choice, and whether it tells a "
            "compelling story. Especially helpful for tech internships and "
            "entry-level roles. Free because good career advice shouldn't be "
            "locked behind a $200/hr career coach."
        ),
        "category": "writing",
        "price":    None,
        "is_free":  True,
        "contact_preference": "email",
        "is_available": True,
    },

    # ---- Music Lessons -----------------------------------------------------
    {
        "owner":    "jake_torres",
        "title":    "Beginner Acoustic Guitar Lessons",
        "description": (
            "Been playing guitar for 8 years and love teaching. I'll start you "
            "from zero — how to hold it, basic chords, strumming patterns — "
            "and get you playing real songs within 2–3 sessions. Bring your "
            "own guitar or borrow mine for the lesson. No music theory required "
            "upfront. We'll go at whatever pace feels right. Offered free "
            "because I just enjoy it."
        ),
        "category": "music",
        "price":    None,
        "is_free":  True,
        "contact_preference": "inperson",
        "is_available": True,
    },
    {
        "owner":    "sofia_d",
        "title":    "Ableton & Music Production Basics",
        "description": (
            "Self-taught producer with 3 years in Ableton Live. I can show you "
            "the DAW layout, how to record and chop samples, basic mixing "
            "concepts, and how to export a track that sounds decent. Great "
            "for anyone who wants to make beats, produce for a campus "
            "organization, or just mess around creatively. Sessions at my "
            "place with my setup — you don't need your own gear."
        ),
        "category": "music",
        "price":    "20.00",
        "is_free":  False,
        "contact_preference": "discord",
        "is_available": True,
    },

    # ---- Fitness & Wellness ------------------------------------------------
    {
        "owner":    "sofia_d",
        "title":    "Beginner Gym Program & Workout Planning",
        "description": (
            "Certified personal trainer (ACE) and kinesiology student. I'll "
            "build you a 4-week beginner program based on your goals — muscle "
            "gain, fat loss, or general fitness — and walk you through every "
            "exercise so you're not just copying strangers at the gym. "
            "One-time session includes the plan plus a form check on your main "
            "lifts. Available at the campus rec center."
        ),
        "category": "fitness",
        "price":    "25.00",
        "is_free":  False,
        "contact_preference": "phone",
        "is_available": True,
    },

    # ---- Moving & Errands --------------------------------------------------
    {
        "owner":    "alex_w",
        "title":    "Moving Help — Boxes, Furniture, Heavy Lifting",
        "description": (
            "Moving into or out of the dorms or an apartment near campus? "
            "I've helped six people move in the last year and I'm fast, "
            "careful with fragile stuff, and I have a car for smaller loads. "
            "Available most weekends. Rate is per hour, with a 2-hour minimum. "
            "Let me know your move date and I'll confirm availability."
        ),
        "category": "moving",
        "price":    "15.00",
        "is_free":  False,
        "contact_preference": "phone",
        "is_available": True,
    },
]


class Command(BaseCommand):
    help = "Seed the database with mock users and skill posts."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete all existing skills and seeded users before re-seeding.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            usernames = [u["username"] for u in USERS]
            deleted, _ = Skill.objects.filter(owner__username__in=usernames).delete()
            User.objects.filter(username__in=usernames).delete()
            self.stdout.write(self.style.WARNING(
                f"Reset: removed {deleted} skills and {len(usernames)} users."
            ))

        # 1. Create users
        user_objects = {}
        for u in USERS:
            obj, created = User.objects.get_or_create(
                username=u["username"],
                defaults={"email": u["email"]},
            )
            if created:
                obj.set_password(u["password"])
                obj.save()
                self.stdout.write(f"  Created user: {u['username']}")
            else:
                self.stdout.write(f"  Skipped (exists): {u['username']}")
            user_objects[u["username"]] = obj

        # 2. Create skills
        created_count = 0
        for s in SKILLS:
            owner = user_objects[s["owner"]]
            # Skip if this user already has a skill with the same title
            if Skill.objects.filter(owner=owner, title=s["title"]).exists():
                self.stdout.write(f"  Skipped (exists): {s['title'][:50]}")
                continue

            Skill.objects.create(
                owner=owner,
                title=s["title"],
                description=s["description"],
                category=s["category"],
                price=s["price"],
                is_free=s["is_free"],
                contact_preference=s["contact_preference"],
                is_available=s["is_available"],
            )
            created_count += 1
            self.stdout.write(f"  Created skill: {s['title'][:50]}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! {created_count} skills created across "
            f"{len(set(s['owner'] for s in SKILLS))} users.\n"
            f"Log in with any seeded account — password is: SkillSwap2024!"
        ))
