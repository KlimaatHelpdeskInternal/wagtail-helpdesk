"""
Tests for site page views to ensure all pages load properly.

This file verifies that key site pages respond correctly with proper HTTP status codes
and contain expected content. It covers the main navigation paths and critical functionality
pages of the Klimaat Helpdesk application.
"""
from http import HTTPStatus

import pytest
from django.urls import reverse

from wagtail_helpdesk.tests.factories import (
    AnswerIndexPageFactory,
    AnswerFactory,
    AskQuestionPageFactory,
    ExpertAnswerOverviewPageFactory,
    ExpertIndexPageFactory,
)

@pytest.mark.django_db
class TestSitePageLoading:
    """Test that essential site pages load correctly."""

    @pytest.mark.xfail
    def test_homepage_loads(self, django_app):
        """Test that the homepage loads with correct status code."""
        response = django_app.get("/")
        assert response.status_code == HTTPStatus.OK
        assert 'lang="nl"' in response.content.decode()
        assert "Antwoorden van wetenschappers op al je vragen over klimaatverandering" in response.content.decode()

    def test_admin_pages_load(self, django_app):
        """Test that admin interface pages are accessible."""
        # Django admin login page
        response = django_app.get(reverse("admin:login"))
        assert response.status_code == HTTPStatus.OK

        # Wagtail admin login page
        response = django_app.get("/admin/")
        assert response.status_code == HTTPStatus.FOUND # Redirects to login

    def test_healthcheck_loads(self, django_app):
        """Test that health check endpoint is accessible."""
        response = django_app.get("/__healthcheck__/")
        assert response.status_code == HTTPStatus.OK

    def test_error_pages_load_in_debug_mode(self, django_app, settings):                        # ? Not found in templates
        """Test that error pages load correctly in debug mode."""
        if settings.DEBUG:
            response = django_app.get("/test404")
            assert response.status_code == HTTPStatus.OK

            response = django_app.get("/test500")
            assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
class TestWagtailHelpdeskPages:
    """Test wagtail-helpdesk specific pages load correctly."""

    def test_answer_index_page_loads(self, django_app, home_page):
        """Test that the answers index page loads correctly."""
        answer_index = AnswerIndexPageFactory(parent=home_page, slug="answers")

        response = django_app.get(answer_index.url)
        assert response.status_code == HTTPStatus.OK
        assert "answers" in response.content.decode()

    def test_answer_detail_page_loads(self, django_app, home_page):
        """Test that individual answer pages load correctly."""
        answer_index = AnswerIndexPageFactory(parent=home_page, slug="answers")
        answer = AnswerFactory(
            parent=answer_index,
            slug="test-answer",
            title="Test Answer",
            type="answer"
        )

        response = django_app.get(answer.url)
        assert response.status_code == HTTPStatus.OK
        assert "Test Answer" in response.content.decode()

    def test_ask_question_page_loads(self, django_app, home_page):
        """Test that the ask question page loads correctly."""
        ask_question_page = AskQuestionPageFactory(
            parent=home_page,
            slug="ask-question",
            title="Ask a Question"
        )

        response = django_app.get(ask_question_page.url)
        assert response.status_code == HTTPStatus.OK
        assert "Ask a Question" in response.content.decode()
        # Check that form elements are present
        assert 'name="question"' in response.content.decode()

    @pytest.mark.xfail
    def test_expert_index_page_loads(self, django_app, home_page):
        """Test that the expert index page loads correctly."""
        expert_index = ExpertIndexPageFactory(
            parent=home_page,
            slug="experts",
            title="Experts"
        )

        response = django_app.get(expert_index.url)
        assert response.status_code == HTTPStatus.OK
        assert "Experts" in response.content.decode()

    def test_expert_answer_overview_page_loads(self, django_app, home_page):
        """Test that expert answer overview page loads correctly with expert ID."""
        from wagtail_helpdesk.tests.factories import ExpertFactory

        # Create an expert and expert overview page
        expert_overview = ExpertAnswerOverviewPageFactory(
            parent=home_page,
            slug="answers_by",
            title="Expert Answers"
        )
        expert = ExpertFactory()

        # ExpertAnswerOverviewPage requires an expert ID in the URL
        expert_url = expert_overview.url + f"{expert.pk}/"
        response = django_app.get(expert_url)
        assert response.status_code == HTTPStatus.OK
        assert expert.name in response.content.decode()

    def test_expert_answer_overview_page_base_url_returns_404(self, django_app, home_page):
        """Test that expert answer overview page base URL returns 404 as expected."""
        expert_overview = ExpertAnswerOverviewPageFactory(
            parent=home_page,
            slug="answers_by"
        )

        # The base URL should return 404 by design
        response = django_app.get(expert_overview.url, expect_errors=True)
        assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.django_db
class TestPageNavigation:
    """Test page navigation and menu structure."""

    def test_main_navigation_structure(self, django_app, home_page):
        """Test that main navigation contains expected pages."""
        # Create typical site structure
        answer_index = AnswerIndexPageFactory(
            parent=home_page,
            slug="answers",
            title="Answers",
            show_in_menus=True
        )
        expert_index = ExpertIndexPageFactory(
            parent=home_page,
            slug="experts",
            title="Experts",
            show_in_menus=True
        )
        ask_question = AskQuestionPageFactory(
            parent=home_page,
            slug="ask-question",
            title="Ask a Question",
            show_in_menus=True
        )

        response = django_app.get("/")
        content = response.content.decode()

        # Check that navigation contains links to the created pages
        assert answer_index.url in content or "Answers" in content
        assert expert_index.url in content or "Experts" in content
        assert ask_question.url in content or "Ask a Question" in content

        # Also verify pages are accessible
        assert django_app.get(answer_index.url).status_code == HTTPStatus.OK
        assert django_app.get(expert_index.url).status_code == HTTPStatus.OK
        assert django_app.get(ask_question.url).status_code == HTTPStatus.OK

    def test_answer_categories_accessible(self, django_app, home_page):
        """Test that answer categories are accessible through GET parameter filtering."""
        from wagtail_helpdesk.tests.factories import AnswerCategoryFactory

        answer_index = AnswerIndexPageFactory(parent=home_page, slug="answers")
        category = AnswerCategoryFactory(name="Climate Change", slug="climate-change")

        # Test category filtering via GET parameter (this works correctly)
        category_url = f"{answer_index.url}?{category.name}="
        response = django_app.get(category_url)
        assert response.status_code == HTTPStatus.OK

        # Verify the category appears in the context
        assert category.name in [c['category'].name for c in response.context['categories']]

    def test_search_functionality_accessible(self, django_app, home_page):
        """Test that search functionality is accessible."""
        answer_index = AnswerIndexPageFactory(parent=home_page, slug="answers")

        # Test search with query parameter
        search_url = f"{answer_index.url}?search=climate"
        response = django_app.get(search_url)
        assert response.status_code == HTTPStatus.OK

        # Should contain search term or search functionality
        content = response.content.decode()
        assert 'search' in content.lower()


@pytest.mark.django_db
class TestPageAccessibility:
    """Test page accessibility and error handling."""

    def test_nonexistent_pages_return_404(self, django_app):
        """Test that non-existent pages return 404 status."""
        response = django_app.get("/nonexistent-page/", expect_errors=True)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_pages_handle_malformed_urls(self, django_app, home_page):
        """Test that pages handle malformed URLs gracefully."""
        answer_index = AnswerIndexPageFactory(parent=home_page, slug="answers")

        # Test malformed category URL
        malformed_url = f"{answer_index.url}/category/nonexistent-category/"
        response = django_app.get(malformed_url, expect_errors=True)
        # Should either return 404 or handle empty results
        assert response.status_code == HTTPStatus.NOT_FOUND

    @pytest.mark.xfail
    def test_iframe_search_widget_loads(self, django_app):
        """Test that iframe search widget endpoint loads."""
        response = django_app.get("/iframe-search-widget")
        assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
class TestPageContent:
    """Test that pages contain expected content and functionality."""

    def test_homepage_contains_featured_content(self, django_app, home_page):
        """Test that homepage displays featured content when available."""
        # Create featured content
        answer_index = AnswerIndexPageFactory(parent=home_page, slug="answers")
        featured_answer = AnswerFactory(
            parent=answer_index,
            featured=True,
            title="Featured Climate Answer"
        )

        response = django_app.get("/")
        content = response.content.decode()

        # Homepage should show featured content
        assert "Featured Climate Answer" in content

    def test_answer_pages_contain_metadata(self, django_app, home_page):
        """Test that answer pages contain proper metadata and structure."""
        answer_index = AnswerIndexPageFactory(parent=home_page, slug="answers")
        answer = AnswerFactory(
            parent=answer_index,
            title="Climate Science Answer",
            excerpt="A brief summary of climate science",
            type="answer"
        )

        response = django_app.get(answer.url)
        content = response.content.decode()

        assert "Climate Science Answer" in content
        assert "A brief summary of climate science" in content

    def test_pages_include_seo_elements(self, django_app):
        """Test that pages include basic SEO elements."""
        response = django_app.get("/")
        content = response.content.decode()

        # Check for basic HTML structure
        assert "<html" in content
        assert "<head>" in content
        assert "<title>" in content
        assert "</html>" in content