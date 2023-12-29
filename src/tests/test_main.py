from typing import Any
from unittest.mock import Mock, patch

from main import UrlRequest, get_youtube_audio, get_youtube_key


def test_get_youtube_key_with_kurzgesagt():
    # Given
    pass

    # When
    url_youtube_kurzgesagt = "https://www.youtube.com/watch?v=cFslUSyfZPc"
    input_req = UrlRequest(urlink=url_youtube_kurzgesagt)
    output = get_youtube_key(input_req)

    # Then
    assert output == "cFslUSyfZPc"

def test_get_youtube_short_key_with_kurzgesagt():
    # Given
    pass

    # When
    url_youtube_short_kurzgesagt = "https://youtu.be/cFslUSyfZPc"
    input_req = UrlRequest(urlink=url_youtube_short_kurzgesagt)
    output = get_youtube_key(input_req)

    # Then
    assert output == "cFslUSyfZPc"


def test_get_youtube_embed_key_with_kurzgesagt():
    # Given
    pass

    # When
    url_youtube_embed_kurzgesagt = "https://www.youtube.com/embed/cFslUSyfZPc?si=fqKkzm2GgVUen-VM"
    input_req = UrlRequest(urlink=url_youtube_embed_kurzgesagt)
    output = get_youtube_key(input_req)

    # Then
    assert output == "cFslUSyfZPc"

@patch("yt_dlp.YoutubeDL")
def test_get_youtube_audio_should_run_ydl_download(mock_youtube_dl: Any):
    # Given
    mocked_download = mock_youtube_dl.return_value.__enter__.return_value.download

    # When
    input_req = UrlRequest(urlink="https://youtu.be/cFslUSyfZPc")
    get_youtube_audio(input_req)

    # Then
    mock_youtube_dl.assert_called_once_with({
        "format": "bestaudio/best",
        "outtmpl": "./audio/%(id)s.%(ext)s",
    })
    mocked_download.assert_called_once_with([input_req])
