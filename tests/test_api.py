from OmniOrchestrator import app

client = app.test_client()

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
