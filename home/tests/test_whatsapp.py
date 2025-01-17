import json
from pathlib import Path

import responses
from django.conf import settings
from django.core.files.images import ImageFile
from django.test import TestCase
from responses.matchers import multipart_matcher
from wagtail.images.models import Image

from home.whatsapp import create_whatsapp_template


class WhatsAppTests(TestCase):
    @responses.activate
    def test_create_whatsapp_template(self):
        data = {
            "category": "UTILITY",
            "name": "test-template",
            "language": "en_US",
            "components": [{"type": "BODY", "text": "Test Body"}],
        }
        url = "http://whatsapp/graph/v14.0/27121231234/message_templates"
        responses.add(responses.POST, url, json={})

        create_whatsapp_template("Test-Template", "Test Body")

        request = responses.calls[0].request

        self.assertEqual(request.headers["Authorization"], "Bearer fake-access-token")
        self.assertEqual(request.body, json.dumps(data, indent=4))

    @responses.activate
    def test_create_whatsapp_template_with_buttons(self):
        data = {
            "category": "UTILITY",
            "name": "test-template",
            "language": "en_US",
            "components": [
                {"type": "BODY", "text": "Test Body"},
                {
                    "type": "BUTTONS",
                    "buttons": [
                        {"type": "QUICK_REPLY", "text": "Test button1"},
                        {"type": "QUICK_REPLY", "text": "test button2"},
                    ],
                },
            ],
        }
        url = "http://whatsapp/graph/v14.0/27121231234/message_templates"
        responses.add(responses.POST, url, json={})

        create_whatsapp_template(
            "Test-Template", "Test Body", ["Test button1", "test button2"]
        )

        request = responses.calls[0].request

        self.assertEqual(request.headers["Authorization"], "Bearer fake-access-token")
        self.assertEqual(request.body, json.dumps(data, indent=4))

    @responses.activate
    def test_create_whatsapp_template_with_image(self):
        img_name = "test.jpeg"
        img_path = Path("home/tests/test_static") / img_name

        read_file = img_path.open("rb")
        saved_image = Image(
            title=img_name,
            file=ImageFile(read_file, name=img_path),
        )
        saved_file = saved_image.file
        saved_image.save()
        read_file.seek(0)

        mock_session_id = "TEST_SESSION_ID"
        mock_session_url = "http://whatsapp/graph/v14.0/app/uploads"
        responses.add(responses.POST, mock_session_url, json={"id": mock_session_id})

        mock_start_upload_url = f"http://whatsapp/graph/{mock_session_id}"
        mock_image_handle = "TEST_IMAGE_HANDLE"
        req_files = {
            "file": saved_file,
            "number": settings.FB_BUSINESS_ID,
            "access_token": settings.WHATSAPP_ACCESS_TOKEN,
        }
        responses.add(
            responses.POST,
            mock_start_upload_url,
            json={"h": mock_image_handle},
            match=[
                multipart_matcher(
                    req_files,
                )
            ],
        )

        template_url = "http://whatsapp/graph/v14.0/27121231234/message_templates"
        responses.add(responses.POST, template_url, json={})

        create_whatsapp_template("Test-Template", "Test Body", [], saved_image.id)

        mock_get_session_data = {
            "file_length": 631,
            "file_type": "image/jpeg",
            "access_token": "fake-access-token",
            "number": "27121231234",
        }
        get_session_id_request = responses.calls[0].request
        self.assertEqual(
            get_session_id_request.body, json.dumps(mock_get_session_data, indent=4)
        )

        create_template_request = responses.calls[2].request
        mock_create_template_data = {
            "category": "UTILITY",
            "name": "test-template",
            "language": "en_US",
            "components": [
                {"type": "BODY", "text": "Test Body"},
                {
                    "type": "HEADER",
                    "format": "IMAGE",
                    "example": {"header_handle": [mock_image_handle]},
                },
            ],
        }

        self.assertEqual(
            create_template_request.headers["Authorization"], "Bearer fake-access-token"
        )
        self.assertEqual(
            create_template_request.body,
            json.dumps(mock_create_template_data, indent=4),
        )
