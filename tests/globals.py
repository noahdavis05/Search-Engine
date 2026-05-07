HTML_CONTENT1 = """
    <div class="container">
        <h3>Page Title</h3> 
        
        <div class="quote" itemscope="" itemtype="">
            <span class="text" itemprop="text">
                “This is a quote”
            </span>
            <span>by <small class="author" itemprop="author">Noah Davis</small>
                <a href="/author/Noah-Davis">(about)</a>
            </span>
            <div class="tags">
                Tags:
                <a class="tag" href="/tag">tag</a>
            </div>
        </div>
    </div>
"""

HTML_CONTENT2 = """
    <div class="container">
        <h3>Page Title</h3> 
        
        <div class="quote" itemscope="" itemtype="">
            <span class="text" itemprop="text">
                “This is a quote”
            </span>
            <span>by <small class="author" itemprop="author">Noah Davis</small>
                <a href="/author/Noah-Davis">(about)</a>
            </span>
            <div class="tags">
                Tags:
                <a class="tag" href="/tag">tag</a>
            </div>
        </div>
        <div class="quote" itemscope="" itemtype="">
            <span class="text" itemprop="text">
                “This is another quote”
            </span>
            <span>by <small class="author" itemprop="author">Noah Davis</small>
                <a href="/author/Noah-Davis">(about)</a>
            </span>
            <div class="tags">
                Tags:
                <a class="tag" href="/tag">tag</a>
            </div>
        </div>
    </div>
"""

HTML_CONTENT3 = """
    <div class="container">       
        
        <div class="quote" itemscope="" itemtype="">
            <span class="text" itemprop="text">
                “This is a quote”
            </span>
            <span>by <small class="author" itemprop="author">Noah Davis</small>
                <a href="/author/Noah-Davis">(about)</a>
            </span>
            <div class="tags">
                Tags:
                <a class="tag" href="/tag">tag</a>
            </div>
        </div>
    </div>
"""

HTML_CONTENT4 = """
    <div class="container">
        <h3>Page Title</h3> 
        
        <div class="quote" itemscope="" itemtype="">
            <span>by <small class="author" itemprop="author">Noah Davis</small>
                <a href="/author/Noah-Davis">(about)</a>
            </span>
            <div class="tags">
                Tags:
                <a class="tag" href="/tag">tag</a>
            </div>
        </div>
    </div>
"""

HTML_CONTENT5 = """
    <div class="container">
        <h3>Page Title</h3> 
        
        <div class="quote" itemscope="" itemtype="">
            <span class="text" itemprop="text">
                “This is a quote”
            </span>
            <div class="tags">
                Tags:
                <a class="tag" href="/tag">tag</a>
            </div>
        </div>
    </div>
"""

HTML_CONTENT6 = """
    <div class="container">
        <h3>Page Title</h3> 
        
        <div class="quote" itemscope="" itemtype="">
            <span class="text" itemprop="text">
                “This is a quote”
            </span>
            <span>by <small class="author" itemprop="author">Noah Davis</small>
                <a href="/author/Noah-Davis">(about)</a>
            </span>
        </div>
    </div>
"""

HTML_CONTENT7 = """
    <div class="container">
        <h3>Author Profile</h3>
        <div class="author-details">
            Noah Davis wrote this test.
        </div>
        <div class="author-born-date">January 01, 1990</div>
    </div>
"""


FULL_SITE_HOME = """
    <div class="container">
        <h3>Page Title</h3> 
        
        <div class="quote" itemscope="" itemtype="">
            <span class="text" itemprop="text">
                “This is a quote”
            </span>
            <span>by <small class="author" itemprop="author">Noah Davis</small>
                <a href="/author/Noah-Davis">(about)</a>
            </span>
            <div class="tags">
                Tags:
                <a class="tag" href="/tag">tag</a>
            </div>
        </div>
    </div>
"""

FULL_SITE_AUTHOR = """
    <h3>Noah Davis</h3>
"""

FULL_SITE_TAG_TAG = """
    <div class="container">
        <h3>Tag Quotes</h3> 
        
        <div class="quote" itemscope="" itemtype="">
            <span class="text" itemprop="text">
                “This is a quote about tag”
            </span>
            <span>by <small class="author" itemprop="author">Noah Davis</small>
                <a href="/author/Noah-Davis">(about)</a>
            </span>
            <div class="tags">
                Tags:
                <a class="tag" href="/tag">tag</a>
            </div>
        </div>
        <div class="quote" itemscope="" itemtype="">
            <span class="text" itemprop="text">
                “This is another quote about tag”
            </span>
            <span>by <small class="author" itemprop="author">Noah Davis</small>
                <a href="/author/Noah-Davis">(about)</a>
            </span>
            <div class="tags">
                Tags:
                <-- This tag ensures that the crawler never leaves the website -->
                <a class="tag" href="https://www.bbc.co.uk">tag</a>
            </div>
        </div>
    </div>

"""

SEARCH_PLAIN_DATA = {
    "https://example.com/search": [
        "python", "search", "engine", "is", "fast", "and", "python", "is", "simple", "code"
    ],
    "https://example.com/about": [
        "noah", "davis", "is", "the", "author", "of", "the", "python", "search", "engine"
    ],
    "https://example.com/docs": [
        "learn", "how", "to", "code", "a", "python", "crawler", "and", "search", "engine"
    ]
}

SEARCH_INDEXED_DATA = {
    "python": {
        "https://example.com/search": [0, 6],
        "https://example.com/about": [7],
        "https://example.com/docs": [5]
    },
    "search": {
        "https://example.com/search": [1],
        "https://example.com/about": [8],
        "https://example.com/docs": [8]
    },
    "engine": {
        "https://example.com/search": [2],
        "https://example.com/about": [9],
        "https://example.com/docs": [9]
    },
    "is": {
        "https://example.com/search": [3, 7],
        "https://example.com/about": [2]
    },
    "fast": {
        "https://example.com/search": [4]
    },
    "and": {
        "https://example.com/search": [5],
        "https://example.com/docs": [7]
    },
    "simple": {
        "https://example.com/search": [8]
    },
    "code": {
        "https://example.com/search": [9],
        "https://example.com/docs": [3]
    },
    "noah": {
        "https://example.com/about": [0]
    },
    "davis": {
        "https://example.com/about": [1]
    },
    "the": {
        "https://example.com/about": [3, 6]
    },
    "author": {
        "https://example.com/about": [4]
    },
    "of": {
        "https://example.com/about": [5]
    },
    "learn": {
        "https://example.com/docs": [0]
    },
    "how": {
        "https://example.com/docs": [1]
    },
    "to": {
        "https://example.com/docs": [2]
    },
    "a": {
        "https://example.com/docs": [4]
    },
    "crawler": {
        "https://example.com/docs": [6]
    }
}