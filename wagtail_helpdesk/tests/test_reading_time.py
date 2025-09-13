import re
import pytest
from django.template import Template, Context


# Helpers to fake Wagtail blocks
class FakeContent:
    def __init__(self, source):
        self.source = source


class Block:
    def __init__(self, block_type, value):
        self.block_type = block_type
        self.value = value


@pytest.fixture
def answer_model():
    """
    Minimal inline version of the model with only the relevant methods.
    Replace with your actual model import in real tests.
    """
    import re as _re

    class Answer:
        def __init__(self, excerpt=None, page_content=None):
            self.excerpt = excerpt
            self.page_content = page_content

        def get_plain_text_from_page_content(self) -> str:
            parts = []

            if self.excerpt:
                parts.append(self.excerpt)

            for block in self.page_content or []:
                if block.block_type == "richtext":
                    try:
                        html = block.value["content"].source
                    except Exception:
                        html = ""
                    text = _re.sub(r"<[^>]+>", " ", html)
                    parts.append(text)

                elif block.block_type == "quote":
                    if hasattr(block.value, "get"):
                        quote_html = block.value.get("text", "") or block.value.get(
                            "quote", ""
                        )
                        quote_text = _re.sub(r"<[^>]+>", " ", quote_html)
                        parts.append(quote_text)

            return " ".join(parts)

        @property
        def calculated_reading_time(self) -> int | None:
            text = self.get_plain_text_from_page_content()
            avg_read_speed = 200
            word_count = len(_re.findall(r"\w+", text))
            return max(1, round(word_count / avg_read_speed)) if word_count else None

    return Answer


# --- Tests for get_plain_text_from_page_content ---

def test_plain_text_includes_excerpt_richtext_and_quote(answer_model):
    """Plain text extraction should include excerpt, richtext, and quote content."""
    a = answer_model(
        excerpt="Short summary.",
        page_content=[
            Block(
                "richtext",
                {"content": FakeContent("<p>This is <strong>rich</strong> text.</p>")},
            ),
            Block("quote", {"text": "<blockquote>A quote &amp; more</blockquote>"}),
        ],
    )
    text = a.get_plain_text_from_page_content()
    assert "Short summary." in text
    assert "This is  rich  text." in text
    assert "A quote" in text


def test_plain_text_handles_missing_richtext_content(answer_model):
    """Richtext blocks without .source should not crash and just add empty text."""
    a = answer_model(page_content=[Block("richtext", {"not_content": "oops"})])
    text = a.get_plain_text_from_page_content()
    assert text.strip() == ""


def test_plain_text_handles_both_text_and_quote_keys(answer_model):
    """Quote blocks may use 'text' or 'quote' key; both should work."""
    a1 = answer_model(page_content=[Block("quote", {"text": "<i>Text</i>"})])
    a2 = answer_model(page_content=[Block("quote", {"quote": "<i>Alternative</i>"})])
    assert "Text" in a1.get_plain_text_from_page_content()
    assert "Alternative" in a2.get_plain_text_from_page_content()


# --- Tests for calculated_reading_time ---

def test_reading_time_is_none_when_no_words(answer_model):
    """If there is no text, reading time should be None."""
    a = answer_model(excerpt="", page_content=[])
    assert a.calculated_reading_time is None


@pytest.mark.parametrize(
    "word_count, expected_minutes",
    [
        (1, 1),
        (50, 1),
        (200, 1),
        (250, 1),
        (300, 2),
        (380, 2),
        (401, 2),
        (450, 2),
        (500, 2),  # bankers rounding: 2.5 -> 2
        (550, 3),
    ],
)
def test_reading_time_rounding(answer_model, word_count, expected_minutes):
    """Check rounding and minimum 1 minute rule."""
    words = " ".join(f"w{i}" for i in range(word_count))
    a = answer_model(excerpt=words, page_content=[])
    assert a.calculated_reading_time == expected_minutes


def test_reading_time_counts_all_sources(answer_model):
    """Word count should include excerpt, richtext, and quote together."""
    a = answer_model(
        excerpt="one two three",
        page_content=[
            Block("richtext", {"content": FakeContent("<p>four five</p>")}),
            Block("quote", {"text": "<b>six</b> <i>seven</i> eight"}),
        ],
    )
    assert a.calculated_reading_time == 1  # 8 words in total


# --- Tests for the template fragment ---

def render_fragment(obj):
    tpl = Template(
        """
    {% with minutes=self.calculated_reading_time %}
      {% if minutes %}
        <span class="content-header__tag">
          {{ minutes }} min. leestijd
        </span>
      {% endif %}
    {% endwith %}
    """
    )
    return tpl.render(Context({"self": obj}))


def test_template_shows_reading_time_label(answer_model):
    """Template should render a reading time label when words exist."""
    a = answer_model(excerpt="word " * 400, page_content=[])  # ~400 words = 2 min.
    html = render_fragment(a)
    assert "2 min. leestijd" in html


def test_template_hides_label_when_no_words(answer_model):
    """Template should not render a label if there is no text."""
    a = answer_model(excerpt="", page_content=[])
    html = render_fragment(a)
    assert "min. leestijd" not in html