"""Exercise the actual release-scan expression with synthetic tracked files."""
from pathlib import Path
import subprocess
import tempfile
import unittest


class PublicScanTests(unittest.TestCase):
    def test_password_values_are_distinguished_from_runtime_prompt(self):
        script = (Path(__file__).resolve().parents[1] /
                  "scripts/public-sanity-check.sh").read_text()
        line = next(line for line in script.splitlines()
                    if "git grep -I -l -E " in line)
        expression = line.split("-E ", 1)[1].rstrip().removesuffix("\\").strip()
        fixtures = {
            "prompt.py": "def read(password=None):\n"
                         "    password = getpass.getpass('Archive password: ').encode()\n"
                         "    password=getpass.getpass()\n",
            "double.txt": 'password = "synthetic-fixture"\n',
            "single.txt": "password: 'synthetic-fixture'\n",
            "yaml.txt": "  password: synthetic-fixture\n",
            "env.txt": "password=synthetic-fixture\n",
            "ini.txt": "password = synthetic-fixture\n",
            "ini-comment.txt": "  password\t=\tsynthetic-fixture  ; example\n",
            "token.txt": "ghp_" + "a" * 24 + "\n",
        }
        with tempfile.TemporaryDirectory() as temp:
            subprocess.run(["git", "init", "-q", temp], check=True)
            for name, body in fixtures.items():
                (Path(temp) / name).write_text(body)
            subprocess.run(["git", "-C", temp, "add", "."], check=True)
            result = subprocess.run(
                ["bash", "-c", "git grep -I -l -E " + expression],
                cwd=temp, text=True, capture_output=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(set(result.stdout.splitlines()),
                             set(fixtures) - {"prompt.py"})
