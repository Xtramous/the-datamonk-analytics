"""Web scraper for The Data Monk blog posts."""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

from ..config import settings, RAW_DATA_DIR

logger = logging.getLogger(__name__)


class WebScraper:
    """Scrape blog posts from The Data Monk website."""

    def __init__(self, base_url: str = settings.WEBSITE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Data Engineering Bot)"
        })

    def get_latest_posts(self, limit: int = settings.NUM_POSTS_TO_SCRAPE) -> list[dict]:
        """
        Scrape latest N blog posts from website.

        Args:
            limit: Number of posts to scrape

        Returns:
            List of post dictionaries with metadata and content
        """
        try:
            logger.info(f"Scraping latest {limit} posts from {self.base_url}")
            response = self.session.get(self.base_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            posts = []

            # Try different selectors for blog post links
            post_selectors = [
                'article',
                '[class*="post"]',
                '[class*="blog"]',
                'h2.post-title',
            ]

            post_elements = []
            for selector in post_selectors:
                elements = soup.select(selector)
                if elements:
                    post_elements = elements[:limit]
                    break

            if not post_elements:
                logger.warning("Could not find post elements with selectors")
                # Fallback: extract all links that look like blog posts
                all_links = soup.find_all('a', href=True)
                post_links = [
                    link for link in all_links
                    if any(keyword in link['href'].lower()
                          for keyword in ['blog', 'post', 'article'])
                ][:limit]
            else:
                post_links = []
                for elem in post_elements:
                    link = elem.find('a')
                    if link and link.get('href'):
                        post_links.append(link)

            logger.info(f"Found {len(post_links)} post links")

            for idx, link in enumerate(post_links, 1):
                post_url = link['href']
                if not post_url.startswith('http'):
                    post_url = self.base_url.rstrip('/') + '/' + post_url.lstrip('/')

                post_data = self._scrape_post(post_url, idx)
                if post_data:
                    posts.append(post_data)

            logger.info(f"Successfully scraped {len(posts)} posts")
            return posts

        except requests.RequestException as e:
            logger.error(f"Error scraping website: {e}")
            return []

    def _scrape_post(self, url: str, post_number: int) -> Optional[dict]:
        """
        Scrape individual blog post.

        Args:
            url: Post URL
            post_number: Post index for naming

        Returns:
            Dictionary with post metadata and content
        """
        try:
            logger.info(f"Scraping post {post_number}: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract title
            title_elem = soup.find(['h1', 'h2'])
            title = title_elem.get_text(strip=True) if title_elem else "Untitled"

            # Extract main content
            content_elem = soup.find(['article', 'main', '[class*="content"]'])
            if not content_elem:
                content_elem = soup.body

            content = content_elem.get_text(separator='\n', strip=True) if content_elem else ""

            # Extract metadata
            meta_description = soup.find('meta', attrs={'name': 'description'})
            description = meta_description['content'] if meta_description else title

            post_data = {
                "title": title,
                "url": url,
                "content": content,
                "description": description,
                "scraped_at": datetime.now().isoformat(),
                "source": "blog",
                "post_number": post_number
            }

            return post_data

        except Exception as e:
            logger.error(f"Error scraping post {post_number} ({url}): {e}")
            return None

    def save_raw_posts(self, posts: list[dict]) -> Path:
        """Save raw scraped posts to file."""
        output_file = RAW_DATA_DIR / f"posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(posts, f, indent=2)
        logger.info(f"Saved {len(posts)} posts to {output_file}")
        return output_file


def scrape_and_save_posts(num_posts: int = settings.NUM_POSTS_TO_SCRAPE) -> list[dict]:
    """Convenience function to scrape and save posts."""
    scraper = WebScraper()
    posts = scraper.get_latest_posts(limit=num_posts)
    if posts:
        scraper.save_raw_posts(posts)
    return posts
