#!/usr/bin/env python3
"""
YouTube HD/4K Downloader
Downloads ONLY in HD quality (minimum 1080p, preferred 4K)
Refuses to download anything below 1080p
"""

import sys
import yt_dlp
import os

class HDQualityDownloader:
    """Downloads only HD quality videos (1080p minimum)"""

    def __init__(self, min_height=1080, preferred_height=2160):
        self.min_height = min_height
        self.preferred_height = preferred_height

    def check_quality(self, url):
        """Check if video has HD quality available"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'cookiesfrombrowser': ('chrome',),
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])

                # Get available video heights
                heights = sorted(
                    set(f.get('height') for f in formats if f.get('height')),
                    reverse=True
                )

                # Check if we have at least 1080p
                has_hd = any(h >= self.min_height for h in heights)

                return info.get('title', 'Unknown'), heights, has_hd

        except Exception as e:
            print(f"❌ Error checking quality: {e}")
            return None, [], False

    def download_hd(self, url, output_dir=None):
        """Download video in HD/4K quality ONLY"""

        if output_dir is None:
            output_dir = os.path.expanduser("~/Downloads")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # First check available quality
        print(f"\n🔍 Checking video quality...")
        title, available_heights, has_hd = self.check_quality(url)

        if not title:
            print("❌ Could not get video information")
            return False

        print(f"📹 Video: {title}")

        if available_heights:
            print(f"📊 Available qualities: {', '.join(f'{h}p' for h in available_heights[:5])}")

            # Get best available quality
            best_height = available_heights[0] if available_heights else 0

            if best_height < self.min_height:
                print(f"\n❌ QUALITY TOO LOW!")
                print(f"   Best available: {best_height}p")
                print(f"   Minimum required: {self.min_height}p (Full HD)")
                print(f"   This video doesn't meet quality requirements.")
                print(f"\n💡 Tip: The video might only be available in low quality, or")
                print(f"   you might need to be logged in to YouTube for HD access.")
                return False

            # Determine quality label
            quality_label = "8K" if best_height >= 4320 else \
                           "4K" if best_height >= 2160 else \
                           "1440p" if best_height >= 1440 else \
                           "1080p"

            print(f"✅ Quality check passed: {quality_label} ({best_height}p) available")

        # Configure download options for HD/4K only
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s [%(height)sp].%(ext)s'),

            # Format selection: ONLY 1080p or higher
            'format': (
                # Try 4K first
                'bestvideo[height>=2160][ext=mp4]+bestaudio[ext=m4a]/'
                'bestvideo[height>=2160]+bestaudio/'
                # Then 1440p
                'bestvideo[height>=1440][ext=mp4]+bestaudio[ext=m4a]/'
                'bestvideo[height>=1440]+bestaudio/'
                # Then 1080p (minimum acceptable)
                'bestvideo[height>=1080][ext=mp4]+bestaudio[ext=m4a]/'
                'bestvideo[height>=1080]+bestaudio/'
                # If nothing available in HD, fail
                'bestvideo[height>=1080]+bestaudio'
            ),

            'merge_output_format': 'mp4',
            'noplaylist': True,

            # Use browser cookies
            'cookiesfrombrowser': ('chrome',),

            # Network settings
            'retries': 10,
            'fragment_retries': 10,
            'concurrent_fragment_downloads': 4,
            'buffersize': 1024 * 1024,  # 1MB buffer for HD content

            # User agent
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            },

            # YouTube specific
            'extractor_args': {
                'youtube': {
                    'player_client': ['web', 'tv_embedded'],
                    'player_skip': ['webpage'],
                }
            },

            # Rate limiting
            'sleep_interval': 2,
            'max_sleep_interval': 5,

            # Verbose output
            'quiet': False,
            'no_warnings': False,
            'progress': True,
        }

        try:
            print(f"\n⬇️ Downloading in HD/4K quality...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

                if info:
                    actual_height = info.get('height', 0)
                    filesize = info.get('filesize', 0) or info.get('filesize_approx', 0)

                    if actual_height < self.min_height:
                        print(f"\n⚠️ WARNING: Downloaded quality ({actual_height}p) is below minimum!")
                        print(f"   File might be deleted or re-downloaded.")
                    else:
                        quality_label = "4K" if actual_height >= 2160 else \
                                       "1440p" if actual_height >= 1440 else \
                                       "1080p"

                        print(f"\n✅ Download completed successfully!")
                        print(f"📺 Quality: {quality_label} ({actual_height}p)")
                        if filesize:
                            print(f"💾 File size: {filesize / (1024*1024):.1f} MB")
                        print(f"📁 Saved to: {output_dir}")

                    return True

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            print(f"\n❌ Download failed: {error_msg}")

            if "Requested format is not available" in error_msg:
                print("\n⚠️ HD format not available. Possible solutions:")
                print("1. Make sure you're logged into YouTube in Chrome")
                print("2. The video might not have HD version")
                print("3. Try using a VPN if video is region-locked")

        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")

        return False

def batch_download_hd(urls, output_dir=None):
    """Download multiple videos in HD/4K only"""
    downloader = HDQualityDownloader()

    if output_dir is None:
        output_dir = os.path.expanduser("~/Downloads")

    total = len(urls)
    successful = []
    failed = []
    skipped = []

    print(f"\n{'='*60}")
    print(f"🎬 HD/4K BATCH DOWNLOAD")
    print(f"{'='*60}")
    print(f"Minimum quality: 1080p (Full HD)")
    print(f"Preferred quality: 4K")
    print(f"Videos: {total}")
    print(f"Output: {output_dir}")
    print(f"{'='*60}")

    for i, url in enumerate(urls, 1):
        print(f"\n{'─'*60}")
        print(f"📥 Video {i}/{total}")
        print(f"URL: {url}")
        print(f"{'─'*60}")

        # First check quality
        title, heights, has_hd = downloader.check_quality(url)

        if not has_hd:
            print(f"⏭️ SKIPPED - Quality too low (best: {heights[0]}p if heights else '?')")
            skipped.append(url)
            continue

        # Download if quality is acceptable
        if downloader.download_hd(url, output_dir):
            successful.append(url)
        else:
            failed.append(url)

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 DOWNLOAD SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {len(successful)}/{total}")
    print(f"❌ Failed: {len(failed)}/{total}")
    print(f"⏭️ Skipped (low quality): {len(skipped)}/{total}")

    if skipped:
        print(f"\n⏭️ Skipped URLs (quality below 1080p):")
        for url in skipped:
            print(f"   - {url}")

    if failed:
        print(f"\n❌ Failed URLs:")
        for url in failed:
            print(f"   - {url}")

    print(f"{'='*60}\n")

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='YouTube HD/4K Downloader - ONLY downloads 1080p or higher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quality Requirements:
  - Minimum: 1080p (Full HD)
  - Preferred: 4K (2160p)
  - Videos below 1080p will be SKIPPED

Examples:
  %(prog)s https://youtube.com/watch?v=xxx
  %(prog)s --batch url1 url2 url3
  %(prog)s --output ~/Desktop https://youtube.com/watch?v=xxx
  %(prog)s --min-quality 1440 https://youtube.com/watch?v=xxx
        """
    )

    parser.add_argument('url', nargs='?', help='YouTube URL')
    parser.add_argument('--batch', nargs='+', help='Multiple URLs')
    parser.add_argument('--output', '-o', help='Output directory')
    parser.add_argument('--min-quality', type=int, default=1080,
                       choices=[720, 1080, 1440, 2160],
                       help='Minimum acceptable quality (default: 1080)')

    args = parser.parse_args()

    # Create downloader with specified minimum quality
    downloader = HDQualityDownloader(min_height=args.min_quality)

    if args.batch:
        batch_download_hd(args.batch, args.output)
    elif args.url:
        success = downloader.download_hd(args.url, args.output)
        if not success:
            sys.exit(1)  # Exit with error code if download failed
    else:
        # Interactive mode
        print("🎬 YouTube HD/4K Downloader")
        print("=" * 50)
        print("⚠️  ONLY downloads 1080p or higher!")
        print("=" * 50)
        url = input("YouTube URL: ").strip()
        if url:
            downloader.download_hd(url)
        else:
            print("❌ No URL provided!")

if __name__ == "__main__":
    main()