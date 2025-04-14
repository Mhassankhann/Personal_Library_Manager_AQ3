import streamlit as st
import json
import os

# Data file for library
data_file = 'library.txt'

# Load existing data
def load_data():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

# Save data to file
def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file)

def main():
    st.set_page_config(page_title="📚 Personal Library Manager", page_icon="📚", layout="wide")

    # Add custom styles for modern design
    st.markdown("""
    <style>
    body {
        background-color: #f4f6f9;
        color: #2c3e50;
        font-family: 'Roboto', sans-serif;
    }
    .sidebar {
        background-color: #34495e;
        padding-top: 20px;
        font-size: 18px;
        color: #ecf0f1;
    }
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 12px;
        padding: 12px 25px;
        font-weight: bold;
        transition: transform 0.3s ease, background-color 0.3s ease;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.15);
    }
    .stButton>button:hover {
        background-color: #2980b9;
        transform: translateY(-4px);
    }
    .stTextInput input {
        background-color: #ecf0f1;
        color: #2c3e50;
        border: 2px solid #bdc3c7;
        border-radius: 12px;
        padding: 12px;
        font-size: 16px;
    }
    .stTextInput input:focus {
        border-color: #3498db;
    }
    .card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        margin: 10px;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0px 6px 16px rgba(0, 0, 0, 0.15);
    }
    .book-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #3498db;
    }
    .book-details {
        color: #7f8c8d;
        font-size: 1rem;
        margin-bottom: 12px;
    }
    .book-status {
        font-weight: bold;
        color: #2ecc71;
    }
    .book-button {
        background-color: #3498db;
        border-radius: 8px;
        padding: 8px 15px;
        color: white;
        text-align: center;
        cursor: pointer;
        margin-top: 10px;
        transition: background-color 0.3s ease;
    }
    .book-button:hover {
        background-color: #2980b9;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("📚 Personal Library Manager")
    st.markdown("""
    **Manage your personal library. Add, remove, search, and view your books with ease.**
    """)

    data = load_data()

    # Sidebar menu
    menu = ['Add a book', 'Remove a book', 'Search for a book', 'Display all books', 'Display statistics', 'Recently Added Books']
    
    # Custom sidebar with logo and user name
    st.sidebar.image("https://via.placeholder.com/150x50.png?text=Library+Logo", width=150)  # Placeholder logo
    st.sidebar.markdown('### **Muhammad Hassan khan**')
    choice = st.sidebar.selectbox('Menu', menu)

    # Add a book section
    if choice == 'Add a book':
        st.subheader('📚 Add a New Book')
        title = st.text_input('Title')
        author = st.text_input('Author')
        year = st.text_input('Year')
        genre = st.text_input('Genre')
        read = st.checkbox('Have you read the book?')

        if st.button('Add Book'):
            if title and author and year and genre:
                new_book = {'title': title, 'author': author, 'year': year, 'genre': genre, 'read': read}
                data.append(new_book)
                save_data(data)
                st.success(f'Book "{title}" added successfully!')
            else:
                st.error("Please fill out all fields!")

    # Remove a book section
    elif choice == 'Remove a book':
        st.subheader('🗑️ Remove a Book')
        titles = [book['title'] for book in data]
        title = st.selectbox('Select a book to remove', titles)

        if st.button('Remove Book'):
            data = [book for book in data if book['title'] != title]
            save_data(data)
            st.success(f'Book "{title}" removed successfully!')

    # Search for a book section
    elif choice == 'Search for a book':
        st.subheader('🔍 Search for a Book')
        title = st.text_input('Enter book title')

        if st.button('Search'):
            found = [book for book in data if title.lower() in book['title'].lower()]
            if found:
                for book in found:
                    st.json(book)
            else:
                st.error(f'No books found with the title "{title}"!')

    # Display all books section
    elif choice == 'Display all books':
        st.subheader('📚 All Books in Your Library')
        if data:
            for book in data:
                st.markdown(f"""
                <div class="card">
                    <div class="book-title">{book['title']}</div>
                    <div class="book-details">by {book['author']} ({book['year']})</div>
                    <div class="book-details">Genre: {book['genre']}</div>
                    <div class="book-status">Status: {'Read' if book['read'] else 'Unread'}</div>
                    <div class="book-button">Details</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info('No books found!')

    # Library Statistics section
    elif choice == 'Display statistics':
        st.subheader('📊 Library Statistics')
        total_books = len(data)
        total_read = len([book for book in data if book['read']])
        percentage_read = (total_read / total_books) * 100 if total_books > 0 else 0
        st.write(f'Total books: {total_books}')
        st.write(f'Percentage read: {percentage_read:.2f}%')

    # Recently Added Books section
    elif choice == 'Recently Added Books':
        st.subheader('✨ Recently Added Books')
        recent_books = data[-2:] if len(data) >= 2 else data  # Show the last 2 books or fewer
        if recent_books:
            for book in recent_books:
                st.markdown(f"""
                    <div class="card">
                        <div class="book-title">{book['title']}</div>
                        <div class="book-details">by {book['author']} ({book['year']})</div>
                        <div class="book-details">Genre: {book['genre']}</div>
                        <div class="book-status">Status: {'Read' if book['read'] else 'Unread'}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info('No recently added books to display!')

    # Footer section
    st.markdown('---')
    st.markdown('👨‍💻 **Created by Muhammad Hassan Khan**')

if __name__ == '__main__':
    main()
