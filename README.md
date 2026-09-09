# Plumbers Boynton Beach

Static marketing site. No build step, no dependencies. Every page is plain HTML.

## Deploy to Vercel
1. Push the contents of this `site/` folder to a GitHub repository (files at repo root).
2. In Vercel, **Add New Project** and import that repository.
3. Framework preset: **Other**. Build command: leave empty. Output directory: `.` (repo root).
4. Deploy, then add your domain under Project Settings → Domains.

## Before going live
- Replace `https://plumbersboyntonbeach.com` in `sitemap.xml`, `robots.txt` and every page's canonical/JSON-LD if the final domain differs.
- Update `service@plumbersboyntonbeach.com` on the Contact page if a different inbox is used.
- Submit `/sitemap.xml` in Google Search Console.

## Structure
```
index.html            Home
services/             Index + 16 service pages
fl/                   Index + 12 city pages
blog/                 Index + 3 articles
about-us/ contact-us/ faq/ privacy-policy/ terms-of-service/
assets/               site.css, site.js, logo.svg, img/
sitemap.xml robots.txt vercel.json
```

Phone: +1 833 567 2788 · Theme: #0B6E5B teal, #D98324 amber · Fonts: Archivo + Source Sans 3
