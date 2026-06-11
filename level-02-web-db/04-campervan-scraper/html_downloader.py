"""
Module: html_downloader.py
Description: Uses undetected-chromedriver to patch browser binaries dynamically,
             evading deep JavaScript variable inspection from enterprise WAFs.
"""
import sys
import types

# --- MONKEYPATCH FOR PYTHON 3.12+ / 3.14 COMPATIBILITY ---
# Mocking the extinct distutils.version.LooseVersion to prevent third-party crashes
class LegacyLooseVersion:
    def __init__(self, vstring):
        self.vstring = vstring
        # Convert the version string into a comparable tuple of integers
        self.version = tuple(int(x) for x in vstring.split('.') if x.isdigit())
    def __str__(self): return self.vstring
    def __repr__(self): return f"LooseVersion('{self.vstring}')"
    def __lt__(self, other): return self.version < other.version
    def __le__(self, other): return self.version <= other.version
    def __eq__(self, other): return self.version == other.version
    def __gt__(self, other): return self.version > other.version
    def __ge__(self, other): return self.version >= other.version

# Inject fake module structures directly into the global system modules runtime cache
distutils_mock = types.ModuleType("distutils")
version_mock = types.ModuleType("version")
version_mock.LooseVersion = LegacyLooseVersion
distutils_mock.version = version_mock

sys.modules["distutils"] = distutils_mock
sys.modules["distutils.version"] = version_mock
# ---------------------------------------------------------

# Now the library import will execute smoothly without throwing ModuleNotFoundError
import undetected_chromedriver as uc
import time

import undetected_chromedriver as uc
import time

class AutomatedHtmlDownloader:
    """
    Handles stealth browser automation by patching standard ChromeDriver signatures.
    """

    def __init__(self):
        self.options = uc.ChromeOptions()
        # Mantenemos un tamaño de ventana estándar, dejamos que uc maneje el resto
        self.options.add_argument("--window-size=1280,800")

    def save_page_to_local(self, url: str, output_path: str) -> bool:
        """
        Launches the stealth browser, navigates to the target, and dumps the DOM.
        """
        print(f"[*] Launching stealth browser session for: {url}")
        driver = None
        
        try:
            # uc.Chrome automatically patches the executable to hide cdc_ variables
            driver = uc.Chrome(options=self.options)
            driver.get(url)
            
            # Esperamos 6 segundos para que el WAF evalúe el navegador y cargue la red
            time.sleep(6)
            
            html_content = driver.page_source
            
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(html_content)
                
            print(f"[+] Web page successfully cloned locally to: {output_path}")
            return True
            
        except Exception as e:
            print(f"[!] Stealth automation failed during execution: {e}")
            return False
        finally:
            if driver:
                driver.quit()