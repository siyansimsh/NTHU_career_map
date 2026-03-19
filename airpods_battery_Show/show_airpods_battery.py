"""
AirPods 4 Battery Monitor — Windows 系統匣電量監控工具
透過掃描 BLE 廣播封包解析 AirPods 左耳/右耳電量，
並在工作列右下角（系統匣）即時顯示。
需求：Windows 10+、Python 3.8+、winsdk、pystray、Pillow
"""

import asyncio
import threading
from winsdk.windows.devices.bluetooth.advertisement import (
    BluetoothLEAdvertisementWatcher,
    BluetoothLEScanningMode,
)
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw, ImageFont

# ── 設定 ───────────────────────────────────────────
SCAN_DURATION = 2            # 每次掃描秒數
UPDATE_INTERVAL = 5          # 電量更新間隔（秒）
# ───────────────────────────────────────────────────

APPLE_COMPANY_ID = 0x004C
stop_event = threading.Event()


def _parse_battery(data: bytes) -> tuple[int | None, int | None]:
    """解析 AirPods BLE 廣播封包，回傳 (left%, right%)。"""
    if len(data) < 27 or data[0] != 0x07 or data[1] != 0x19:
        return None, None

    payload = data[2:]
    if payload[0] != 0x01:
        return None, None

    flip = bool(payload[3] & 0x02)
    raw_a = (payload[4] >> 4) & 0xF
    raw_b = payload[4] & 0xF
    raw_left = raw_b if flip else raw_a
    raw_right = raw_a if flip else raw_b

    def to_pct(v):
        return None if v == 15 else v * 10

    return to_pct(raw_left), to_pct(raw_right)


def get_airpods_battery() -> tuple[int | None, int | None]:
    """掃描 BLE 廣播，回傳 (left%, right%) 或 (None, None)。"""
    results: list[bytes] = []

    def on_received(sender, args):
        for section in args.advertisement.manufacturer_data:
            if section.company_id == APPLE_COMPANY_ID:
                raw = bytes(section.data)
                if len(raw) >= 27 and raw[0] == 0x07 and raw[1] == 0x19:
                    results.append(raw)

    async def scan():
        watcher = BluetoothLEAdvertisementWatcher()
        watcher.scanning_mode = BluetoothLEScanningMode.ACTIVE
        watcher.add_received(on_received)
        watcher.start()
        await asyncio.sleep(SCAN_DURATION)
        watcher.stop()

    asyncio.run(scan())
    return _parse_battery(results[-1]) if results else (None, None)


# ── 圖示繪製 ──────────────────────────────────────

def _pick_color(level: int | None):
    if level is None:
        return (100, 100, 100, 230)
    if level <= 15:
        return (220, 50, 50, 230)
    if level <= 40:
        return (220, 160, 30, 230)
    return (50, 180, 50, 230)


def create_icon_image(left: int | None, right: int | None):
    """產生 64×64 系統匣圖示：顯示較低電量的數字，依電量變色。"""
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    vals = [v for v in (left, right) if v is not None]
    min_level = min(vals) if vals else None
    text = str(min_level) if min_level is not None else "--"
    fill = _pick_color(min_level)

    draw.rounded_rectangle([4, 4, 60, 60], radius=8, fill=fill)

    try:
        font_size = 28 if len(text) <= 2 else 22
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((64 - tw) // 2, (64 - th) // 2 - 2),
              text, fill=(255, 255, 255), font=font)
    return img


def _build_title(left: int | None, right: int | None) -> str:
    if left is None and right is None:
        return "AirPods 4: 未連線"
    parts = []
    if left is not None:
        parts.append(f"L:{left}%")
    if right is not None:
        parts.append(f"R:{right}%")
    return "AirPods " + " | ".join(parts)


# ── 更新邏輯 ──────────────────────────────────────

def update_battery(icon):
    left, right = get_airpods_battery()
    icon.title = _build_title(left, right)
    icon.icon = create_icon_image(left, right)


def update_loop(icon):
    while not stop_event.is_set():
        update_battery(icon)
        stop_event.wait(UPDATE_INTERVAL)


def on_refresh(icon, item):
    threading.Thread(target=update_battery, args=(icon,), daemon=True).start()


def on_exit(icon, item):
    stop_event.set()
    icon.stop()


def main():
    menu = Menu(
        MenuItem('重新整理', on_refresh),
        Menu.SEPARATOR,
        MenuItem('退出', on_exit),
    )
    icon = Icon(
        "AirPodsMonitor",
        create_icon_image(None, None),
        "AirPods Battery Monitor",
        menu,
    )

    thread = threading.Thread(target=update_loop, args=(icon,), daemon=True)
    thread.start()

    icon.run()


if __name__ == "__main__":
    main()