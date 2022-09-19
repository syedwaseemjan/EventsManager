from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status

PATTERN_DATE = r"^\d{4}-\d{1,2}-\d{1,2}$"

create_event_schema = swagger_auto_schema(
    operation_id="createEvent",
    operation_description="Creates an event for a user.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(
                title="Title",
                description="Event title.",
                type=openapi.TYPE_STRING,
            ),
            "description": openapi.Schema(
                title="Description",
                description="Event description.",
                type=openapi.TYPE_STRING,
            ),
            "date": openapi.Schema(
                title="Date",
                description="Event date.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                pattern=PATTERN_DATE,
            ),
        },
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            "Returns `event_id` (UUID) of new event.",
            examples={
                "application/json": {
                    "event_id": "1d5f8593-26eb-495c-b0bf-c1954558b33e",
                    "title": "Test Event 1",
                    "description": "Test Event 1 Description",
                    "date": "2024-12-12T00:00:00Z",
                    "creator": 1,
                    "total_participants": 0,
                }
            },
        )
    },
)

update_event_schema = swagger_auto_schema(
    operation_id="editEvents",
    operation_description="Edits an event.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "title": openapi.Schema(
                title="Title",
                description="Event title.",
                type=openapi.TYPE_STRING,
            ),
            "description": openapi.Schema(
                title="Description",
                description="Event description.",
                type=openapi.TYPE_STRING,
            ),
            "date": openapi.Schema(
                title="Date",
                description="Event date.",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE,
                pattern=PATTERN_DATE,
            ),
        },
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            "Edits an event.",
            examples={
                "application/json": {
                    "event_id": "1d5f8593-26eb-495c-b0bf-c1954558b33e",
                    "title": "Test Event 1",
                    "description": "Test Event 1 Description",
                    "date": "2024-12-12T00:00:00Z",
                    "creator": 1,
                    "total_participants": 0,
                }
            },
        )
    },
)

get_events_schema = swagger_auto_schema(
    operation_id="getEvents",
    operation_description="Retrieves the list of events.",
    responses={
        status.HTTP_200_OK: openapi.Response(
            "Retrieves the list of events.",
            examples={
                "application/json": {
                    "count": 15,
                    "next": "/api/v1/events/?page=2&page_size=5",
                    "previous": None,
                    "results": [
                        {
                            "event_id": "16abba90-5aaa-498b-8f64-cdca71b623f2",
                            "title": "Test Event 1",
                            "description": "Test Event 1",
                            "date": "2024-12-12T00:00:00Z",
                            "creator": 1,
                            "total_participants": 15,
                        },
                        {
                            "event_id": "521f1466-36a7-46f8-b829-76f2b749154b",
                            "title": "Test Event 2",
                            "description": "Test Event 2 Description",
                            "date": "2024-02-02T00:00:00Z",
                            "creator": 2,
                            "total_participants": 0,
                        },
                    ],
                }
            },
        )
    },
)

get_participants_schema = swagger_auto_schema(
    operation_id="getEventParticipants",
    operation_description="Retrieves the list of event participants.",
    responses={
        status.HTTP_200_OK: openapi.Response(
            "Retrieves the list of event participants.",
            examples={
                "application/json": {
                    "count": 15,
                    "next": "api/v1/events/16abba90-5aaa-498b-8f64-cdca71b623f2/participants/?page=2",
                    "previous": None,
                    "results": [
                        "user1",
                        "user2",
                        "user3",
                    ],
                }
            },
        )
    },
)

signup_for_event_schema = swagger_auto_schema(
    operation_id="signupForEvent",
    operation_description="Adds user for an event.",
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            "Adds user for an event.",
            examples={"application/json": {"event": "d53ad258-c730-4622-84af-684193a97653", "user": 2}},
        )
    },
)

withdraw_from_event_schema = swagger_auto_schema(
    operation_id="withdrawFromEvent",
    operation_description="Withdraws user for an event.",
    responses={
        status.HTTP_200_OK: openapi.Response(
            "Withdraws user for an event.",
            examples={"application/json": {"detail": "Deleted."}},
        )
    },
)
