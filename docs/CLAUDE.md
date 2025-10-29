# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an empty YouTube downloader project directory. The user wants to create a simple tool for downloading YouTube videos. The project currently contains only Claude configuration files.

## Development Setup

Since this is a new project, the following tools and approaches should be considered:

- **Python with yt-dlp**: Most common and reliable approach for YouTube downloading
- **Node.js with ytdl-core**: JavaScript-based alternative
- **Simple CLI script**: Quick and straightforward implementation

## Project Structure

The repository is currently empty except for:
- `.claude/settings.local.json`: Claude permissions configuration

## Recommended Implementation

When implementing the YouTube downloader:

1. Choose between Python (yt-dlp) or Node.js (ytdl-core) based on user preference
2. Create a simple CLI interface for ease of use
3. Include basic error handling for invalid URLs and network issues
4. Support common video formats and quality options
5. Add progress indicators for download status

## Notes

- The user prefers simplicity over complex features
- Consider looking for existing GitHub repositories before writing from scratch
- German is the user's primary language (evident from their request)