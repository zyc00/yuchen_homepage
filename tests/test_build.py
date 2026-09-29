"""Check the publication editing workflow without third-party dependencies."""

from copy import deepcopy
import json
import unittest

from scripts import build


def example_paper():
    return {
        "id": "new-paper",
        "name": "New paper",
        "title": "A New Research Paper",
        "authors": ["Yuchen Zhou", "Coauthor"],
        "venue": {"name": "Preprint"},
        "links": {"Paper": "https://example.com/paper"},
    }


class PublicationBuildTests(unittest.TestCase):
    def test_add_paper_by_changing_only_data(self):
        papers = json.loads((build.ROOT / "data/publications.json").read_text())
        paper = example_paper()
        paper["links"]["Slides"] = "https://example.com/slides"
        papers.append(paper)
        page = build.render_site(papers)

        self.assertEqual(page.count('<article class="publication'), len(papers))
        positions = [page.index(f'<h3 id="{item["id"]}-title">') for item in papers]
        self.assertEqual(positions, sorted(positions))
        self.assertIn('class="publication publication-text-only"', page)
        self.assertIn('<a href="https://example.com/slides">Slides</a>', page)
        self.assertIn('<p class="publication-venue">Preprint</p>', page)
        self.assertNotIn('<!-- PUBLICATIONS -->', page)

    def test_author_highlighting_and_contribution_note(self):
        paper = example_paper()
        papers_html, note = build.render_publications([paper])
        self.assertIn('<strong>Yuchen Zhou</strong>, Coauthor', papers_html)
        self.assertEqual(note, "")
        paper["authors"] = ["Yuchen Zhou*", "Coauthor*"]
        papers_html, note = build.render_publications([paper])
        self.assertIn('<strong>Yuchen Zhou</strong><sup>*</sup>, Coauthor<sup>*</sup>', papers_html)
        self.assertIn('Equal contribution.', note)

    def test_plain_text_and_url_attributes_are_escaped(self):
        paper = example_paper()
        paper["title"] = 'Learning <Shapes> & "Parts"'
        paper["authors"].append("<script>alert(1)</script>")
        paper["links"]["Project"] = 'https://example.com/?x="value"&y=2'
        page = build.render_site([paper])
        self.assertIn('Learning &lt;Shapes&gt; &amp; &quot;Parts&quot;', page)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', page)
        self.assertIn('<a href="https://example.com/?x=&quot;value&quot;&amp;y=2">Learning', page)
        self.assertNotIn('<script>alert(1)</script>', page)

    def test_optional_media_uses_existing_image_or_video(self):
        paper = example_paper()
        paper["media"] = {
            "type": "image",
            "src": "assets/images/publications/oric.png",
            "alt": "Full overview",
        }
        image_html, _ = build.render_publications([paper])
        self.assertIn('loading="lazy" decoding="async" alt="Full overview"', image_html)
        self.assertNotIn('publication-text-only', image_html)

        paper["media"] = {
            "type": "video",
            "src": "assets/videos/point-sam-transformer.mp4",
            "start": 3,
            "alt": "Demo video",
        }
        video_html, _ = build.render_publications([paper])
        self.assertIn('point-sam-transformer.mp4#t=3', video_html)
        self.assertIn('<video autoplay muted loop playsinline', video_html)

    def test_invalid_data_gives_actionable_errors(self):
        cases = [
            ({"links": {"Paper": "javascript:alert(1)"}}, "links.Paper"),
            ({"authors": []}, "authors"),
            ({"media": {"type": "image", "src": "assets/missing.png", "alt": "Figure"}}, "media.src"),
            ({"media": {"type": "image", "src": "assets/images/publications/oric.png", "alt": "Figure", "width": -1}}, "media.width"),
            ({"media": {"type": "video", "src": "assets/videos/point-sam-transformer.mp4", "alt": "Demo", "start": -3}}, "media.start"),
        ]
        for changes, field in cases:
            with self.subTest(field=field):
                paper = example_paper()
                paper.update(changes)
                with self.assertRaisesRegex(ValueError, f"Paper 1: {field}"):
                    build.render_publications([paper])

    def test_duplicate_ids_are_rejected(self):
        paper = example_paper()
        with self.assertRaisesRegex(ValueError, "Paper 2: id must be unique"):
            build.render_publications([paper, deepcopy(paper)])

    def test_empty_publications_list(self):
        page = build.render_site([])
        self.assertNotIn('<article', page)
        self.assertNotIn('Equal contribution.', page)


if __name__ == "__main__":
    unittest.main()
