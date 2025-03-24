#!/usr/bin/env python3
"""
Reddit Thread Dumper - A tool to convert Reddit threads to Markdown format
"""

import argparse
import praw
import sys
import datetime
from urllib.parse import urlparse


def submission_to_markdown(submission):
    """Convert a Reddit submission to Markdown format"""
    timestamp = datetime.datetime.fromtimestamp(submission.created_utc)
    md = f"# {submission.title}\n\n"
    md += f"* **Posted by:** {submission.author}\n"
    md += f"* **Date:** {timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
    md += f"* **Score:** {submission.score}\n"
    md += f"* **URL:** {submission.url}\n"

    if submission.selftext:
        md += f"\n{submission.selftext}\n\n"
    return md


def comment_to_markdown(comment, level=0):
    """Convert a Reddit comment to Markdown format, recursively handling replies"""
    indent = "  " * level
    if comment.author is None:
        author_string = "[deleted]"
    else:
        author_string = str(comment.author)

    timestamp = datetime.datetime.fromtimestamp(comment.created_utc)
    md = f"{indent}* **{author_string}** ({comment.score}) *{timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}*\n"
    md += f"{indent}  {comment.body}\n\n"

    for reply in comment.replies:
        if isinstance(reply, praw.models.MoreComments):
            md += f"{indent}  *More comments... (not loaded)*\n"
            continue
        md += comment_to_markdown(reply, level + 1)
    return md


def is_valid_reddit_url(url):
    """Checks if the given URL is a valid Reddit submission URL."""
    try:
        parsed_url = urlparse(url)
        return (parsed_url.netloc in ["www.reddit.com", "reddit.com", "old.reddit.com"] and 
                "/comments/" in parsed_url.path)
    except:
        return False


def main():
    """Main function to handle command-line arguments and process the Reddit thread"""
    parser = argparse.ArgumentParser(description="Dump a Reddit thread to Markdown.")
    parser.add_argument("reddit_url", help="The URL of the Reddit thread to dump.")
    args = parser.parse_args()

    # Validate the URL before proceeding
    if not is_valid_reddit_url(args.reddit_url):
        print(f"Error: Invalid Reddit URL: {args.reddit_url}", file=sys.stderr)
        print("URL must be a valid Reddit thread URL (e.g., https://www.reddit.com/r/subreddit/comments/...)", 
              file=sys.stderr)
        sys.exit(1)

    reddit = praw.Reddit(
        read_only=True,  # Read-only mode as per specs
    )

    try:
        submission = reddit.submission(url=args.reddit_url)
        # Try to access a property to verify the submission exists
        _ = submission.title
    except praw.exceptions.ClientException as e:
        print(f"Error: Invalid Reddit URL format: {e}", file=sys.stderr)
        sys.exit(1)
    except praw.exceptions.PRAWException as e:
        print(f"Error: Reddit API error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: Could not retrieve submission from URL: {e}", file=sys.stderr)
        sys.exit(1)

    markdown = submission_to_markdown(submission)
    submission.comments.replace_more(limit=0)  # Don't load any MoreComments at the top level
    for comment in submission.comments:
        markdown += comment_to_markdown(comment)
    print(markdown)


if __name__ == "__main__":
    main()
