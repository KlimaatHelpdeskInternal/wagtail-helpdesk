import pytest

from wagtail_helpdesk.tests.factories import (
    AnswerFactory,
    AnswerIndexPageFactory,
    ExpertAnswerOverviewPageFactory,
    ExpertFactory,
)

pytestmark = pytest.mark.django_db


def test_homepage_context(django_app, home_page):
    """Verify the homepage context includes the expected pages and featured items."""

    # Arrange: create featured and non-featured answers and experts.
    featured_answers = AnswerFactory.create_batch(size=2, featured=True)
    excluded_answer = AnswerFactory(featured=False)

    featured_experts = ExpertFactory.create_batch(size=2, featured=True)
    excluded_expert = ExpertFactory(featured=False)

    answer_index_page = AnswerIndexPageFactory(parent=home_page, slug="answers")
    expert_answers_overview_page = ExpertAnswerOverviewPageFactory(
        parent=home_page,
        slug="experts",
    )

    # Act: request the homepage and inspect its context.
    response = django_app.get("/")
    context = response.context

    # Assert: the context includes the expected pages and featured items, and excludes non-featured items.
    assert context["answer_index_page"] == answer_index_page
    assert context["expert_answers_overview_page"] == expert_answers_overview_page

    assert len(context["featured_answers"]) == 2
    for featured_answer in featured_answers:
        assert featured_answer in context["featured_answers"]
    assert excluded_answer not in context["featured_answers"]

    assert len(context["featured_experts"]) == 2
    for expert in featured_experts:
        assert expert in context["featured_experts"]
    assert excluded_expert not in context["featured_experts"]