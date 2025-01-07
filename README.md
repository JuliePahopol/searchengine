# Web Search Using Database
The Web Search Using Database folder contains a fully functional web search engine implementation that integrates a web crawler, PageRank computation, and a user-facing search interface. The system uses a database to store crawled pages and their metadata, enabling efficient query handling. Below is a detailed description of each file and its purpose.
## Files and Their Descriptions:
### 1. pagerank.py

### Purpose:
Implements the PageRank algorithm using the crawled data stored in the SQLite database to compute the importance of each web page.

### Key Features:

• Connects to the SQLite database (crawled_pages.db) to retrieve URLs and outgoing links.

• Constructs a directed graph of web pages using NetworkX, where nodes represent web pages and edges represent links.

• Calculates the PageRank scores for each page using the NetworkX pagerank() function.

• Updates the database to store the computed PageRank scores for each URL.

## Usage: 
Run this script after the crawler has populated the database to compute and store PageRank scores, which are then used for ranking search results.
### 2. web_spider.py
• Purpose: Crawls the web starting from seed URLs and stores the content and metadata of web pages in the SQLite database.
• Key Features:

• Creates a database table (pages) with fields for URL, content, cleaned content (text only), title, outgoing links, and PageRank.

• Fetches web pages using the requests library and parses them with BeautifulSoup.

• Extracts and stores the page title, text content, and outgoing links.

• Uses a breadth-first search (BFS) approach to explore up to a specified number of pages (max_pages).

• Avoids duplicate crawling by maintaining a visited_pages set.

## Database Schema:
sql
CREATE TABLE IF NOT EXISTS pages ( id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT UNIQUE, content TEXT, cleaned_content TEXT, title TEXT, outgoing_links TEXT, pagerank REAL );

![Screenshot 2025-01-07 204715](https://github.com/user-attachments/assets/40ffa9bc-a4fa-48ff-af6e-c049ddda8eb3)

## Usage:
Modify the seed_urls list to specify starting points and run the script to populate the database.

### 3. websearch.py

• Purpose: Provides a web interface for searching the crawled web pages.
• Key Features:

Built with Flask, a lightweight web framework.

Contains two routes:
▪ /: Displays the search form (websearch.html).
▪ /websearch: Handles search queries and displays results.

Queries the SQLite database for matches in the cleaned_content field based on user input.

Orders search results by PageRank to prioritize more important pages.

Returns matching URLs and their titles, which are displayed using the results.html template.
• Usage: Run this script to start the Flask server and access the search engine via a browser at http://127.0.0.1:5000.
### 4. crawled_pages.db
• Purpose: An SQLite database that stores information about the crawled pages.
•
Structure:
### id: 
Auto-incremented unique identifier.

### url: 
The URL of the page.

• content: The full HTML content of the page.

• cleaned_content: The plain text content of the page (used for searching).

• title: The title of the page.

• outgoing_links: A comma-separated list of outgoing links from the page.

• pagerank: The PageRank score of the page (computed by pagerank.py).

## Static Folder (For Web Interface Design)
### 1. websearch.html
 Purpose: The main search page where users can enter queries.
 Features:
• Simple search form with an input field and a submit button.
• Links to style.css for consistent styling.
### 2. results.html
Purpose: Displays the search results.
Features:

• Shows a list of URLs and titles that match the query.
• Includes a header indicating the query and a styled list of results.
### 3. style.css
• Purpose: Provides styling for the web pages.
• Features:
o
Defines font styles, colors, and layout for the search page and results page.
o
Ensures a clean and user-friendly interface.
# How the System Works
### 1.Web Crawling:
a.
Run web_spider.py to populate the crawled_pages.db database with web page data.
### 2.PageRank Calculation:
a.
Run pagerank.py to compute and store PageRank scores for the crawled pages.
### 3.Search Functionality:
a. Run websearch.py to start the Flask server.
b. Access the search engine in a web browser, enter a query, and view results ranked by relevance and PageRank.
4. Database Structure:
a.All crawled data, including content, metadata, and computed scores, is stored in the crawled_pages.db database for efficient retrieval and ranking.
## Future Improvements
• Enhance Crawler:
  Handle dynamic content using tools like Selenium.
  Respect robots.txt and implement rate limiting.
• Improve Search:
  Add support for advanced queries (e.g., Boolean search).
  Implement snippet generation to show query-relevant parts of the content.
• Optimize Database:
  Use indexing for faster queries.
• UI/UX Enhancements:
   Make the interface responsive and visually appealing.

   
#### This folder demonstrates the integration of web crawling, ranking algorithms, and a search engine interface. It’s a practical foundation for building scalable and sophisticated search solutions.

![Screenshot 2025-01-07 204910](https://github.com/user-attachments/assets/d8332011-b8ef-4059-9bb3-76b225583020)


![Screenshot 2025-01-07 204924](https://github.com/user-attachments/assets/034c1881-3a87-41cb-a62c-b37798eba49a)
