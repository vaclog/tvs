import os
import signal
import sys
import tempfile
import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


URLS = [
    "https://vots20.vaclog.com/modulos/tv/tableros/tablero_tv.php",
    "https://vots20.vaclog.com/modulos/tv/terminales/terminales_v2.php",
    "https://vots20.vaclog.com/modulos/tv/ofic/ofic.php",
]
DEFAULT_INTERVAL_SECONDS = 45
PAGE_LOAD_TIMEOUT_MS = 30_000
BROWSER_ARGS = [
    "--kiosk",
    "--start-fullscreen",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-notifications",
    "--disable-infobars",
    "--disable-session-crashed-bubble",
    "--disable-features=Translate,BackForwardCache",
    "--disable-blink-features=AutomationControlled",
]


def get_interval_seconds() -> int:
    raw_value = os.getenv("TV_ROTATION_INTERVAL", str(DEFAULT_INTERVAL_SECONDS))
    try:
        interval = int(raw_value)
    except ValueError as exc:
        raise ValueError("TV_ROTATION_INTERVAL debe ser un entero positivo.") from exc

    if interval <= 0:
        raise ValueError("TV_ROTATION_INTERVAL debe ser mayor que 0.")

    return interval


def install_signal_handlers(stop_callback) -> None:
    def handle_stop(signum, _frame):
        print(f"Senal recibida ({signum}). Cerrando navegador...", flush=True)
        stop_callback()

    for signal_name in ("SIGINT", "SIGTERM"):
        if hasattr(signal, signal_name):
            signal.signal(getattr(signal, signal_name), handle_stop)


def open_pages(context, urls: list[str]):
    pages = []
    for index, url in enumerate(urls):
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=PAGE_LOAD_TIMEOUT_MS)
        enforce_fullscreen(page)
        pages.append(page)
        if index == 0:
            print(f"Pagina inicial cargada: {url}", flush=True)
        else:
            print(f"Pagina adicional cargada: {url}", flush=True)
    return pages


def enforce_fullscreen(page) -> None:
    # F11 fuerza fullscreen del navegador; el script JS es respaldo dentro del documento.
    page.bring_to_front()
    page.keyboard.press("F11")
    time.sleep(1)
    page.evaluate(
        """
        () => {
            const element = document.documentElement;
            if (document.fullscreenElement || !element.requestFullscreen) {
                return;
            }
            return element.requestFullscreen().catch(() => null);
        }
        """
    )


def main() -> int:
    interval_seconds = get_interval_seconds()
    stopped = False

    def request_stop():
        nonlocal stopped
        stopped = True

    install_signal_handlers(request_stop)

    try:
        with sync_playwright() as playwright:
            user_data_dir = tempfile.mkdtemp(prefix="tvs-playwright-")
            context = playwright.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                channel="chrome",
                headless=False,
                no_viewport=True,
                args=BROWSER_ARGS,
            )
            pages = open_pages(context, URLS)

            print(
                f"Rotando {len(pages)} paginas cada {interval_seconds} segundos.",
                flush=True,
            )

            while not stopped:
                for page in pages:
                    if stopped:
                        break

                    page.bring_to_front()
                    enforce_fullscreen(page)
                    time.sleep(interval_seconds)

            context.close()
            return 0
    except PlaywrightTimeoutError as exc:
        print(f"Timeout cargando una pagina: {exc}", file=sys.stderr, flush=True)
    except Exception as exc:  # noqa: BLE001
        print(f"Error ejecutando la rotacion de TV: {exc}", file=sys.stderr, flush=True)

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
