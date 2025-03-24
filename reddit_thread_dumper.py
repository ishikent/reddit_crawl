#!/usr/bin/env python3
"""
Reddit Thread Dumper - A tool to convert Reddit threads to Markdown format
"""

import argparse
import praw
import sys
import datetime


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


def main():
    """Main function to handle command-line arguments and process the Reddit thread"""
    parser = argparse.ArgumentParser(description="Dump a Reddit thread to Markdown.")
    parser.add_argument("reddit_url", help="The URL of the Reddit thread to dump.")
    args = parser.parse_args()

    reddit = praw.Reddit(
        read_only=True,  # Read-only mode as per specs
    )

    try:
        submission = reddit.submission(url=args.reddit_url)
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
