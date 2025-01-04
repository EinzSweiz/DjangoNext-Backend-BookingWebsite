import pytest
from rest_framework import status
from property.models import Property

@pytest.mark.django_db
def test_create_review(create_review):
    review = create_review

    assert review.text == "This is a test review."

    assert review.property is not None

    assert review.user is not None



@pytest.mark.django_db
def test_get_reviews(api_client, create_review):

    review = create_review

    url = f'/api/reviews/all/{str(review.property.id)}'

    response = api_client.get(url)
    # Debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.json()}")

    assert response.status_code == status.HTTP_200_OK

    assert response.json()['total_reviews'] > 0
    assert len(response.json()['reviews']) > 0
    assert response.json()['reviews'][0]['text'] == "This is a test review."


@pytest.mark.django_db
def test_create_review_report(api_client, create_report_review):
    """
    Test the creation of a review report using the helper fixture.
    """
    report_response = create_report_review

    assert report_response.get('success') == 'Report was created successfully'
