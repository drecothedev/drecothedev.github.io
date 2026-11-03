"""Regression checks for the retired generator and clean static export.

Every command runs in a temporary project copy, never against canonical source.
Run: python3 scripts/test_build_workflows.py
"""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Elements(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.elements = []
        self.feed(html)

    def handle_starttag(self, tag, attributes):
        self.elements.append((tag, dict(attributes)))


def snapshot(root):
    return {
        path.relative_to(root).as_posix(): sha256(path.read_bytes()).hexdigest()
        for path in root.rglob('*')
        if path.is_file() and '__pycache__' not in path.parts
    }


class BuildWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='portfolio-build-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(
            ROOT/'submission/ActivityWebserver',
            self.root/'submission/ActivityWebserver',
            ignore=shutil.ignore_patterns('__pycache__', '.DS_Store'),
        )
        (self.root/'scripts').mkdir()
        for name in ['build_milestone2.py', 'export_milestone2_preview.py', 'verify_milestone2.py']:
            shutil.copy2(ROOT/'scripts'/name, self.root/'scripts'/name)

    def run_script(self, name):
        return subprocess.run(
            [sys.executable, '-B', str(self.root/'scripts'/name)],
            cwd=self.root, capture_output=True, text=True, timeout=60,
        )

    def test_retired_generator_leaves_source_unchanged_and_app_working(self):
        before = snapshot(self.root)
        result = self.run_script('build_milestone2.py')
        self.assertNotEqual(result.returncode, 0, 'Retired generator must not report success')
        self.assertIn('Retired:', result.stderr)
        self.assertIn('scripts/export_milestone2_preview.py', result.stderr)
        self.assertEqual(before, snapshot(self.root), 'Retired generator wrote files')
        result = self.run_script('verify_milestone2.py')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_clean_export_creates_folders_and_valid_links(self):
        output = self.root/'portfolio/dist'
        self.assertFalse(output.exists())
        source_before = snapshot(self.root/'submission/ActivityWebserver')
        result = self.run_script('export_milestone2_preview.py')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue((output/'assets').is_dir())
        self.assertEqual(source_before, snapshot(self.root/'submission/ActivityWebserver'))
        self.assertTrue((output/'spotlight.js').is_file())
        self.assertTrue((output/'styles.css').is_file())

        expected = {
            'index.html', 'products.html', 'products-apps.html',
            'products-languages.html', 'products-learning.html',
            'details.html', 'cart.html', 'current-project.html',
        }
        self.assertEqual(expected, {path.name for path in output.glob('*.html')})
        responsive_candidates = 0
        for page in output.glob('*.html'):
            for tag, attributes in Elements(page.read_text()).elements:
                urls = [attributes[key] for key in ['href', 'src', 'action'] if key in attributes]
                for candidate in attributes.get('srcset', '').split(','):
                    if candidate.strip():
                        urls.append(candidate.strip().split()[0])
                        responsive_candidates += 1
                for url in urls:
                    parsed = urlsplit(url)
                    if parsed.scheme or parsed.netloc or not parsed.path:
                        continue
                    self.assertFalse(parsed.path.startswith('/'), (page.name, url))
                    target = (page.parent/unquote(parsed.path)).resolve()
                    self.assertTrue(target.is_relative_to(output.resolve()), (page.name, url))
                    self.assertTrue(target.is_file(), (page.name, url))
        self.assertGreater(responsive_candidates, 0, 'No responsive images were checked')
        # A second export must also work when output directories already exist.
        first_output = snapshot(output)
        result = self.run_script('export_milestone2_preview.py')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(first_output, snapshot(output))


if __name__ == '__main__':
    unittest.main(verbosity=2)
