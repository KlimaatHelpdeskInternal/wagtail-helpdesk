from http import HTTPStatus

import pytest

from wagtail_helpdesk.tests.factories import (
    AnswerFactory,
    ExpertAnswerOverviewPageFactory,
    ExpertFactory,
)

pytestmark = pytest.mark.django_db


def test_expert_answer_overview_page(home_page, django_app):
    """Verify that the expert answer overview page returns the expected answers.

    The page should include answers authored by the requested expert, including
    shared answers, and exclude answers from other experts.
    """

    # Arrange: create an overview page and two experts with associated answers.
    expert_answer_overview_page = ExpertAnswerOverviewPageFactory(parent=home_page)
    expert, other_expert = ExpertFactory.create_batch(size=2)
    answer = AnswerFactory(experts=[expert])
    shared_answer = AnswerFactory(experts=[expert, other_expert])
    other_answer = AnswerFactory(experts=[other_expert])

    # Act: request the overview page for the chosen expert.
    url = expert_answer_overview_page.url + expert_answer_overview_page.reverse_subpage(
        "expert_answers", args=(expert.pk,)
    )
    response = django_app.get(url)
    context = response.context

    # Assert: only the expert's answers are included in the response context.
    assert answer in context["answers"]
    assert shared_answer in context["answers"]
    assert other_answer not in context["answers"]
    assert context["expert"] == expert


def test_expert_answer_overview_page_expert_not_found(home_page, django_app):
    """Verify that invalid expert overview requests return a 404 response."""

    expert_answer_overview_page = ExpertAnswerOverviewPageFactory(parent=home_page)

    # Request the overview page without an expert identifier.
    response = django_app.get(expert_answer_overview_page.url, expect_errors=True)
    assert response.status_code == HTTPStatus.NOT_FOUND

    # Request the expert-specific subpage using a non-existent expert id.
    missing_expert_url = (
        expert_answer_overview_page.url
        + expert_answer_overview_page.reverse_subpage("expert_answers", args=(999999,))
    )
    response = django_app.get(missing_expert_url, expect_errors=True)

    assert response.status_code == HTTPStatus.NOT_FOUND
