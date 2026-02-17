import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "quotes.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'general'
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM quotes")
    if cursor.fetchone()[0] == 0:
        seed_quotes(cursor)

    conn.commit()
    conn.close()


def seed_quotes(cursor):
    quotes = [
        ("The only way to do great work is to love what you do.", "Steve Jobs", "inspiration"),
        ("Innovation distinguishes between a leader and a follower.", "Steve Jobs", "innovation"),
        ("Stay hungry, stay foolish.", "Steve Jobs", "motivation"),
        ("Life is what happens when you're busy making other plans.", "John Lennon", "life"),
        ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt", "dreams"),
        ("It is during our darkest moments that we must focus to see the light.", "Aristotle", "perseverance"),
        ("The only impossible journey is the one you never begin.", "Tony Robbins", "motivation"),
        ("In the middle of every difficulty lies opportunity.", "Albert Einstein", "perseverance"),
        ("Imagination is more important than knowledge.", "Albert Einstein", "creativity"),
        ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb", "wisdom"),
        ("Do what you can, with what you have, where you are.", "Theodore Roosevelt", "motivation"),
        ("Everything you've ever wanted is on the other side of fear.", "George Addair", "courage"),
        ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill", "perseverance"),
        ("Believe you can and you're halfway there.", "Theodore Roosevelt", "motivation"),
        ("The mind is everything. What you think you become.", "Buddha", "wisdom"),
        ("Strive not to be a success, but rather to be of value.", "Albert Einstein", "wisdom"),
        ("The best revenge is massive success.", "Frank Sinatra", "success"),
        ("I have not failed. I've just found 10,000 ways that won't work.", "Thomas Edison", "perseverance"),
        ("A person who never made a mistake never tried anything new.", "Albert Einstein", "courage"),
        ("The only limit to our realization of tomorrow will be our doubts of today.", "Franklin D. Roosevelt", "motivation"),
        ("What you get by achieving your goals is not as important as what you become by achieving your goals.", "Zig Ziglar", "growth"),
        ("You miss 100% of the shots you don't take.", "Wayne Gretzky", "courage"),
        ("Whether you think you can or you think you can't, you're right.", "Henry Ford", "mindset"),
        ("The purpose of our lives is to be happy.", "Dalai Lama", "life"),
        ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson", "perseverance"),
        ("Simplicity is the ultimate sophistication.", "Leonardo da Vinci", "creativity"),
        ("If you want to lift yourself up, lift up someone else.", "Booker T. Washington", "wisdom"),
        ("The greatest glory in living lies not in never falling, but in rising every time we fall.", "Nelson Mandela", "perseverance"),
        ("Your time is limited, so don't waste it living someone else's life.", "Steve Jobs", "life"),
        ("If you look at what you have in life, you'll always have more.", "Oprah Winfrey", "gratitude"),
        ("The way to get started is to quit talking and begin doing.", "Walt Disney", "motivation"),
        ("Don't judge each day by the harvest you reap but by the seeds that you plant.", "Robert Louis Stevenson", "wisdom"),
        ("It always seems impossible until it's done.", "Nelson Mandela", "perseverance"),
        ("What lies behind us and what lies before us are tiny matters compared to what lies within us.", "Ralph Waldo Emerson", "wisdom"),
        ("Happiness is not something ready-made. It comes from your own actions.", "Dalai Lama", "happiness"),
        ("Act as if what you do makes a difference. It does.", "William James", "motivation"),
        ("The secret of getting ahead is getting started.", "Mark Twain", "motivation"),
        ("It does not matter how slowly you go as long as you do not stop.", "Confucius", "perseverance"),
        ("Everything has beauty, but not everyone sees it.", "Confucius", "wisdom"),
        ("Life is really simple, but we insist on making it complicated.", "Confucius", "life"),
        ("The best way to predict the future is to create it.", "Peter Drucker", "innovation"),
        ("Turn your wounds into wisdom.", "Oprah Winfrey", "growth"),
        ("We become what we think about most of the time.", "Earl Nightingale", "mindset"),
        ("Creativity is intelligence having fun.", "Albert Einstein", "creativity"),
        ("You must be the change you wish to see in the world.", "Mahatma Gandhi", "wisdom"),
        ("The only person you are destined to become is the person you decide to be.", "Ralph Waldo Emerson", "growth"),
        ("Go confidently in the direction of your dreams. Live the life you have imagined.", "Henry David Thoreau", "dreams"),
        ("When one door of happiness closes, another opens.", "Helen Keller", "happiness"),
        ("The power of imagination makes us infinite.", "John Muir", "creativity"),
        ("Not how long, but how well you have lived is the main thing.", "Seneca", "life"),
    ]

    cursor.executemany(
        "INSERT INTO quotes (text, author, category) VALUES (?, ?, ?)",
        quotes,
    )
