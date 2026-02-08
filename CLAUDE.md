# CLAUDE.md - Luxe Properties (reexample)

## Project Overview

**Luxe Properties** is a luxury real estate listing website built with **Python FastHTML** framework. It serves as a marketing and lead-generation platform for a real estate business, showcasing properties for sale, lease, and pre-selling. All content is currently static/hardcoded (no database).

---

## Business Workflow

### Core Business Purpose
- Display luxury real estate properties to potential buyers, renters, and investors
- Capture leads through a contact form (name, email, phone, interest, message)
- Build trust through company info, team profiles, testimonials, and stats

### User Journey
1. **Land on Homepage** (`/`) - See hero banner with search box (Buy/Rent/Sell tabs), featured property listings, property categories, about section, testimonials, and contact form
2. **Browse Listings** - Navigate to specific listing pages:
   - `/for-sale` - Properties available for purchase (Philippine market, prices in PHP-styled as $)
   - `/pre-selling` - Upcoming developments from named developers (Ayala Land, SMDC, Megaworld, DMCI, Robinsons Land) with turnover years
   - `/for-lease` - Rental properties with furnishing status and lease terms
3. **Learn About Company** (`/about`) - Company story, stats, features (verified listings, expert agents, secure transactions, 24/7 support), team profiles
4. **Contact** (`/contact`) - Contact form, office location, phone, email, office hours, map placeholder

### Listing Page Features (For Sale / For Lease / Pre-Selling)
- **Filter sidebar** (location, property type, price range, bedrooms, + page-specific filters)
- **Sort** (newest, price low-high, price high-low, size/turnover)
- **Grid/List view toggle**
- **Favorite/heart button** (persisted in localStorage per listing type)
- **Pagination** (client-side, simulated)
- **Breadcrumb navigation**

### Property Data (All Hardcoded)
- **For Sale**: 6 listings (Pasig, BGC, Muntinlupa, Makati, Quezon City) - $12.5M-$85M range
- **For Lease**: 6 listings (Makati, BGC, Ortigas, Muntinlupa, QC) - $28K-$180K/month
- **Pre-Selling**: 6 listings (Makati, BGC, Laguna, Manila, QC, Cebu) - $4.5M-$12M starting

---

## Technical Workflow

### Tech Stack
- **Backend**: Python 3.11+ with [FastHTML](https://github.com/AnswerDotAI/fasthtml) (ASGI web framework)
- **UI Framework**: MonsterUI (listed as dependency, not actively used in pages)
- **Frontend**: Vanilla CSS + Vanilla JavaScript (no build tools, no bundler)
- **Font**: Google Fonts - Poppins (300-700 weights)
- **Images**: Unsplash CDN (external URLs)
- **Package Manager**: uv (pyproject.toml)
- **Dependencies**: python-fasthtml, monsterui, pydantic, python-dotenv

### Project Structure

```
reexample/
├── main.py                          # App entry point - route definitions
├── pyproject.toml                   # Python dependencies
├── scratch.py                       # Design reference (HTML mockup, not used at runtime)
├── .sesskey                         # FastHTML session key
├── pages/                           # Page view functions (return full HTML documents)
│   ├── homepage.py                  # Landing page with all sections
│   ├── forsale.py                   # For-sale listings with filter sidebar
│   ├── preselling.py                # Pre-selling listings with filter sidebar
│   ├── forlease.py                  # For-lease listings with filter sidebar
│   ├── about.py                     # About page (story, stats, features, team)
│   └── contact.py                   # Contact page (form, info, map placeholder)
├── styles/
│   ├── components/                  # Shared UI components
│   │   ├── navbar.py                # Navbar() function - reusable across all pages
│   │   ├── navbar.css               # Navbar styles (fixed header, mobile menu, responsive)
│   │   ├── navbar.js                # Navbar behavior (scroll effect, mobile toggle)
│   │   ├── footer.py                # AppFooter() function - reusable across all pages
│   │   └── footer.css               # Footer styles + CSS custom properties (design tokens)
│   └── static/                      # Page-specific assets served via fast_app(static_dir=)
│       ├── homepage.css / .js       # Homepage-specific styles and interactions
│       ├── about.css / .js          # About page styles and animations
│       ├── contact.css / .js        # Contact page styles and form handling
│       ├── forsale.css / .js        # For-sale listing styles and interactions
│       ├── forlease.css / .js       # For-lease listing styles and interactions
│       ├── preselling.css / .js     # Pre-selling listing styles and interactions
│       └── listing.js               # Shared listing page logic (filters, sort, pagination, favorites)
└── documents/                       # Project documents (excluded from code analysis)
```

### Routing (main.py)

| Route           | Handler Function    | Page Module            |
|-----------------|---------------------|------------------------|
| `/`             | `home()`            | `pages.homepage`       |
| `/for-sale`     | `forsale()`         | `pages.forsale`        |
| `/pre-selling`  | `preselling()`      | `pages.preselling`     |
| `/for-lease`    | `forlease()`        | `pages.forlease`       |
| `/about`        | `about()`           | `pages.about`          |
| `/contact`      | `contact()`         | `pages.contact`        |

### How Pages Are Built
Each page function returns a complete `Html(Head(...), Body(...))` document:
1. **Head**: Meta tags (SEO), Google Fonts link, CSS links (navbar.css, footer.css, page-specific.css)
2. **Body**: `Navbar(active="pagename")` -> page sections -> `AppFooter()` -> Script tags (navbar.js, page-specific.js)

All HTML is generated server-side using FastHTML's Python-to-HTML element constructors (`Div()`, `Section()`, `H1()`, etc.). No templating engine - it's pure Python function composition.

### Shared Components

**Navbar** (`styles/components/navbar.py`):
- Accepts `active` param to highlight current page link
- Desktop nav: logo, 6 links (Home, For Sale, Pre-Selling, For Lease, About, Contact), phone number, "Get Started" CTA
- Mobile: hamburger toggle -> slide-in menu with overlay
- CSS: Fixed position, transparent -> white background on scroll (`header.scrolled` class via JS)

**Footer** (`styles/components/footer.py`):
- 4-column grid: brand info + social icons, Quick Links, Property Types, Support
- Bottom bar: copyright + legal links
- Helper functions: `footer_column()`, `social()`

### CSS Architecture
- **Design tokens** defined in `footer.css` `:root` (also applies globally):
  - `--primary: #8b6914` (gold/brown), `--primary-dark: #725611`
  - `--background: #ffffff`, `--card: #f5f5f5`, `--text: #1a1a1a`, `--text-muted: #555555`
  - `--border: #e0e0e0`, `--font-main: 'Poppins'`
- Each page has its own CSS file with self-contained styles
- Responsive breakpoints: 1200px, 1024px (tablet/mobile menu), 768px, 480px

### JavaScript Behavior (Client-Side)

**Navbar JS** (`navbar.js` - loaded on every page):
- Header scroll effect (add `scrolled` class at 50px scroll)
- Mobile menu open/close with overlay
- Active nav link management

**Homepage JS** (`homepage.js`):
- Search tabs (Buy/Rent/Sell) switching
- Property favorite toggle
- Animated stats counter (IntersectionObserver triggers count-up)
- Testimonials auto-rotating slider with dot navigation (5s interval)
- Contact form validation (client-side only, no server submission)
- Search form handling (logs params, scrolls to properties section)
- Scroll reveal animation for cards

**Listing Pages JS** (`forsale.js`, `forlease.js`, `preselling.js`):
- Filter sidebar toggle (mobile: slide-in with overlay, ESC to close)
- Grid/List view toggle
- Favorites management (localStorage per listing type: `saleFavorites`, `leaseFavorites`, `presellFavorites`)
- Client-side sort by price (low-high, high-low)
- Pagination UI (client-side page switching, simulated loading)
- Toast notifications
- Lazy image loading via IntersectionObserver

**About JS** (`about.js`): Stats counter animation + scroll reveal for feature/team cards

**Contact JS** (`contact.js`): Form validation + simulated submission with toast notification

**listing.js**: Shared/generic listing logic (similar to page-specific JS but includes share and compare button features)

### Key Technical Notes
- **No database**: All property data is hardcoded in Python page files
- **No backend form handling**: Contact/search forms are handled client-side only (preventDefault, no POST routes)
- **No authentication**: Public-facing only
- **Static file serving**: `fast_app(static_dir="styles/static")` serves JS/CSS from `styles/static/`
- **CSS/JS per page**: Each page has dedicated CSS and JS files (navbar and footer are shared)
- **scratch.py**: Contains a full HTML mockup of the original single-page design (reference only, not imported anywhere)
- **Server**: `serve()` starts the Uvicorn ASGI server

### Running the App
```bash
cd /Users/danmarcllanes/Desktop/project-2026/reexample
uv run python main.py
# or
python main.py
```
The app starts on `http://localhost:5001` (FastHTML default).
