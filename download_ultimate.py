#!/usr/bin/env python3
"""
Ultimate YouTube HD/4K Downloader
Multi-strategy approach for downloading HD/4K videos
"""

import yt_dlp
import os
import json
from pathlib import Path

class UltimateHDDownloader:
    """Ultimate downloader with multiple strategies for HD content"""

    def __init__(self):
        self.config_path = Path.home() / ".yt_downloader_ultimate.json"
        self.config = self.load_config()

    def load_config(self):
        """Load configuration"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def save_config(self):
        """Save configuration"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get_base_opts(self, output_dir):
        """Get base download options"""
        return {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'retries': 10,
            'fragment_retries': 10,
            'concurrent_fragment_downloads': 4,
            'quiet': False,
            'no_warnings': False,
            'progress': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Sec-Fetch-Mode': 'navigate',
            },
        }

    def strategy_1_cookies(self, url, output_dir):
        """Strategy 1: Use browser cookies with best format"""
        print("🍪 Strategy 1: Browser cookies with best format...")

        opts = self.get_base_opts(output_dir)
        opts.update({
            'format': 'bestvideo[height>=1080]+bestaudio/best[height>=1080]/best',
            'cookiesfrombrowser': ('chrome',),
        })

        return self.try_download(url, opts)

    def strategy_2_web_client(self, url, output_dir):
        """Strategy 2: Web client with specific format codes"""
        print("🌐 Strategy 2: Web client with format codes...")

        opts = self.get_base_opts(output_dir)
        opts.update({
            # Try specific format codes for HD
            # 137 = 1080p, 299/303 = 1080p60, 313 = 2160p
            'format': '313+140/299+140/137+140/303+140/22/best[height>=1080]',
            'cookiesfrombrowser': ('chrome',),
            'extractor_args': {
                'youtube': {
                    'player_client': ['web'],
                }
            },
        })

        return self.try_download(url, opts)

    def strategy_3_android(self, url, output_dir):
        """Strategy 3: Android client (may need PO token)"""
        print("📱 Strategy 3: Android client...")

        opts = self.get_base_opts(output_dir)
        opts.update({
            'format': 'best[height>=1080]/best',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                }
            },
        })

        # Add PO token if available
        if self.config.get('po_token'):
            opts['extractor_args']['youtube']['po_token'] = f"android.gvs+{self.config['po_token']}"

        return self.try_download(url, opts)

    def strategy_4_tv_embedded(self, url, output_dir):
        """Strategy 4: TV embedded client"""
        print("📺 Strategy 4: TV embedded client...")

        opts = self.get_base_opts(output_dir)
        opts.update({
            'format': 'best[height>=1080]',
            'cookiesfrombrowser': ('chrome',),
            'extractor_args': {
                'youtube': {
                    'player_client': ['tv_embedded'],
                }
            },
        })

        return self.try_download(url, opts)

    def strategy_5_ytdlp_auto(self, url, output_dir):
        """Strategy 5: Let yt-dlp figure it out automatically"""
        print("🤖 Strategy 5: Auto mode with quality filter...")

        opts = self.get_base_opts(output_dir)
        opts.update({
            'format': 'bv*[height>=1080]+ba/b[height>=1080]',
            'cookiesfrombrowser': ('chrome',),
        })

        return self.try_download(url, opts)

    def strategy_6_fallback_best(self, url, output_dir):
        """Strategy 6: Fallback to best available"""
        print("🔧 Strategy 6: Best available (may be <1080p)...")

        opts = self.get_base_opts(output_dir)
        opts.update({
            'format': 'best',
            'cookiesfrombrowser': ('chrome',),
        })

        return self.try_download(url, opts)

    def try_download(self, url, opts):
        """Try to download with given options"""
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if info:
                    height = info.get('height', 0)
                    format_note = info.get('format_note', '')
                    filesize = info.get('filesize', 0) or info.get('filesize_approx', 0)

                    if height >= 1080:
                        print(f"✅ SUCCESS! Downloaded in {height}p ({format_note})")
                        if filesize:
                            print(f"   File size: {filesize / (1024*1024):.1f} MB")
                        return True, height
                    else:
                        print(f"⚠️  Downloaded but quality is {height}p (below 1080p)")
                        return False, height
        except Exception as e:
            print(f"   ❌ Failed: {str(e)[:100]}...")
            return False, 0

    def download_hd(self, url, output_dir=None):
        """Download using all strategies until one works"""

        if output_dir is None:
            output_dir = os.path.expanduser("~/Downloads")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"\n" + "="*60)
        print("🎬 ULTIMATE HD/4K DOWNLOADER")
        print("="*60)
        print(f"📹 URL: {url}")
        print(f"📁 Output: {output_dir}")
        print(f"🎯 Target: 1080p minimum, 4K preferred")
        print("="*60 + "\n")

        # Try all strategies in order
        strategies = [
            self.strategy_1_cookies,
            self.strategy_2_web_client,
            self.strategy_3_android,
            self.strategy_4_tv_embedded,
            self.strategy_5_ytdlp_auto,
        ]

        for i, strategy in enumerate(strategies, 1):
            print(f"\n[{i}/5] Trying strategy...")
            success, height = strategy(url, output_dir)

            if success:
                print(f"\n" + "="*60)
                print(f"✅ DOWNLOAD SUCCESSFUL!")
                print(f"📺 Quality: {height}p")
                print(f"📁 Location: {output_dir}")
                print("="*60 + "\n")
                return True

        # Last resort - try best available even if <1080p
        print(f"\n⚠️  All HD strategies failed. Trying best available...")
        success, height = self.strategy_6_fallback_best(url, output_dir)

        if success or height > 0:
            if height < 1080:
                print(f"\n" + "="*60)
                print(f"⚠️  DOWNLOAD COMPLETED (LOW QUALITY)")
                print(f"📺 Quality: {height}p (below 1080p requirement)")
                print(f"📁 Location: {output_dir}")
                print(f"\n💡 Tips to get HD quality:")
                print(f"   1. Login to YouTube in Chrome")
                print(f"   2. Get a PO token (run with --setup-token)")
                print(f"   3. Try a different video")
                print(f"   4. Use a VPN")
                print("="*60 + "\n")
            return success

        print(f"\n" + "="*60)
        print(f"❌ DOWNLOAD FAILED")
        print(f"   All strategies exhausted.")
        print("="*60 + "\n")
        return False

    def setup_po_token(self):
        """Setup PO Token"""
        print("\n" + "="*60)
        print("🔑 PO TOKEN SETUP")
        print("="*60)
        print("\nA PO Token can help download HD videos.")
        print("See PO_TOKEN_ANLEITUNG.md for instructions.")
        print("\nEnter token (or press Enter to skip):")

        token = input("> ").strip()

        if token:
            # Clean token
            if token.startswith('android.gvs+'):
                token = token[12:]
            elif token.startswith('gvs+'):
                token = token[4:]

            self.config['po_token'] = token
            self.save_config()
            print("✅ Token saved!")
        else:
            print("⏭️  Skipped")

def main():
    """Main function"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Ultimate YouTube HD/4K Downloader - Multiple strategies for HD downloads'
    )

    parser.add_argument('url', nargs='?', help='YouTube URL')
    parser.add_argument('--output', '-o', help='Output directory')
    parser.add_argument('--setup-token', action='store_true', help='Setup PO Token')

    args = parser.parse_args()

    downloader = UltimateHDDownloader()

    if args.setup_token:
        downloader.setup_po_token()
    elif args.url:
        downloader.download_hd(args.url, args.output)
    else:
        # Interactive mode
        print("🎬 ULTIMATE HD/4K DOWNLOADER")
        print("="*50)
        url = input("YouTube URL: ").strip()
        if url:
            downloader.download_hd(url)

if __name__ == "__main__":
    main()