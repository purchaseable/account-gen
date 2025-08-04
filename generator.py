import random
import csv
from datetime import datetime, timedelta
from faker import Faker
import asyncio
from playwright.async_api import async_playwright

fake = Faker()

def generate_username(niche):
    keywords = {
        "fitness": ["Fit", "Muscle", "Gym", "Lift", "Shred"],
        "motivational": ["Mindset", "Hustle", "Grind", "Inspire", "Rise"],
        "tech": ["Tech", "Gadget", "Code", "Byte", "Nerd"]
    }
    word = random.choice(keywords.get(niche.lower(), ["User"]))
    suffix = random.randint(100, 999)
    return f"{word}{suffix}"

def generate_name(username):
    parts = [word for word in username if word.isalpha()]
    return fake.name()

def generate_birthdate():
    today = datetime.today()
    min_age = 18
    max_age = 50
    delta = timedelta(days=random.randint(min_age*365, max_age*365))
    birthdate = today - delta
    return birthdate.strftime("%Y-%m-%d")

def generate_password():
    return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)

async def create_account(email, proxy, niche):
    username = generate_username(niche)
    name = generate_name(username)
    birthdate = generate_birthdate()
    password = generate_password()
    timestamp = datetime.now().isoformat()

    try:
        async with async_playwright() as p:
            if proxy:
                browser = await p.chromium.launch(proxy={"server": proxy}, headless=True)
            else:
                browser = await p.chromium.launch(headless=True)

            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://example.com/signup")  # replace with real URL

            await page.fill('input[name="email"]', email)
            await page.fill('input[name="username"]', username)
            await page.fill('input[name="name"]', name)
            await page.fill('input[name="birthdate"]', birthdate)
            await page.fill('input[name="password"]', password)
            await page.click('button[type="submit"]')

            await browser.close()

        status = "success"

    except Exception as e:
        status = f"failed: {str(e)}"

        # Save to CSV
        with open("accounts.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([email, proxy, niche, username, name, birthdate, password, timestamp, status])

        return {
            "email": email,
            "username": username,
            "name": name,
            "birthdate": birthdate,
            "password": password,
            "status": status
        }
