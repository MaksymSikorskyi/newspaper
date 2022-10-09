# The Newspaper

Media agency/newspaper web site

## Ideas and functionality

- [ ] Static and dynamic pages
    - [ ] Home page, articles
    - [ ] Terms, about, contacts (optional)
- [x] Articles
    - [ ] Rich-text content
    - [ ] Main image and attached image gallery
    - [ ] Featured articles
- [x] Categories and tags
- [ ] Social interactions (likes/dislikes)
    - [ ] Social sharing
- [ ] Comments
- [ ] Users authentication and profiles
    - [ ] Author profile
- [ ] Newsletter (daily, weekly, most popular, etc)
- [ ] API for public articles
- [ ] Telegram feed


## Main requirements

#### Articles

- Title (text, maximum 300 chars)
- Slug (unique text per publication date, for urls)
- Short content / description (text, max 600 chars)
- Content (rich-text, unlimited)
- Main image (optional)
- Category (required)
- Tags (optional, comma-separated list)
- Publishing date (date without time)

#### Categories

- Name (text, max 100 chars)
- Slug (unique text, for urls)
- Image (optional)

#### Comments

- Author (user who left the comment)
- Message (text)


## Tech & libs

- Django
- PostgreSQL
- Django Extensions (for tools and extra fields)
- Django ImageKit (for images)
- Django Taggit (for tags)
- Django Rest Framework (for API)
- Django Debug Toolbar
