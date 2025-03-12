import streamlit as st
import pandas as pd

# Dark Mode Toggle
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Default to dark mode

def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode  # Toggle the dark mode state

# Custom CSS for Dark and Light Mode
dark_mode_css = """
    <style>
        body {
            background-color: #1e1e1e;
            color: #E0E0E0;
            font-family: 'Arial', sans-serif;
        }
        .main {
            background-color: #222222;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3);
        }
        h1, h2, h3 {
            color: #FFCC00;
        }
        .stButton>button {
            background-color: #444444;
            color: #E0E0E0;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #555555;
            transform: scale(1.05);
        }
        /* Fixing Input & Select Colors */
        .stTextInput input, .stSelectbox select {
            background-color: white;
            color: black !important;  /* White text for dark mode */
            border: 2px solid #FFD700;
        }
    </style>
"""

light_mode_css = """
    <style>
        body {
            background-color: #f5f5f5;
            color: #000;
            font-family: 'Arial', sans-serif;
        }
        .main {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3 {
            color: #333;
        }
        .stButton>button {
            background-color: #dddddd;
            color: #000;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #bbbbbb;
            transform: scale(1.05);
        }
        /* Fixing Input & Select Colors */
        .stTextInput input, .stSelectbox select {
            background-color: #ffffff;
            color: black !important; /* Black text for light mode */
            border: 2px solid #555;
        }
    </style>
"""

# Apply the correct CSS based on dark mode
st.markdown(dark_mode_css if st.session_state.dark_mode else light_mode_css, unsafe_allow_html=True)

# Toggle Button for Dark Mode
st.sidebar.button("🌙 Toggle Dark Mode" if st.session_state.dark_mode else "☀️ Toggle Light Mode", on_click=toggle_dark_mode)

# Initialize library data
if 'books' not in st.session_state:
    st.session_state.books = pd.DataFrame(columns=["Title", "Author", "Year", "Status", "Genre", "Language", "Rating"])

# Book functions
def add_book(title, author, year, status, genre, language, rating):
    new_book = pd.DataFrame([[title, author, year, status, genre, language, rating]], 
                            columns=["Title", "Author", "Year", "Status", "Genre", "Language", "Rating"])
    st.session_state.books = pd.concat([st.session_state.books, new_book], ignore_index=True)

def remove_book(title):
    st.session_state.books = st.session_state.books[st.session_state.books['Title'] != title]

def edit_book(old_title, new_title, new_author, new_year, new_status, new_genre, new_language, new_rating):
    book_index = st.session_state.books[st.session_state.books['Title'] == old_title].index  # Find index of book to edit
    if len(book_index) > 0:
        st.session_state.books.at[book_index[0], 'Title'] = new_title
        st.session_state.books.at[book_index[0], 'Author'] = new_author
        st.session_state.books.at[book_index[0], 'Year'] = new_year
        st.session_state.books.at[book_index[0], 'Status'] = new_status
        st.session_state.books.at[book_index[0], 'Genre'] = new_genre
        st.session_state.books.at[book_index[0], 'Language'] = new_language
        st.session_state.books.at[book_index[0], 'Rating'] = new_rating
        st.success(f"✅ Book **'{new_title}'** updated successfully!")
    else:
        st.error("❌ Book not found.")

def search_books(query):
    return st.session_state.books[st.session_state.books['Title'].str.contains(query, case=False) |
                                   st.session_state.books['Author'].str.contains(query, case=False)]

def display_stats():
    total_books = len(st.session_state.books)
    read_books = len(st.session_state.books[st.session_state.books['Status'] == 'Read'])
    read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0

    st.write(f"📚 Total Books: **{total_books}**")
    st.write(f"✅ Read Books: **{read_books}** ({read_percentage:.2f}%)")

# Book Shelf - Categorization by Genre
def display_books_by_genre():
    genre_filter = st.selectbox("📚 Select Genre to Display", st.session_state.books['Genre'].unique())  # Genre filter
    filtered_books = st.session_state.books[st.session_state.books['Genre'] == genre_filter]
    if not filtered_books.empty:
        for _, row in filtered_books.iterrows():
            st.markdown(f"📖 **{row['Title']}**")
            st.write(f"✍️ Author: {row['Author']}")
            st.write(f"📅 Year: {row['Year']}")
            st.write(f"📌 Status: {row['Status']}")
            st.write(f"⭐ Rating: {row['Rating']}")
            st.markdown("---")
    else:
        st.write(f"❌ No books found in the **{genre_filter}** genre.")

# Book Recommendation - Based on Rating
def recommend_books():
    recommended_books = st.session_state.books[st.session_state.books['Rating'] >= 4]  # Filter books with rating >= 4
    if not recommended_books.empty:
        for _, row in recommended_books.iterrows():
            st.markdown(f"📖 **{row['Title']}**")
            st.write(f"✍️ Author: {row['Author']}")
            st.write(f"⭐ Rating: {row['Rating']}")
            st.markdown("---")
    else:
        st.write("❌ No recommended books based on rating.")

# Save Library to CSV
def save_library_to_csv():
    st.session_state.books.to_csv("library.csv", index=False)
    st.success("✅ Library saved to CSV successfully!")

# Streamlit UI
def library_app():
    st.title("📚 Personal Library Manager")
    
    menu = ["🏠 Home", "➕ Add a Book", "❌ Remove a Book", "✏️ Edit a Book", "🔍 Search for a Book", 
            "📊 Display Stats", "📚 View Books by Genre", "📖 Book Recommendations", "💾 Save Library", "🚪 Exit"]
    choice = st.sidebar.selectbox("📌 Menu", menu)

    if choice == "🏠 Home":
        st.markdown("### 📖 Welcome to your Personal Library!")
        st.write("Manage your books effortlessly!")

    elif choice == "➕ Add a Book":
        st.markdown("### ➕ Add a New Book")
        title = st.text_input("📕 Book Title")
        author = st.text_input("✍️ Author")
        year = st.text_input("📅 Year")
        status = st.selectbox("📌 Status", ["Unread", "Read"])
        genre = st.text_input("📚 Genre (e.g. Fiction, Non-Fiction, Fantasy)")
        language = st.text_input("🌍 Language (e.g. English, Spanish)")
        rating = st.slider("⭐ Rating", min_value=1, max_value=5, step=1)

        if st.button("✅ Add Book"):
            if title and author and year and genre and language:
                add_book(title, author, year, status, genre, language, rating)
                st.success(f"✅ Book **'{title}'** added successfully!")
            else:
                st.error("❌ Please provide all details to add a book.")

    elif choice == "❌ Remove a Book":
        st.markdown("### ❌ Remove a Book")
        title = st.text_input("Enter the Title of the Book to Remove")

        if st.button("🗑 Remove Book"):
            if title in st.session_state.books['Title'].values:
                remove_book(title)
                st.success(f"✅ Book **'{title}'** removed successfully!")
            else:
                st.error("❌ Book not found.")

    elif choice == "✏️ Edit a Book":
        st.markdown("### ✏️ Edit Book Details")
        old_title = st.text_input("Enter the Title of the Book to Edit")
        new_title = st.text_input("New Book Title")
        new_author = st.text_input("New Author")
        new_year = st.text_input("New Year")
        new_status = st.selectbox("New Status", ["Unread", "Read"])
        new_genre = st.text_input("New Genre (e.g. Fiction, Non-Fiction, Fantasy)")
        new_language = st.text_input("New Language (e.g. English, Spanish)")
        new_rating = st.slider("New Rating", min_value=1, max_value=5, step=1)

        if st.button("✅ Update Book"):
            if old_title and new_title and new_author and new_year and new_genre and new_language:
                edit_book(old_title, new_title, new_author, new_year, new_status, new_genre, new_language, new_rating)
            else:
                st.error("❌ Please provide all details to edit a book.")

    elif choice == "🔍 Search for a Book":
        st.markdown("### 🔍 Search for a Book")
        query = st.text_input("Enter Book Title or Author to Search")

        if query:
            search_result = search_books(query)
            if not search_result.empty:
                for _, row in search_result.iterrows():
                    st.markdown(f"📖 **{row['Title']}**")
                    st.write(f"✍️ Author: {row['Author']}")
                    st.write(f"📅 Year: {row['Year']}")
                    st.write(f"📌 Status: {row['Status']}")
                    st.write(f"📚 Genre: {row['Genre']}")
                    st.write(f"🌍 Language: {row['Language']}")
                    st.write(f"⭐ Rating: {row['Rating']}")
                    st.markdown("---")
            else:
                st.write("❌ No books found matching your search.")

    elif choice == "📊 Display Stats":
        st.markdown("### 📊 Library Stats")
        display_stats()

    elif choice == "📚 View Books by Genre":
        st.markdown("### 📚 View Books by Genre")
        display_books_by_genre()

    elif choice == "📖 Book Recommendations":
        st.markdown("### 📖 Book Recommendations")
        recommend_books()

    elif choice == "💾 Save Library":
        st.markdown("### 💾 Save Library to CSV")
        save_library_to_csv()

    elif choice == "🚪 Exit":
        st.write("👋 Exiting... Thank you for using the Library Manager!")
        st.stop()

if __name__ == "__main__":
    with st.container():
        library_app()
