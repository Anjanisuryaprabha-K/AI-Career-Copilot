import re
from urllib.parse import quote_plus
from typing import Dict, Any, List, Optional
from datetime import datetime

class LearningSeedService:
    """
    Service responsible for providing and seeding the complete standalone Technical Learning Catalog
    containing 24+ main technologies with rich subtopic sequences and valid YouTube search URLs.
    """

    @staticmethod
    def build_search_url(query: str) -> str:
        clean_query = re.sub(r'[^\w\s\-\+\.#]', '', query).strip()
        encoded = quote_plus(clean_query)
        return f"https://www.youtube.com/results?search_query={encoded}"

    @classmethod
    def get_categories(cls) -> List[Dict[str, Any]]:
        return [
            {"id": "all", "name": "All Categories", "icon": "📚"},
            {"id": "dsa", "name": "DSA & Algorithms", "icon": "🧠"},
            {"id": "languages", "name": "Programming Languages", "icon": "💻"},
            {"id": "web", "name": "Web Development", "icon": "🌐"},
            {"id": "databases", "name": "Databases", "icon": "🗄"},
            {"id": "cs", "name": "Computer Science", "icon": "🖥"},
            {"id": "tools", "name": "Developer Tools", "icon": "🛠"},
            {"id": "cloud", "name": "Cloud & DevOps", "icon": "☁️"},
            {"id": "system_design", "name": "System Design", "icon": "🏗"},
        ]

    @classmethod
    def get_master_catalog(cls) -> List[Dict[str, Any]]:
        """
        Returns master definition of all technical topics, subtopics, and resources.
        No role dependency. Every topic has subtopics with YouTube search URLs.
        """
        s_url = cls.build_search_url

        catalog = [
            # 1. DSA & ALGORITHMS (24 Subtopics)
            {
                "id": "dsa",
                "slug": "dsa",
                "title": "DSA",
                "full_title": "Data Structures & Algorithms",
                "icon": "🧠",
                "category": "DSA & Algorithms",
                "description": "Master Data Structures & Algorithms from fundamentals to advanced interview problem solving.",
                "tags": ["dsa", "algorithms", "data structures", "leetcode", "arrays", "trees", "dp", "graphs"],
                "subtopics": [
                    {"id": "dsa_1", "order": 1, "title": "1. DSA Introduction", "description": "Overview of Data Structures, Algorithms, problem solving paradigms, and classification.", "query": "dsa introduction data structures algorithms tutorial"},
                    {"id": "dsa_2", "order": 2, "title": "2. Time & Space Complexity", "description": "Big O notation, Omega, Theta, space complexity, and asymptotic analysis.", "query": "time and space complexity big o notation tutorial"},
                    {"id": "dsa_3", "order": 3, "title": "3. Arrays", "description": "Array operations, memory layout, prefix sums, sub-array problems, and Kadane's Algorithm.", "query": "arrays data structures tutorial coding"},
                    {"id": "dsa_4", "order": 4, "title": "4. Strings", "description": "String immutability, pattern searching, anagrams, palindromes, and ASCII tricks.", "query": "strings data structures problem solving tutorial"},
                    {"id": "dsa_5", "order": 5, "title": "5. Searching", "description": "Linear search, Binary search, search space reduction, lower & upper bounds.", "query": "searching algorithms binary search tutorial"},
                    {"id": "dsa_6", "order": 6, "title": "6. Sorting", "description": "Bubble, Selection, Insertion, Merge Sort, Quick Sort, Count Sort, and stability.", "query": "sorting algorithms merge sort quick sort tutorial"},
                    {"id": "dsa_7", "order": 7, "title": "7. Two Pointers", "description": "Opposite direction, same direction, fast-slow pointers, and 3Sum/4Sum patterns.", "query": "two pointers pattern algorithm tutorial"},
                    {"id": "dsa_8", "order": 8, "title": "8. Sliding Window", "description": "Fixed and dynamic window sizes, max subarray, longest substring problems.", "query": "sliding window technique algorithm tutorial"},
                    {"id": "dsa_9", "order": 9, "title": "9. Hashing", "description": "Hash tables, hash functions, collision handling, frequency counting, and sets.", "query": "hashing hashmap data structures tutorial"},
                    {"id": "dsa_10", "order": 10, "title": "10. Linked Lists", "description": "Singly, Doubly, Circular Linked Lists, pointer manipulation, reversal, and cycle detection.", "query": "linked list data structure tutorial"},
                    {"id": "dsa_11", "order": 11, "title": "11. Stack", "description": "LIFO concept, stack via array/linked list, balanced parentheses, Next Greater Element.", "query": "stack data structure tutorial"},
                    {"id": "dsa_12", "order": 12, "title": "12. Queue", "description": "FIFO concept, Circular Queue, Deque, Priority Queue, and producer-consumer model.", "query": "queue data structure tutorial"},
                    {"id": "dsa_13", "order": 13, "title": "13. Recursion", "description": "Base case, recursive call stack, tail recursion, fibonacci, and Tower of Hanoi.", "query": "recursion data structures tutorial"},
                    {"id": "dsa_14", "order": 14, "title": "14. Backtracking", "description": "State space tree, N-Queens, Sudoku solver, Subsets, and Permutations.", "query": "backtracking algorithms tutorial"},
                    {"id": "dsa_15", "order": 15, "title": "15. Binary Trees", "description": "Tree terminology, Preorder, Inorder, Postorder, Level order traversals, height & diameter.", "query": "binary tree traversals data structures tutorial"},
                    {"id": "dsa_16", "order": 16, "title": "16. Binary Search Trees", "description": "BST properties, Insertion, Deletion, Searching, LCA in BST, and AVL introduction.", "query": "binary search tree bst tutorial"},
                    {"id": "dsa_17", "order": 17, "title": "17. Heap / Priority Queue", "description": "Min-heap, Max-heap, Heapify, Heap Sort, Top K Frequent Elements pattern.", "query": "heap priority queue data structure tutorial"},
                    {"id": "dsa_18", "order": 18, "title": "18. Graphs", "description": "Graph representations (Adjacency Matrix & List), Directed vs Undirected, Weighted graphs.", "query": "graphs data structure representation tutorial"},
                    {"id": "dsa_19", "order": 19, "title": "19. BFS", "description": "Breadth First Search algorithm, shortest path in unweighted graphs, level order traversal.", "query": "breadth first search bfs graph tutorial"},
                    {"id": "dsa_20", "order": 20, "title": "20. DFS", "description": "Depth First Search algorithm, cycle detection, connected components, topological sort.", "query": "depth first search dfs graph tutorial"},
                    {"id": "dsa_21", "order": 21, "title": "21. Greedy Algorithms", "description": "Greedy choice property, Activity Selection, Fractional Knapsack, Huffman Coding.", "query": "greedy algorithms tutorial"},
                    {"id": "dsa_22", "order": 22, "title": "22. Dynamic Programming", "description": "Overlapping subproblems, Optimal substructure, Memoization (Top-down) vs Tabulation (Bottom-up).", "query": "dynamic programming memoization tabulation tutorial"},
                    {"id": "dsa_23", "order": 23, "title": "23. Bit Manipulation", "description": "AND, OR, XOR, NOT, Bit shifts, Set/Unset bits, Power of two, Single Number problem.", "query": "bit manipulation data structures tutorial"},
                    {"id": "dsa_24", "order": 24, "title": "24. Advanced Problem Solving", "description": "Trie, Disjoint Set Union (DSU), Segment Trees, and FAANG interview coding patterns.", "query": "advanced dsa coding interview problem solving tutorial"}
                ]
            },

            # 2. SQL (19 Subtopics)
            {
                "id": "sql",
                "slug": "sql",
                "title": "SQL",
                "full_title": "Structured Query Language (SQL)",
                "icon": "🗄",
                "category": "Databases",
                "description": "Master relational database management, querying, joins, window functions, and database tuning.",
                "tags": ["sql", "database", "rdbms", "queries", "joins", "subqueries", "indexing", "mysql", "postgresql"],
                "subtopics": [
                    {"id": "sql_1", "order": 1, "title": "1. SQL Introduction", "description": "Relational database concepts, RDBMS overview, tables, columns, rows, and SQL data types.", "query": "sql introduction rdbms basics tutorial"},
                    {"id": "sql_2", "order": 2, "title": "2. SELECT", "description": "Writing basic SELECT statements, DISTINCT keyword, column aliasing, and expressions.", "query": "sql select statement tutorial"},
                    {"id": "sql_3", "order": 3, "title": "3. WHERE", "description": "Filtering rows with WHERE clause, AND, OR, NOT, IN, BETWEEN, LIKE, and NULL checks.", "query": "sql where clause filtering tutorial"},
                    {"id": "sql_4", "order": 4, "title": "4. ORDER BY", "description": "Sorting result sets ascending (ASC) and descending (DESC), multi-column sorting, and LIMIT.", "query": "sql order by limit offset tutorial"},
                    {"id": "sql_5", "order": 5, "title": "5. GROUP BY", "description": "Grouping rows by column values, HAVING clause vs WHERE clause.", "query": "sql group by having clause tutorial"},
                    {"id": "sql_6", "order": 6, "title": "6. Aggregate Functions", "description": "COUNT, SUM, AVG, MIN, MAX functions and handling NULL values in aggregates.", "query": "sql aggregate functions count sum avg min max tutorial"},
                    {"id": "sql_7", "order": 7, "title": "7. JOINS", "description": "INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL OUTER JOIN, CROSS JOIN, and Self JOIN.", "query": "sql joins inner left right outer join tutorial"},
                    {"id": "sql_8", "order": 8, "title": "8. Subqueries", "description": "Single-row, multi-row, correlated subqueries, EXISTS and IN operators.", "query": "sql subqueries correlated subqueries tutorial"},
                    {"id": "sql_9", "order": 9, "title": "9. Constraints", "description": "NOT NULL, UNIQUE, CHECK, DEFAULT, and constraint management.", "query": "sql constraints not null unique check tutorial"},
                    {"id": "sql_10", "order": 10, "title": "10. Primary Keys", "description": "Primary key concepts, composite primary keys, and auto-increment/identity columns.", "query": "sql primary key concept tutorial"},
                    {"id": "sql_11", "order": 11, "title": "11. Foreign Keys", "description": "Foreign key relationships, referential integrity, ON DELETE CASCADE, ON UPDATE CASCADE.", "query": "sql foreign key referential integrity tutorial"},
                    {"id": "sql_12", "order": 12, "title": "12. Views", "description": "Creating, updating, and dropping SQL Views, materialized views introduction.", "query": "sql views tutorial"},
                    {"id": "sql_13", "order": 13, "title": "13. Indexes", "description": "Clustered vs Non-clustered indexes, composite indexes, and performance impact.", "query": "sql indexes performance optimization tutorial"},
                    {"id": "sql_14", "order": 14, "title": "14. Transactions", "description": "COMMIT, ROLLBACK, SAVEPOINT, and ACID properties in SQL database transactions.", "query": "sql transactions commit rollback acid tutorial"},
                    {"id": "sql_15", "order": 15, "title": "15. Normalization", "description": "Database normalization forms: 1NF, 2NF, 3NF, BCNF, and denormalization.", "query": "database normalization 1nf 2nf 3nf bcnf tutorial"},
                    {"id": "sql_16", "order": 16, "title": "16. Window Functions", "description": "ROW_NUMBER, RANK, DENSE_RANK, NTILE, LEAD, LAG, OVER clause, and PARTITION BY.", "query": "sql window functions row_number rank dense_rank partition by tutorial"},
                    {"id": "sql_17", "order": 17, "title": "17. CTEs", "description": "Common Table Expressions (WITH clause) and Recursive CTEs.", "query": "sql common table expressions cte with clause tutorial"},
                    {"id": "sql_18", "order": 18, "title": "18. Query Optimization", "description": "EXPLAIN ANALYZE, query execution plans, indexing strategies, avoiding SELECT *.", "query": "sql query performance tuning explain analyze tutorial"},
                    {"id": "sql_19", "order": 19, "title": "19. SQL Interview Problems", "description": "Solving LeetCode / HackerRank SQL questions (Nth highest salary, active users).", "query": "sql interview questions leetcode hard sql problems tutorial"}
                ]
            },

            # 3. HTML (11 Subtopics)
            {
                "id": "html",
                "slug": "html",
                "title": "HTML",
                "full_title": "HyperText Markup Language (HTML5)",
                "icon": "🌐",
                "category": "Web Development",
                "description": "Learn modern semantic HTML5, web document structure, forms, accessibility, and SEO foundations.",
                "tags": ["html", "html5", "web development", "frontend", "semantic html", "forms", "a11y"],
                "subtopics": [
                    {"id": "html_1", "order": 1, "title": "1. HTML Basics", "description": "Document structure, <!DOCTYPE html>, <html>, <head>, <body> tags.", "query": "html basics webpage structure tutorial"},
                    {"id": "html_2", "order": 2, "title": "2. Elements & Attributes", "description": "HTML tags, opening/closing tags, self-closing tags, class and id attributes.", "query": "html elements and attributes tutorial"},
                    {"id": "html_3", "order": 3, "title": "3. Headings & Paragraphs", "description": "<h1> to <h6> heading hierarchy, <p>, <br>, <hr>, <span>, and <div> tags.", "query": "html headings paragraphs formatting tags tutorial"},
                    {"id": "html_4", "order": 4, "title": "4. Links & Images", "description": "<a> anchor tag, href, target='_blank', <img> tag, alt text, and image formats.", "query": "html links and images tutorial"},
                    {"id": "html_5", "order": 5, "title": "5. Lists", "description": "Ordered lists <ol>, unordered lists <ul>, list items <li>, definition lists <dl>.", "query": "html ordered unordered lists tutorial"},
                    {"id": "html_6", "order": 6, "title": "6. Tables", "description": "<table>, <tr>, <th>, <td>, colspan, rowspan, <thead>, <tbody>, <tfoot>.", "query": "html tables tutorial"},
                    {"id": "html_7", "order": 7, "title": "7. Forms", "description": "<form>, <input> types, <label>, <textarea>, <select>, <button>, required, pattern validation.", "query": "html forms inputs validation tutorial"},
                    {"id": "html_8", "order": 8, "title": "8. Semantic HTML", "description": "<header>, <nav>, <main>, <section>, <article>, <aside>, <footer> tags.", "query": "semantic html5 tags tutorial"},
                    {"id": "html_9", "order": 9, "title": "9. HTML5", "description": "<audio>, <video>, <canvas>, SVG embedding, local storage overview.", "query": "html5 features audio video canvas tutorial"},
                    {"id": "html_10", "order": 10, "title": "10. Accessibility", "description": "Web accessibility (a11y), ARIA roles, keyboard navigation, screen reader compatibility.", "query": "html web accessibility a11y tutorial"},
                    {"id": "html_11", "order": 11, "title": "11. SEO Basics", "description": "Meta title, meta description, Open Graph tags, canonical URLs, structured data.", "query": "html seo meta tags basics tutorial"}
                ]
            },

            # 4. CSS (12 Subtopics)
            {
                "id": "css",
                "slug": "css",
                "title": "CSS",
                "full_title": "Cascading Style Sheets (CSS3)",
                "icon": "🎨",
                "category": "Web Development",
                "description": "Master CSS styling, Box Model, Flexbox, Grid, Responsive Design, and CSS Animations.",
                "tags": ["css", "css3", "flexbox", "grid", "responsive design", "animations", "web design"],
                "subtopics": [
                    {"id": "css_1", "order": 1, "title": "1. CSS Basics", "description": "Inline, internal, external CSS, syntax, cascading, specificity, and inheritance.", "query": "css basics introduction syntax tutorial"},
                    {"id": "css_2", "order": 2, "title": "2. Selectors", "description": "Element, class, id, attribute, pseudo-class (:hover, :nth-child), pseudo-elements (::before, ::after).", "query": "css selectors pseudo classes elements tutorial"},
                    {"id": "css_3", "order": 3, "title": "3. Box Model", "description": "Content, padding, border, margin, box-sizing: border-box, and margin collapsing.", "query": "css box model tutorial"},
                    {"id": "css_4", "order": 4, "title": "4. Colors & Typography", "description": "HEX, RGB, HSL, web fonts, font-family, line-height, letter-spacing, text alignment.", "query": "css colors typography web fonts tutorial"},
                    {"id": "css_5", "order": 5, "title": "5. Flexbox", "description": "Flex container, flex-direction, justify-content, align-items, flex-wrap, flex-grow/shrink.", "query": "css flexbox complete guide tutorial"},
                    {"id": "css_6", "order": 6, "title": "6. Grid", "description": "Grid container, grid-template-columns/rows, gap, grid-area, auto-fit and minmax().", "query": "css grid layout tutorial"},
                    {"id": "css_7", "order": 7, "title": "7. Positioning", "description": "Static, relative, absolute, fixed, sticky positioning, z-index and stacking context.", "query": "css position relative absolute fixed sticky tutorial"},
                    {"id": "css_8", "order": 8, "title": "8. Responsive Design", "description": "Mobile-first approach, viewport meta tag, fluid units (rem, em, vh, vw, %).", "query": "responsive web design css tutorial"},
                    {"id": "css_9", "order": 9, "title": "9. Media Queries", "description": "@media rules, screen breakpoints, device orientations, and responsive layouts.", "query": "css media queries breakpoints tutorial"},
                    {"id": "css_10", "order": 10, "title": "10. Animations", "description": "@keyframes, animation-name, duration, iteration-count, fill-mode, timing-function.", "query": "css keyframes animations tutorial"},
                    {"id": "css_11", "order": 11, "title": "11. Transitions", "description": "transition-property, duration, timing-function, delay, transform (scale, rotate, translate).", "query": "css transitions transforms tutorial"},
                    {"id": "css_12", "order": 12, "title": "12. Advanced CSS", "description": "CSS Variables (--custom-prop), BEM methodology, glassmorphism, dark mode implementation.", "query": "advanced css custom properties variables bem dark mode tutorial"}
                ]
            },

            # 5. JAVASCRIPT (16 Subtopics)
            {
                "id": "javascript",
                "slug": "javascript",
                "title": "JavaScript",
                "full_title": "Modern JavaScript (ES6+)",
                "icon": "⚡",
                "category": "Web Development",
                "description": "Comprehensive JavaScript course covering syntax, DOM, Async programming, ES6+, Promises, and Projects.",
                "tags": ["javascript", "js", "es6", "async", "promises", "dom", "frontend", "web dev"],
                "subtopics": [
                    {"id": "js_1", "order": 1, "title": "1. JavaScript Basics", "description": "JS execution environment, script tags, console, statements, and comments.", "query": "javascript basics introduction tutorial"},
                    {"id": "js_2", "order": 2, "title": "2. Variables & Data Types", "description": "var vs let vs const, primitives (string, number, boolean, null, undefined, symbol) vs objects.", "query": "javascript variables data types let const tutorial"},
                    {"id": "js_3", "order": 3, "title": "3. Functions", "description": "Function declarations, function expressions, arrow functions, parameters, return values, scope.", "query": "javascript functions arrow functions scope tutorial"},
                    {"id": "js_4", "order": 4, "title": "4. Arrays", "description": "Array methods: push, pop, shift, unshift, map, filter, reduce, find, forEach, slice, splice.", "query": "javascript array methods map filter reduce tutorial"},
                    {"id": "js_5", "order": 5, "title": "5. Objects", "description": "Object literals, dot vs bracket notation, object methods, Object.keys(), Object.values().", "query": "javascript objects properties methods tutorial"},
                    {"id": "js_6", "order": 6, "title": "6. DOM", "description": "Document Object Model, querySelector, getElementById, innerText, innerHTML, style manipulation.", "query": "javascript dom manipulation queryselector tutorial"},
                    {"id": "js_7", "order": 7, "title": "7. Events", "description": "addEventListener, click, submit, keydown events, event object, event bubbling & capturing.", "query": "javascript event listeners handling bubbling tutorial"},
                    {"id": "js_8", "order": 8, "title": "8. ES6+", "description": "Template literals, default parameters, rest & spread operators, enhanced object literals.", "query": "es6 javascript features spread rest template literals tutorial"},
                    {"id": "js_9", "order": 9, "title": "9. Destructuring", "description": "Array destructuring, Object destructuring, nested destructuring, and parameter destructuring.", "query": "javascript destructuring assignment tutorial"},
                    {"id": "js_10", "order": 10, "title": "10. Promises", "description": "Asynchronous JS, callback hell, Promise states (pending, fulfilled, rejected), .then(), .catch().", "query": "javascript promises async programming tutorial"},
                    {"id": "js_11", "order": 11, "title": "11. Async/Await", "description": "async function syntax, await keyword, try/catch error handling with async code.", "query": "javascript async await tutorial"},
                    {"id": "js_12", "order": 12, "title": "12. Fetch API", "description": "Making GET, POST, PUT, DELETE HTTP requests with fetch(), handling JSON responses.", "query": "javascript fetch api http requests tutorial"},
                    {"id": "js_13", "order": 13, "title": "13. Modules", "description": "ES Modules (import/export), default exports, named exports, bundling overview.", "query": "javascript es modules import export tutorial"},
                    {"id": "js_14", "order": 14, "title": "14. Error Handling", "description": "try...catch...finally blocks, throwing custom errors, Error object properties.", "query": "javascript error handling try catch throw tutorial"},
                    {"id": "js_15", "order": 15, "title": "15. JavaScript Projects", "description": "Building interactive JS apps (Todo list, Weather app, Quiz app, Calculator).", "query": "javascript beginner projects tutorial"},
                    {"id": "js_16", "order": 16, "title": "16. JavaScript Interview Preparation", "description": "Closures, Event Loop, Hoisting, Prototype chain, 'this' keyword, debouncing & throttling.", "query": "javascript interview questions closures event loop hoisting this keyword tutorial"}
                ]
            },

            # 6. JAVA
            {
                "id": "java",
                "slug": "java",
                "title": "Java",
                "full_title": "Java Programming & OOP",
                "icon": "☕",
                "category": "Programming Languages",
                "description": "Learn core Java programming, JDK/JVM, OOP concepts, Collections Framework, and Multithreading.",
                "tags": ["java", "jdk", "jvm", "oop", "collections", "multithreading", "backend"],
                "subtopics": [
                    {"id": "java_1", "order": 1, "title": "1. Java Basics", "description": "Java history, JDK vs JRE vs JVM, Write Once Run Anywhere, main method.", "query": "java programming introduction tutorial"},
                    {"id": "java_2", "order": 2, "title": "2. Data Types & Control Flow", "description": "Primitives, wrappers, if/else, switch-case, for, while, do-while loops.", "query": "java data types loops control flow tutorial"},
                    {"id": "java_3", "order": 3, "title": "3. Classes & Objects", "description": "Class declaration, object creation, constructors, getters & setters.", "query": "java classes objects constructors tutorial"},
                    {"id": "java_4", "order": 4, "title": "4. OOP in Java", "description": "Encapsulation, Inheritance (extends), Polymorphism (Overloading vs Overriding), Abstraction.", "query": "java oop concepts inheritance polymorphism tutorial"},
                    {"id": "java_5", "order": 5, "title": "5. Interfaces & Abstract Classes", "description": "abstract keyword, interface implementation (implements), default & static methods.", "query": "java abstract class vs interface tutorial"},
                    {"id": "java_6", "order": 6, "title": "6. Collections Framework", "description": "ArrayList, LinkedList, HashSet, TreeSet, HashMap, TreeMap, Iterators.", "query": "java collections framework arraylist hashmap tutorial"},
                    {"id": "java_7", "order": 7, "title": "7. Exception Handling", "description": "try-catch-finally, checked vs unchecked exceptions, throw/throws, custom exceptions.", "query": "java exception handling checked unchecked tutorial"},
                    {"id": "java_8", "order": 8, "title": "8. Multithreading & Concurrency", "description": "Thread class, Runnable interface, synchronization, locks, ExecutorService.", "query": "java multithreading concurrency tutorial"},
                    {"id": "java_9", "order": 9, "title": "9. Streams API & Lambdas", "description": "Lambda expressions, Functional Interfaces, Stream operations (map, filter, collect).", "query": "java 8 streams api lambdas tutorial"},
                    {"id": "java_10", "order": 10, "title": "10. Java Interview Preparation", "description": "Memory management (Heap vs Stack), Garbage Collection, equals() vs ==, String pool.", "query": "java core interview questions garbage collection tutorial"}
                ]
            },

            # 7. PYTHON
            {
                "id": "python",
                "slug": "python",
                "title": "Python",
                "full_title": "Python Programming",
                "icon": "🐍",
                "category": "Programming Languages",
                "description": "Master Python syntax, data structures, OOP, decorators, generators, and async programming.",
                "tags": ["python", "py", "scripting", "backend", "data science", "oop"],
                "subtopics": [
                    {"id": "py_1", "order": 1, "title": "1. Python Basics", "description": "Python setup, indentation, print(), comments, type casting, input().", "query": "python programming for beginners tutorial"},
                    {"id": "py_2", "order": 2, "title": "2. Data Structures", "description": "Lists, Tuples, Sets, Dictionaries, list comprehensions, dict comprehensions.", "query": "python data structures lists tuples dicts sets tutorial"},
                    {"id": "py_3", "order": 3, "title": "3. Functions & Modules", "description": "def, *args, **kwargs, lambda functions, import statements, virtual environments.", "query": "python functions args kwargs modules tutorial"},
                    {"id": "py_4", "order": 4, "title": "4. OOP in Python", "description": "Classes, __init__ constructor, self, inheritance, magic (dunder) methods.", "query": "python oop classes inheritance dunder methods tutorial"},
                    {"id": "py_5", "order": 5, "title": "5. File Handling & Exceptions", "description": "open(), read/write, with statement, try-except-finally blocks.", "query": "python file handling exception handling tutorial"},
                    {"id": "py_6", "order": 6, "title": "6. Advanced Python", "description": "Decorators, Generators (yield), Iterators, Context Managers, Asyncio.", "query": "python decorators generators asyncio tutorial"},
                    {"id": "py_7", "order": 7, "title": "7. Python Interview Questions", "description": "GIL (Global Interpreter Lock), memory management, shallow vs deep copy.", "query": "python interview questions gil memory management tutorial"}
                ]
            },

            # 8. C
            {
                "id": "c",
                "slug": "c",
                "title": "C",
                "full_title": "C Programming Language",
                "icon": "🔤",
                "category": "Programming Languages",
                "description": "Procedural programming foundation, pointers, manual memory management, and system concepts.",
                "tags": ["c", "pointers", "memory", "system programming", "procedural"],
                "subtopics": [
                    {"id": "c_1", "order": 1, "title": "1. C Basics", "description": "C compilation process (Preprocessor, Compiler, Assembler, Linker), main(), printf/scanf.", "query": "c programming language introduction tutorial"},
                    {"id": "c_2", "order": 2, "title": "2. Control Statements & Functions", "description": "If-else, switch, loops, function parameters, pass by value vs reference.", "query": "c programming control flow functions tutorial"},
                    {"id": "c_3", "order": 3, "title": "3. Arrays & Strings", "description": "1D and 2D arrays, null-terminated char arrays, string.h library functions.", "query": "c programming arrays strings tutorial"},
                    {"id": "c_4", "order": 4, "title": "4. Pointers & Memory", "description": "Pointer syntax, address-of operator &, dereference *, pointer arithmetic, void pointers.", "query": "c programming pointers explained tutorial"},
                    {"id": "c_5", "order": 5, "title": "5. Dynamic Memory Allocation", "description": "malloc(), calloc(), realloc(), free(), memory leaks and dangling pointers.", "query": "c programming dynamic memory allocation malloc free tutorial"},
                    {"id": "c_6", "order": 6, "title": "6. Structures & File I/O", "description": "struct, typedef, fopen(), fclose(), fread(), fwrite(), C interview questions.", "query": "c programming structs file handling tutorial"}
                ]
            },

            # 9. C++
            {
                "id": "cpp",
                "slug": "cpp",
                "title": "C++",
                "full_title": "C++ & Standard Template Library (STL)",
                "icon": "⚡",
                "category": "Programming Languages",
                "description": "Object-oriented C++, STL containers, smart pointers, templates, and high-performance coding.",
                "tags": ["cpp", "c++", "stl", "dsa", "oop", "templates"],
                "subtopics": [
                    {"id": "cpp_1", "order": 1, "title": "1. C++ Syntax & Basics", "description": "cin/cout, namespaces, references (&), const keyword, inline functions.", "query": "cpp programming basics tutorial"},
                    {"id": "cpp_2", "order": 2, "title": "2. OOP in C++", "description": "Classes, constructors, destructors, access specifiers, copy constructor, virtual functions.", "query": "cpp oop virtual functions polymorphism tutorial"},
                    {"id": "cpp_3", "order": 3, "title": "3. STL Containers", "description": "std::vector, std::list, std::stack, std::queue, std::set, std::map, std::unordered_map.", "query": "cpp stl containers vector map tutorial"},
                    {"id": "cpp_4", "order": 4, "title": "4. STL Algorithms", "description": "std::sort, std::find, std::binary_search, iterators, lambda expressions in C++.", "query": "cpp stl algorithms tutorial"},
                    {"id": "cpp_5", "order": 5, "title": "5. Smart Pointers & Memory", "description": "std::unique_ptr, std::shared_ptr, std::weak_ptr, RAII pattern in modern C++.", "query": "cpp smart pointers unique_ptr shared_ptr tutorial"}
                ]
            },

            # 10. REACT
            {
                "id": "react",
                "slug": "react",
                "title": "React",
                "full_title": "React 18 & Frontend Architecture",
                "icon": "⚛️",
                "category": "Web Development",
                "description": "Build interactive single-page web applications with React components, Hooks, and State Management.",
                "tags": ["react", "jsx", "hooks", "frontend", "javascript", "spa", "redux"],
                "subtopics": [
                    {"id": "react_1", "order": 1, "title": "1. React Intro & JSX", "description": "Virtual DOM, JSX syntax, functional components, React render tree.", "query": "react js introduction jsx tutorial"},
                    {"id": "react_2", "order": 2, "title": "2. Components & Props", "description": "Component composition, passing props, prop destructuring, children prop.", "query": "react components and props tutorial"},
                    {"id": "react_3", "order": 3, "title": "3. State & useState", "description": "Managing component state with useState hook, immutable state updates.", "query": "react usestate hook tutorial"},
                    {"id": "react_4", "order": 4, "title": "4. Lifecycle & useEffect", "description": "Side effects, dependency array, cleanup functions, data fetching pattern.", "query": "react useeffect hook data fetching tutorial"},
                    {"id": "react_5", "order": 5, "title": "5. Context API & Custom Hooks", "description": "Global state without prop drilling via createContext/useContext, building custom hooks.", "query": "react context api custom hooks tutorial"},
                    {"id": "react_6", "order": 6, "title": "6. Performance & Optimization", "description": "useMemo, useCallback, React.memo, code splitting with React.lazy & Suspense.", "query": "react performance optimization usememo usecallback tutorial"}
                ]
            },

            # 11. NODE.JS
            {
                "id": "nodejs",
                "slug": "nodejs",
                "title": "Node.js",
                "full_title": "Node.js & Express.js Backend",
                "icon": "🟢",
                "category": "Web Development",
                "description": "Server-side JavaScript runtime, Event Loop, Express REST APIs, middleware, and backend services.",
                "tags": ["nodejs", "express", "backend", "javascript", "event loop", "rest api"],
                "subtopics": [
                    {"id": "node_1", "order": 1, "title": "1. Node.js Architecture", "description": "Single-threaded non-blocking I/O model, V8 engine, Event Loop execution stages.", "query": "nodejs architecture event loop explained tutorial"},
                    {"id": "node_2", "order": 2, "title": "2. Core Modules & npm", "description": "fs, path, http, os, events modules, package.json, npm scripts.", "query": "nodejs core modules fs path http tutorial"},
                    {"id": "node_3", "order": 3, "title": "3. Express.js Basics", "description": "Express app setup, routing, req & res objects, status codes.", "query": "express js crash course tutorial"},
                    {"id": "node_4", "order": 4, "title": "4. Middleware & REST Routing", "description": "Custom middleware, app.use(), body parser, CORS, error handling middleware.", "query": "express js middleware rest api routing tutorial"},
                    {"id": "node_5", "order": 5, "title": "5. Authentication & JWT", "description": "Password hashing (bcrypt), JSON Web Tokens (JWT) sign & verify, protected routes.", "query": "nodejs express jwt authentication tutorial"}
                ]
            },

            # 12. MONGODB
            {
                "id": "mongodb",
                "slug": "mongodb",
                "title": "MongoDB",
                "full_title": "MongoDB NoSQL Database",
                "icon": "🍃",
                "category": "Databases",
                "description": "Document-oriented NoSQL database, CRUD queries, Aggregation Pipeline, indexing, and drivers.",
                "tags": ["mongodb", "nosql", "database", "crud", "aggregation", "mongoose", "motor"],
                "subtopics": [
                    {"id": "mongo_1", "order": 1, "title": "1. NoSQL Intro & MongoDB Basics", "description": "RDBMS vs NoSQL, BSON documents, collections, MongoDB Compass GUI.", "query": "mongodb nosql database basics tutorial"},
                    {"id": "mongo_2", "order": 2, "title": "2. CRUD Operations", "description": "insertOne, insertMany, find, updateOne, updateMany, deleteOne, deleteMany.", "query": "mongodb crud operations tutorial"},
                    {"id": "mongo_3", "order": 3, "title": "3. Query Operators", "description": "$gt, $gte, $in, $and, $or, $regex, $elemMatch array queries.", "query": "mongodb query operators tutorial"},
                    {"id": "mongo_4", "order": 4, "title": "4. Aggregation Pipeline", "description": "$match, $group, $project, $sort, $limit, $lookup (joins), $unwind stages.", "query": "mongodb aggregation pipeline tutorial"},
                    {"id": "mongo_5", "order": 5, "title": "5. Indexing & Modeling", "description": "Single field, compound, unique indexes, EXPLAIN plans, embedding vs referencing data models.", "query": "mongodb indexing data modeling tutorial"}
                ]
            },

            # 13. DBMS
            {
                "id": "dbms",
                "slug": "dbms",
                "title": "DBMS",
                "full_title": "Database Management Systems",
                "icon": "💾",
                "category": "Computer Science",
                "description": "Core CS database theory: ER Diagrams, Relational Algebra, Normalization, Transactions, and Indexing.",
                "tags": ["dbms", "database", "acid", "transactions", "normalization", "cs core"],
                "subtopics": [
                    {"id": "dbms_1", "order": 1, "title": "1. DBMS Architecture", "description": "1-tier, 2-tier, 3-tier architectures, schema levels, data independence.", "query": "dbms architecture data independence tutorial"},
                    {"id": "dbms_2", "order": 2, "title": "2. ER Diagrams", "description": "Entities, Attributes, Relationships, Cardinality, ER to Relational schema mapping.", "query": "er diagram database design tutorial"},
                    {"id": "dbms_3", "order": 3, "title": "3. Relational Algebra", "description": "Selection, Projection, Union, Set Difference, Cartesian Product, Joins in relational algebra.", "query": "relational algebra dbms tutorial"},
                    {"id": "dbms_4", "order": 4, "title": "4. Normalization", "description": "Functional dependencies,closure, 1NF, 2NF, 3NF, BCNF decomposition.", "query": "dbms normalization 1nf 2nf 3nf bcnf tutorial"},
                    {"id": "dbms_5", "order": 5, "title": "5. Transactions & ACID", "description": "Atomicity, Consistency, Isolation, Durability, Transaction states, serializability.", "query": "dbms acid properties transactions serializability tutorial"}
                ]
            },

            # 14. OPERATING SYSTEMS
            {
                "id": "os",
                "slug": "os",
                "title": "Operating Systems",
                "full_title": "Operating Systems Fundamentals",
                "icon": "🖥",
                "category": "Computer Science",
                "description": "Processes, Threads, CPU Scheduling, Synchronization, Memory Management, and Deadlocks.",
                "tags": ["os", "operating systems", "processes", "threads", "memory", "deadlocks"],
                "subtopics": [
                    {"id": "os_1", "order": 1, "title": "1. Processes & Threads", "description": "Process state diagram, PCB, context switching, user mode vs kernel mode, threads.", "query": "operating systems process vs thread context switch tutorial"},
                    {"id": "os_2", "order": 2, "title": "2. CPU Scheduling", "description": "FCFS, SJF, Round Robin, Priority Scheduling, Gantt charts, throughput & latency.", "query": "cpu scheduling algorithms round robin sjf tutorial"},
                    {"id": "os_3", "order": 3, "title": "3. Synchronization & Deadlocks", "description": "Critical section problem, Semaphores, Mutex, Deadlock 4 conditions, Banker's Algorithm.", "query": "process synchronization semaphores deadlocks tutorial"},
                    {"id": "os_4", "order": 4, "title": "4. Memory Management", "description": "Paging, Segmentation, TLB, Page replacement algorithms (FIFO, LRU, Optimal).", "query": "operating systems virtual memory paging lru tutorial"}
                ]
            },

            # 15. COMPUTER NETWORKS
            {
                "id": "cn",
                "slug": "cn",
                "title": "Computer Networks",
                "full_title": "Computer Networking Protocols",
                "icon": "🌐",
                "category": "Computer Science",
                "description": "OSI 7-Layer Model, TCP/IP, IP Subnetting, Routing, DNS, HTTP/HTTPS, and Sockets.",
                "tags": ["cn", "networking", "tcp/ip", "osi", "dns", "http", "sockets"],
                "subtopics": [
                    {"id": "cn_1", "order": 1, "title": "1. Network Models (OSI & TCP/IP)", "description": "7 layers of OSI model, 4 layers of TCP/IP, encapsulation and decapsulation.", "query": "osi model 7 layers tcp ip tutorial"},
                    {"id": "cn_2", "order": 2, "title": "2. IP Addressing & Subnetting", "description": "IPv4 vs IPv6, CIDR notation, subnet masks, public vs private IP addresses.", "query": "ip addressing subnetting cidr tutorial"},
                    {"id": "cn_3", "order": 3, "title": "3. Transport Layer (TCP vs UDP)", "description": "TCP 3-way handshake, flow control (sliding window), congestion control, UDP datagrams.", "query": "tcp vs udp transport layer 3 way handshake tutorial"},
                    {"id": "cn_4", "order": 4, "title": "4. Application Protocols (HTTP/DNS)", "description": "DNS lookup process, HTTP/1.1 vs HTTP/2 vs HTTP/3, TLS/SSL handshake.", "query": "http https dns lookup process tutorial"}
                ]
            },

            # 16. OOP
            {
                "id": "oop",
                "slug": "oop",
                "title": "OOP",
                "full_title": "Object-Oriented Programming & Design",
                "icon": "🧱",
                "category": "Computer Science",
                "description": "Core object-oriented principles, SOLID design principles, design patterns, and modular architecture.",
                "tags": ["oop", "object oriented", "solid", "design patterns", "cs core"],
                "subtopics": [
                    {"id": "oop_1", "order": 1, "title": "1. OOP Four Pillars", "description": "Encapsulation, Abstraction, Inheritance, and Polymorphism explained with real-world examples.", "query": "object oriented programming 4 pillars tutorial"},
                    {"id": "oop_2", "order": 2, "title": "2. SOLID Principles", "description": "Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.", "query": "solid principles object oriented design tutorial"},
                    {"id": "oop_3", "order": 3, "title": "3. Design Patterns", "description": "Creational (Singleton, Factory), Structural (Adapter, Decorator), Behavioral (Observer, Strategy).", "query": "design patterns singleton factory observer tutorial"}
                ]
            },

            # 17. GIT & GITHUB
            {
                "id": "git",
                "slug": "git",
                "title": "Git & GitHub",
                "full_title": "Git Version Control & GitHub",
                "icon": "🛠",
                "category": "Developer Tools",
                "description": "Version control fundamentals, branching strategies, merge conflicts, pull requests, and CI/CD pipelines.",
                "tags": ["git", "github", "version control", "rebase", "branching", "ci/cd"],
                "subtopics": [
                    {"id": "git_1", "order": 1, "title": "1. Git Basics", "description": "git init, add, commit, status, log, diff, and working directory vs staging area.", "query": "git basics crash course tutorial"},
                    {"id": "git_2", "order": 2, "title": "2. Branching & Merging", "description": "git branch, checkout, switch, merge, resolving merge conflicts cleanly.", "query": "git branching merging conflict resolution tutorial"},
                    {"id": "git_3", "order": 3, "title": "3. Git Rebase & Stash", "description": "git rebase vs merge, interactive rebase, git stash, git cherry-pick.", "query": "git rebase vs merge stash tutorial"},
                    {"id": "git_4", "order": 4, "title": "4. GitHub Workflow", "description": "Remote repositories, git push/pull/fetch, Pull Requests, code reviews, GitHub Actions.", "query": "github workflow pull requests github actions tutorial"}
                ]
            },

            # 18. REST APIS
            {
                "id": "rest_api",
                "slug": "rest_api",
                "title": "REST APIs",
                "full_title": "RESTful API Architecture & Integration",
                "icon": "🔌",
                "category": "Web Development",
                "description": "Design clean RESTful web services, HTTP verbs, status codes, OpenAPI/Swagger docs, and security.",
                "tags": ["rest", "api", "http", "json", "swagger", "postman"],
                "subtopics": [
                    {"id": "api_1", "order": 1, "title": "1. REST API Architecture", "description": "Statelessness, Client-Server separation, Uniform Interface, Cacheability.", "query": "rest api architecture design principles tutorial"},
                    {"id": "api_2", "order": 2, "title": "2. HTTP Methods & Status Codes", "description": "GET, POST, PUT, PATCH, DELETE, 200, 201, 400, 401, 403, 404, 500 status codes.", "query": "http methods status codes rest api tutorial"},
                    {"id": "api_3", "order": 3, "title": "3. API Documentation & Testing", "description": "OpenAPI / Swagger specs, Postman testing collections, rate limiting.", "query": "rest api documentation swagger postman tutorial"}
                ]
            },

            # 19. DOCKER
            {
                "id": "docker",
                "slug": "docker",
                "title": "Docker",
                "full_title": "Docker & Containerization",
                "icon": "🐳",
                "category": "Developer Tools",
                "description": "Containerize applications, write optimized Dockerfiles, manage multi-container apps with Docker Compose.",
                "tags": ["docker", "containers", "dockerfile", "docker compose", "devops"],
                "subtopics": [
                    {"id": "doc_1", "order": 1, "title": "1. Containers vs VMs", "description": "Container isolation, Docker Engine architecture, running containers from Docker Hub.", "query": "docker containers vs virtual machines tutorial"},
                    {"id": "doc_2", "order": 2, "title": "2. Dockerfile & Images", "description": "FROM, RUN, COPY, CMD, ENTRYPOINT, building images, layer caching.", "query": "writing dockerfile best practices tutorial"},
                    {"id": "doc_3", "order": 3, "title": "3. Docker Compose", "description": "docker-compose.yml, multi-container applications (Frontend + Backend + DB), environment variables.", "query": "docker compose multi container app tutorial"}
                ]
            },

            # 20. LINUX
            {
                "id": "linux",
                "slug": "linux",
                "title": "Linux",
                "full_title": "Linux Operating System & Shell Scripting",
                "icon": "🐧",
                "category": "Developer Tools",
                "description": "Master Linux command line, file permissions, process management, and bash shell scripting.",
                "tags": ["linux", "bash", "shell", "terminal", "devops", "sysadmin"],
                "subtopics": [
                    {"id": "lin_1", "order": 1, "title": "1. Linux CLI & File System", "description": "ls, cd, mkdir, rm, cp, mv, grep, find, file permissions (chmod, chown).", "query": "linux command line basics tutorial"},
                    {"id": "lin_2", "order": 2, "title": "2. Process & Package Management", "description": "ps, top, htop, kill, systemctl, apt/yum package managers.", "query": "linux process management commands tutorial"},
                    {"id": "lin_3", "order": 3, "title": "3. Bash Shell Scripting", "description": "Variables, loops, conditionals, functions, cron jobs for task automation.", "query": "bash shell scripting for beginners tutorial"}
                ]
            },

            # 21. SYSTEM DESIGN
            {
                "id": "system_design",
                "slug": "system_design",
                "title": "System Design",
                "full_title": "System Design & Distributed Systems",
                "icon": "🏗",
                "category": "System Design",
                "description": "High-Level System Design (HLD): Scalability, Load Balancers, Caching, Sharding, Message Queues.",
                "tags": ["system design", "hld", "scalability", "architecture", "distributed systems", "redis", "kafka"],
                "subtopics": [
                    {"id": "sd_1", "order": 1, "title": "1. Scalability Fundamentals", "description": "Vertical vs Horizontal scaling, Load Balancers (Nginx/HAProxy), Stateless applications.", "query": "system design scalability load balancing tutorial"},
                    {"id": "sd_2", "order": 2, "title": "2. Caching & CDNs", "description": "Redis / Memcached caching strategies, Cache eviction (LRU), CDN edge caching.", "query": "system design caching strategies redis tutorial"},
                    {"id": "sd_3", "order": 3, "title": "3. Database Scaling & Messaging", "description": "Database replication, Sharding, Consistent Hashing, Message Queues (Kafka/RabbitMQ).", "query": "database sharding message queues system design tutorial"}
                ]
            },

            # 22. AWS
            {
                "id": "aws",
                "slug": "aws",
                "title": "AWS",
                "full_title": "Amazon Web Services (AWS) Cloud",
                "icon": "☁️",
                "category": "Cloud & DevOps",
                "description": "Learn core AWS cloud services: EC2, S3, IAM, VPC, RDS, Lambda serverless, and deployment.",
                "tags": ["aws", "cloud", "ec2", "s3", "iam", "serverless", "devops"],
                "subtopics": [
                    {"id": "aws_1", "order": 1, "title": "1. AWS Fundamentals & IAM", "description": "Cloud computing benefits, IAM Users, Roles, Policies, MFA, root account safety.", "query": "aws cloud basics iam security tutorial"},
                    {"id": "aws_2", "order": 2, "title": "2. EC2 & S3", "description": "Launching EC2 instances, Security Groups, S3 buckets, object storage, static website hosting.", "query": "aws ec2 s3 tutorial"},
                    {"id": "aws_3", "order": 3, "title": "3. VPC & Lambda Serverless", "description": "VPC subnets, route tables, AWS Lambda serverless functions, API Gateway.", "query": "aws vpc serverless lambda tutorial"}
                ]
            },

            # 23. AZURE
            {
                "id": "azure",
                "slug": "azure",
                "title": "Azure",
                "full_title": "Microsoft Azure Cloud Platform",
                "icon": "🔷",
                "category": "Cloud & DevOps",
                "description": "Core Azure services: Azure VMs, Blob Storage, App Service, Cosmos DB, and Azure DevOps.",
                "tags": ["azure", "microsoft", "cloud", "vms", "devops"],
                "subtopics": [
                    {"id": "az_1", "order": 1, "title": "1. Azure Core Services", "description": "Azure Resource Groups, Virtual Machines, Blob Storage, App Services.", "query": "azure fundamentals core services tutorial"},
                    {"id": "az_2", "order": 2, "title": "2. Azure Networking & Databases", "description": "Virtual Networks (VNet), Azure SQL, Cosmos DB NoSQL database.", "query": "azure networking vnet cosmos db tutorial"}
                ]
            },

            # 24. KUBERNETES
            {
                "id": "kubernetes",
                "slug": "kubernetes",
                "title": "Kubernetes",
                "full_title": "Kubernetes (K8s) Container Orchestration",
                "icon": "☸️",
                "category": "Cloud & DevOps",
                "description": "Automate deployment, scaling, and management of containerized applications with Kubernetes.",
                "tags": ["kubernetes", "k8s", "containers", "devops", "kubectl", "helm"],
                "subtopics": [
                    {"id": "k8s_1", "order": 1, "title": "1. K8s Architecture & Pods", "description": "Control Plane vs Worker Nodes, Pods, kubectl commands, YAML manifest files.", "query": "kubernetes architecture pods tutorial"},
                    {"id": "k8s_2", "order": 2, "title": "2. Deployments & Services", "description": "ReplicaSets, Deployments, ClusterIP, NodePort, LoadBalancer services, Ingress.", "query": "kubernetes deployments services ingress tutorial"}
                ]
            }
        ]

        # Convert subtopics into resources list for each topic
        for topic in catalog:
            subtopics = topic.get("subtopics", [])
            resources = []
            for sub in subtopics:
                resources.append({
                    "id": f"res_{topic['id']}_{sub['order']}",
                    "subtopic_id": sub["id"],
                    "order": sub["order"],
                    "title": sub["title"],
                    "description": sub["description"],
                    "topic": topic["title"],
                    "topic_id": topic["id"],
                    "difficulty": "Beginner" if sub["order"] <= 3 else ("Intermediate" if sub["order"] <= len(subtopics) - 3 else "Advanced"),
                    "platform": "YouTube",
                    "url": s_url(sub["query"])
                })
            topic["resources"] = resources

        return catalog
