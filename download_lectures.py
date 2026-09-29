import subprocess
import sys
import os
import re
import json
import time

# Ensure UTF-8 output in Windows terminal
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 72)
    print("  🚀 ULTRA-FAST TELEGRAM LECTURE DOWNLOADER (OFFLINE ACCESS)")
    print("  ⚡ 16x Speed | Chronological Upload Ordering | Auto-Resume")
    print("=" * 72)
    print()

def run_cmd(cmd):
    return subprocess.call(cmd, shell=True)

def check_login():
    res = subprocess.run([".\\tdl.exe", "chat", "ls"], capture_output=True, text=True)
    return res.returncode == 0

def login():
    clear_screen()
    print_header()
    print("[1/2] TELEGRAM LOGIN REQUIRED")
    print("Choose how you want to log in to Telegram:")
    print("  1. QR Code Scan (Fastest & Easiest - scan from Telegram on your phone)")
    print("  2. Phone Number (SMS / Telegram App login code)")
    print("  3. Use Telegram Desktop session (if you have Telegram Desktop installed)")
    print()
    choice = input("Enter choice (1, 2, or 3) [Default 1]: ").strip() or "1"
    
    if choice == "1":
        print("\nOpening QR code... Scan it using Telegram on your phone:")
        print("Settings -> Devices -> Link Desktop Device\n")
        run_cmd(".\\tdl.exe login -T qr")
    elif choice == "2":
        run_cmd(".\\tdl.exe login -T code")
    else:
        run_cmd(".\\tdl.exe login -T desktop")

def load_channels():
    channels = []
    try:
        out = subprocess.check_output([".\\tdl.exe", "chat", "ls"], encoding='utf-8', errors='replace')
        lines = out.strip().splitlines()
        for line in lines[1:]:
            parts = line.split(maxsplit=4)
            if len(parts) >= 3:
                chat_id = parts[0].strip()
                chat_type = parts[1].strip()
                chat_name = parts[2].strip()
                username = parts[3].strip() if len(parts) > 3 else "-"
                if chat_type in ["channel", "group"]:
                    channels.append({
                        "id": chat_id,
                        "type": chat_type,
                        "name": chat_name,
                        "username": username,
                        "raw": line
                    })
    except Exception as e:
        print(f"Error loading chats: {e}")
    return channels

def select_channel():
    channels = load_channels()
    
    while True:
        clear_screen()
        print_header()
        print("CHOOSE HOW TO SELECT YOUR CHANNEL / LECTURE GROUP:")
        print("  1. 🔍 Search your channels by name (e.g., 'Vision', 'UPSC', 'Lectures')")
        print("  2. 📋 View your recent joined channels list")
        print("  3. 🔢 Enter Channel ID directly (e.g., 2591516735)")
        print("  4. 🔗 Paste a Message Link (from inside channel: right-click post -> Copy Link)")
        print("  5. 🌐 Enter Public Channel Username (e.g., @channelname)")
        print("-" * 72)
        
        opt = input("Enter option (1-5) [Default 1]: ").strip() or "1"
        
        if opt == "1":
            keyword = input("\n👉 Enter search word (e.g. vision, upsc, ncert, net, lecture, etc.): ").strip().lower()
            if not keyword:
                continue
            matches = [c for c in channels if keyword in c['name'].lower() or keyword in c['username'].lower()]
            if not matches:
                print(f"\n❌ No channels found matching '{keyword}'.")
                input("Press Enter to try again...")
                continue
            print(f"\nFound {len(matches)} matching channel(s):")
            for idx, c in enumerate(matches[:25], 1):
                uname_str = f" (@{c['username']})" if c['username'] != '-' else ""
                print(f"  [{idx}] {c['name']}{uname_str}  [ID: {c['id']}]")
            
            sel = input("\nEnter number to download (or 'b' to back): ").strip()
            if sel.lower() == 'b':
                continue
            try:
                sel_idx = int(sel) - 1
                if 0 <= sel_idx < len(matches):
                    return matches[sel_idx]['id'], matches[sel_idx]['name']
            except ValueError:
                pass
            print("Invalid selection.")
            input("Press Enter to continue...")

        elif opt == "2":
            print(f"\nShowing your top 20 recent channels/groups:")
            for idx, c in enumerate(channels[:20], 1):
                uname_str = f" (@{c['username']})" if c['username'] != '-' else ""
                print(f"  [{idx:2d}] {c['name']}{uname_str}  [ID: {c['id']}]")
            sel = input("\nEnter number to download (or 'b' to back): ").strip()
            if sel.lower() == 'b':
                continue
            try:
                sel_idx = int(sel) - 1
                if 0 <= sel_idx < len(channels[:20]):
                    return channels[sel_idx]['id'], channels[sel_idx]['name']
            except ValueError:
                pass
            print("Invalid selection.")
            input("Press Enter to continue...")

        elif opt == "3":
            cid = input("\n👉 Enter numeric Channel ID: ").strip()
            if cid.isdigit():
                return cid, f"Channel_{cid}"
            print("❌ ID must be numbers only.")
            input("Press Enter to continue...")

        elif opt == "4":
            link = input("\n👉 Paste Message Link (e.g., https://t.me/c/1234567890/100): ").strip()
            m = re.search(r't\.me/c/(\d+)', link)
            if m:
                cid = m.group(1)
                return cid, f"Channel_{cid}"
            elif "+mbfQ" in link or "t.me/+" in link or "joinchat" in link:
                print("\n⚠️ Note: 't.me/+' is an invite link.")
                print("Since you already joined the group, please open Telegram, right-click ANY")
                print("video/message in the group, click 'Copy Link', and paste THAT link here!")
                input("Press Enter to continue...")
            else:
                print("❌ Invalid message link format.")
                input("Press Enter to continue...")

        elif opt == "5":
            uname = input("\n👉 Enter public username (e.g. @mychannel): ").strip()
            if uname:
                clean_uname = uname.replace("@", "").replace("https://t.me/", "")
                return clean_uname, clean_uname

def organize_and_renumber(download_dir, export_json):
    """
    Renumbers all downloaded files by their strict uploaded chronological order.
    Example: 001_Lecture_Name.mp4, 002_Lecture_Name.mp4, etc.
    Also creates a playable M3U playlist file for VLC / Windows Media Player.
    """
    if not os.path.exists(export_json):
        return

    try:
        with open(export_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        messages = data.get('messages', [])
        # Sort chronologically by Message ID (Oldest uploaded lecture -> Newest uploaded lecture)
        messages.sort(key=lambda m: m['id'])
        
        total_files = len(messages)
        pad_width = 3 if total_files < 1000 else 4
        
        # Build mapping: message_id -> sequential order number
        id_to_seq = {m['id']: i + 1 for i, m in enumerate(messages)}
        id_to_filename = {m['id']: m.get('file', '') for m in messages}

        print("\n" + "-" * 72)
        print("🔢 RENUMBERING LECTURES BY UPLOAD SEQUENCE...")
        print("-" * 72)

        playlist_entries = []
        renamed_count = 0

        # Scan files in directory
        for fname in os.listdir(download_dir):
            if fname.endswith(".tmp") or fname.startswith("000_"):
                continue
            
            # Check if file starts with <message_id>_
            match = re.match(r'^(\d+)_(.+)$', fname)
            if match:
                msg_id = int(match.group(1))
                orig_name = match.group(2)
                
                if msg_id in id_to_seq:
                    seq_num = id_to_seq[msg_id]
                    prefix = f"{seq_num:0{pad_width}d}"
                    new_name = f"{prefix}_{orig_name}"
                    
                    old_path = os.path.join(download_dir, fname)
                    new_path = os.path.join(download_dir, new_name)
                    
                    if old_path != new_path:
                        try:
                            # If target already exists, remove it first
                            if os.path.exists(new_path):
                                os.remove(new_path)
                            os.rename(old_path, new_path)
                            renamed_count += 1
                        except Exception as e:
                            print(f"Warning: Could not rename {fname}: {e}")

        # Build M3U Playlist & Index for easy 1-click playback of all lectures
        all_downloaded = sorted([f for f in os.listdir(download_dir) if not f.startswith("000_") and not f.endswith(".tmp")])
        
        playlist_path = os.path.join(download_dir, "000_PLAY_ALL_LECTURES_IN_ORDER.m3u")
        index_path = os.path.join(download_dir, "000_LECTURE_INDEX.txt")

        with open(playlist_path, "w", encoding="utf-8") as pl:
            pl.write("#EXTM3U\n")
            for f in all_downloaded:
                if f.lower().endswith(('.mp4', '.mkv', '.avi', '.webm', '.ts', '.mp3', '.m4a')):
                    pl.write(f"{f}\n")

        with open(index_path, "w", encoding="utf-8") as idx_f:
            idx_f.write("=" * 72 + "\n")
            idx_f.write("  CHRONOLOGICAL LECTURE INDEX (ORDERED BY UPLOAD DATE)\n")
            idx_f.write("=" * 72 + "\n\n")
            for f in all_downloaded:
                idx_f.write(f"• {f}\n")

        print(f"✅ Renumbered {renamed_count} lecture file(s) by upload order!")
        print(f"🎵 Created 1-Click Offline Playlist : {playlist_path}")
        print(f"📄 Created Complete Lecture Index   : {index_path}")

    except Exception as e:
        print(f"Notice during renumbering: {e}")

def ensure_tdl():
    if not os.path.exists("tdl.exe"):
        print("📦 'tdl' engine not found. Downloading automatically for Windows...")
        try:
            import urllib.request, zipfile, io
            url = 'https://github.com/iyear/tdl/releases/latest/download/tdl_Windows_64bit.zip'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req).read()
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                z.extractall('.')
            print("✅ 'tdl' downloaded and extracted successfully!\n")
        except Exception as e:
            print(f"❌ Failed to download tdl automatically: {e}")
            input("Press Enter to exit...")
            sys.exit(1)

def main():
    clear_screen()
    print_header()
    
    ensure_tdl()

    # Check login
    if not check_login():
        print("⚠️ You are not logged in yet.")
        login()
        if not check_login():
            print("\n❌ Login was not completed. Please try again.")
            input("Press Enter to exit...")
            return

    channel_id, channel_name = select_channel()

    clear_screen()
    print_header()
    print(f"🎯 Selected Channel: {channel_name} (ID: {channel_id})")
    print("-" * 72)
    print("\nSelect what you want to download:")
    print("  1. Everything (All Lecture Videos, Notes, PDFs, Audios, Files)")
    print("  2. Only Videos (mp4, mkv, avi, webm, ts)")
    print("  3. Only PDFs & Documents (pdf, doc, docx, ppt, pptx, zip)")
    file_choice = input("\nEnter choice (1, 2, or 3) [Default 1]: ").strip() or "1"

    include_filter = ""
    if file_choice == "2":
        include_filter = "-i mp4,mkv,avi,webm,ts"
    elif file_choice == "3":
        include_filter = "-i pdf,doc,docx,ppt,pptx,zip,rar"

    # Clean channel folder name
    safe_name = re.sub(r'[\\/*?:"<>|]', "", channel_name).strip()[:35] or f"channel_{channel_id}"
    download_dir = os.path.join(os.getcwd(), "Lectures", safe_name)
    os.makedirs(download_dir, exist_ok=True)

    export_json = f"export_{channel_id}.json"

    clear_screen()
    print_header()
    print(f"📁 Target Folder : {download_dir}")
    print(f"📢 Channel       : {channel_name} [ID: {channel_id}]")
    print(f"⚡ Speed Engine   : 16 Parallel Threads (High Speed DC Pool)")
    print(f"🔢 Sequence Mode : Chronological Upload Order (001_..., 002_...)")
    print("-" * 72)
    print("\n⏳ Step 1: Scanning channel messages and preparing download list...")
    
    export_cmd = f'.\\tdl.exe chat export -c "{channel_id}" -o "{export_json}"'
    ret = run_cmd(export_cmd)
    
    # Template: {{ .MessageID }}_{{ filenamify .FileName }}
    # This prefixes each file with its Telegram Message ID so we can order chronologically
    template_flag = '--template "{{ .MessageID }}_{{ filenamify .FileName }}"'

    if ret != 0 or not os.path.exists(export_json) or os.path.getsize(export_json) == 0:
        print("\n❌ Could not export chat list. Starting direct link download...")
        dl_cmd = f'.\\tdl.exe dl -u "https://t.me/c/{channel_id}/1" -d "{download_dir}" {template_flag} -t 16 -l 4 --continue --skip-same {include_filter}'
    else:
        print("\n✅ Channel scanned successfully! Starting high-speed download...")
        dl_cmd = f'.\\tdl.exe dl -f "{export_json}" -d "{download_dir}" {template_flag} -t 16 -l 4 --continue --skip-same {include_filter}'

    # Download with Auto-Resume Loop
    print("\n" + "=" * 72)
    print("⬇️  DOWNLOADING LECTURES NOW (MAX SPEED - 16 THREADS)")
    print("💡 If your Wi-Fi flickers, the script will automatically pause & resume!")
    print("=" * 72 + "\n")
    
    while True:
        res = run_cmd(dl_cmd)
        if res == 0:
            print("\n" + "=" * 72)
            print("🎉 ALL LECTURES DOWNLOADED SUCCESSFULLY!")
            print(f"📂 Folder: {download_dir}")
            
            # Renumber all lectures by upload sequence (001_, 002_, 003_...)
            organize_and_renumber(download_dir, export_json)
            
            print("\n" + "=" * 72)
            print("👉 You can now disconnect from Wi-Fi completely!")
            print("👉 Double-click '000_PLAY_ALL_LECTURES_IN_ORDER.m3u' to play all lectures in VLC!")
            print("=" * 72)
            break
        else:
            print("\n⚠️ Download paused or connection hiccup.")
            # Run intermediate renumbering for already completed files
            organize_and_renumber(download_dir, export_json)
            print("🔄 Auto-resuming in 4 seconds... (Press Ctrl+C to cancel)")
            try:
                time.sleep(4)
            except KeyboardInterrupt:
                print("\nDownload stopped by user.")
                organize_and_renumber(download_dir, export_json)
                break

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
