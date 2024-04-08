from typing import Dict, Any


class MockESClient:
    def __init__(self, **kwargs):
        print(f'Created mock ES cluster client with config {kwargs}')

    def index(self, index: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "_index": "test_index",
            "_id": "7fBSvY4BrhlG6Amh95OS",
            "_version": 1,
            "result": "created",
            "_shards": {
                "total": 2,
                "successful": 1,
                "failed": 0
            },
            "_seq_no": 0,
            "_primary_term": 1
        }

    def get(self, index: str, id: str) -> Dict[str, Any]:
        return {
            "_index": "test_index",
            "_id": "7fBSvY4BrhlG6Amh95OS",
            "_version": 1,
            "_seq_no": 0,
            "_primary_term": 1,
            "found": "true",
            "_source": {
                "text": "this is a yet another test document"
            }
        }

    def search(self, index: str, body: str) -> Dict[str, Any]:
        return {
            "took": 54,
            "timed_out": "false",
            "_shards": {
                "total": 1,
                "successful": 1,
                "skipped": 0,
                "failed": 0
            },
            "hits": {
                "total": {
                    "value": 1,
                    "relation": "eq"
                },
                "max_score": 0.5753642,
                "hits": [
                    {
                        "_index": "test_index",
                        "_id": "7fBSvY4BrhlG6Amh95OS",
                        "_score": 0.5,
                        "_source": {
                            "text": "this is a yet another test document"
                        }
                    }, {
                        "_index": "test_index",
                        "_id": "a",
                        "_score": 0.6,
                        "_source": {
                            "text": "foo"
                        }
                    }, {
                        "_index": "test_index",
                        "_id": "b",
                        "_score": 0.7,
                        "_source": {
                            "text": "bar"
                        }
                    }
                ]
            }
        }
