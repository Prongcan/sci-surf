"""Verify batched embedding responses stay aligned with paper inputs."""

from unittest.mock import Mock, patch

from orchestrator.storage_util import EmbeddingClient


def test_batch_embeddings_keep_input_order_with_empty_text():
    client = EmbeddingClient(api_key="test", dimension=2)
    response = Mock()
    response.json.return_value = {
        "data": [
            {"index": 1, "embedding": [3.0, 4.0]},
            {"index": 0, "embedding": [1.0, 2.0]},
        ]
    }
    with patch("orchestrator.storage_util.httpx.post", return_value=response) as post:
        result = client.get_embeddings(["paper one", "", "paper two"], delay=0)

    assert result == [[1.0, 2.0], None, [3.0, 4.0]]
    assert post.call_args.kwargs["json"]["input"] == ["paper one", "paper two"]
