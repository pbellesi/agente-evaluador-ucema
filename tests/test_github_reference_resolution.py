import io
import sys
import types
import unittest
import zipfile
from unittest.mock import patch
from urllib.parse import unquote

# Las pruebas reemplazan requests por un fake local y no deben usar red.
if "requests" not in sys.modules:
    requests_stub = types.ModuleType("requests")
    requests_stub.get = lambda *args, **kwargs: (_ for _ in ()).throw(
        AssertionError("La prueba unitaria no debe usar red")
    )
    sys.modules["requests"] = requests_stub

from src.evaluator_engine import run_evaluation
from src.github_fetcher import fetch_repository_data, parse_github_url
from src.schema import EvaluationResult


class FakeResponse:
    def __init__(self, status_code, payload=None, content=b""):
        self.status_code = status_code
        self._payload = payload or {}
        self.content = content

    def json(self):
        return self._payload


def archive_bytes():
    payload = io.BytesIO()
    with zipfile.ZipFile(payload, "w") as archive:
        archive.writestr("fixture-root/README.md", "# Repositorio sintético\n")
    return payload.getvalue()


class FakeGitHub:
    def __init__(self, default_branch, references):
        self.default_branch = default_branch
        self.references = references
        self.calls = []
        self.archive = archive_bytes()

    def get(self, url, timeout):
        self.calls.append(url)
        base = "https://api.github.com/repos/acme/demo"
        if url == base:
            return FakeResponse(200, {"default_branch": self.default_branch})
        if url.startswith(f"{base}/commits/"):
            reference = unquote(url.rsplit("/", 1)[-1])
            sha = self.references.get(reference)
            return FakeResponse(200, {"sha": sha}) if sha else FakeResponse(404)
        if url.startswith(f"{base}/zipball/"):
            return FakeResponse(200, content=self.archive)
        return FakeResponse(404)


class GitHubReferenceResolutionTests(unittest.TestCase):
    def fetch_with(self, url, default_branch="main", references=None):
        references = references or {default_branch: "a" * 40}
        github = FakeGitHub(default_branch, references)
        with patch("src.github_fetcher.requests.get", side_effect=github.get):
            data = fetch_repository_data(url)
        return data, github.calls

    def test_simple_url_uses_default_main_branch(self):
        data, calls = self.fetch_with("https://github.com/acme/demo", "main")
        self.assertEqual(data["branch"], "main")
        self.assertEqual(data["evaluated_revision"], "a" * 40)
        self.assertIn("https://api.github.com/repos/acme/demo", calls)

    def test_simple_url_uses_non_main_default_branch(self):
        data, calls = self.fetch_with(
            "https://github.com/acme/demo",
            "trunk",
            {"trunk": "b" * 40},
        )
        self.assertEqual(data["branch"], "trunk")
        self.assertEqual(data["evaluated_revision"], "b" * 40)
        self.assertIn("https://api.github.com/repos/acme/demo/commits/trunk", calls)
        self.assertNotIn("https://api.github.com/repos/acme/demo/commits/main", calls)

    def test_explicit_sha_is_respected_without_metadata_lookup(self):
        sha = "c" * 40
        data, calls = self.fetch_with(
            f"https://github.com/acme/demo/commit/{sha}",
            "trunk",
            {sha: sha},
        )
        self.assertEqual(data["branch"], sha)
        self.assertEqual(data["evaluated_revision"], sha)
        self.assertNotIn("https://api.github.com/repos/acme/demo", calls)

    def test_explicit_branch_is_respected_without_metadata_lookup(self):
        data, calls = self.fetch_with(
            "https://github.com/acme/demo/tree/release",
            "trunk",
            {"release": "d" * 40},
        )
        self.assertEqual(data["branch"], "release")
        self.assertNotIn("https://api.github.com/repos/acme/demo", calls)

    def test_explicit_tag_is_respected_without_metadata_lookup(self):
        data, calls = self.fetch_with(
            "https://github.com/acme/demo/tree/v1.2.0",
            "trunk",
            {"v1.2.0": "e" * 40},
        )
        self.assertEqual(data["branch"], "v1.2.0")
        self.assertNotIn("https://api.github.com/repos/acme/demo", calls)

    def test_nonexistent_explicit_reference_reports_the_attempted_reference(self):
        github = FakeGitHub("trunk", {"trunk": "f" * 40})
        with patch("src.github_fetcher.requests.get", side_effect=github.get):
            with self.assertRaisesRegex(RuntimeError, "referencia 'missing'"):
                fetch_repository_data("https://github.com/acme/demo/tree/missing")

    def test_access_error_for_one_repository_does_not_poison_the_next_evaluation(self):
        successful_data = {
            "repository": "acme/ok",
            "evaluated_revision": "g" * 40,
            "repository_inventory": [],
            "file_contents": {},
        }
        completed = EvaluationResult(
            repository="acme/ok",
            evaluated_revision="g" * 40,
            evaluation_date="2026-09-06",
            evaluation_status="completed",
            dimensions=[],
            final_score=0,
            concrete_improvement="",
            integrity_notes=[],
        )
        with patch(
            "src.evaluator_engine.fetch_repository_data",
            side_effect=[RuntimeError("referencia inexistente"), successful_data],
        ), patch("src.evaluator_engine.evaluate_repository_deterministically", return_value=completed):
            failed = run_evaluation("https://github.com/acme/missing")
            succeeded = run_evaluation("https://github.com/acme/ok")
        self.assertEqual(failed.evaluation_status, "access_error")
        self.assertEqual(succeeded.evaluation_status, "completed")


class ParseGitHubUrlTests(unittest.TestCase):
    def test_simple_url_has_no_explicit_reference(self):
        _, _, revision, _ = parse_github_url("https://github.com/acme/demo")
        self.assertIsNone(revision)


if __name__ == "__main__":
    unittest.main()
