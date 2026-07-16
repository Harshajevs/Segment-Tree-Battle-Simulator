"""End-to-end API tests over the FastAPI TestClient."""
from app.services.match_service import match_service


def create_match(client, **overrides):
    payload = {"team_size": 16, "seed": 7, "max_rounds": 12, **overrides}
    response = client.post("/api/matches", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def attack_payload(al=0, ar=7, dl=0, dr=3):
    return {
        "type": "attack",
        "attack_range": {"left": al, "right": ar},
        "defense_range": {"left": dl, "right": dr},
    }


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_get_match(client):
    match = create_match(client)
    assert match["state"] == {
        "round": 1,
        "scores": [0, 0],
        "attacker": 0,
        "status": "in_progress",
        "winner": None,
        "expected_action": "attack",
    }
    assert [t["size"] for t in match["teams"]] == [16, 16]

    fetched = client.get(f"/api/matches/{match['id']}").json()
    assert fetched == match


def test_match_not_found_envelope(client):
    response = client.get("/api/matches/doesnotexist")
    assert response.status_code == 404
    assert "not found" in response.json()["error"]["message"]


def test_action_flow_and_log(client):
    match = create_match(client)
    response = client.post(f"/api/matches/{match['id']}/actions", json=attack_payload())
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["result"]["damage"] >= 0
    assert body["state"]["round"] == 2
    assert body["state"]["attacker"] == 1
    assert "update_paths" in body["result"]

    log = client.get(f"/api/matches/{match['id']}/actions").json()
    assert len(log) == 1
    assert log[0]["sequence"] == 1
    assert "update_paths" not in log[0]["result"]  # trimmed for persistence


def test_wrong_action_type_rejected(client):
    match = create_match(client)
    challenge = {**attack_payload(), "type": "challenge"}
    response = client.post(f"/api/matches/{match['id']}/actions", json=challenge)
    assert response.status_code == 422
    assert "expects" in response.json()["error"]["message"]


def test_invalid_range_rejected(client):
    match = create_match(client)
    response = client.post(
        f"/api/matches/{match['id']}/actions", json=attack_payload(ar=999)
    )
    assert response.status_code == 422


def test_query_endpoint_all_operations(client):
    match = create_match(client)
    for operation in ("sum", "max", "min", "gcd", "lcm"):
        response = client.get(
            f"/api/matches/{match['id']}/query",
            params={
                "team": 0,
                "attribute": "attack",
                "operation": operation,
                "left": 0,
                "right": 15,
            },
        )
        assert response.status_code == 200, (operation, response.text)
        body = response.json()
        if operation in ("max", "min"):
            assert 0 <= body["value"] <= 15
            assert body["element_value"] is not None


def test_tree_endpoint_depth_cap(client):
    match = create_match(client, team_size=64)
    response = client.get(
        f"/api/matches/{match['id']}/tree",
        params={
            "team": 1,
            "attribute": "health",
            "operation": "sum",
            "max_depth": 3,
        },
    )
    body = response.json()
    assert response.status_code == 200
    assert max(n["depth"] for n in body["nodes"]) == 3
    root = next(n for n in body["nodes"] if n["node"] == 1)
    assert (root["start"], root["end"]) == (0, 63)


def test_soldiers_pagination(client):
    match = create_match(client, team_size=64)
    response = client.get(
        f"/api/matches/{match['id']}/soldiers",
        params={"team": 0, "offset": 60, "limit": 10},
    )
    body = response.json()
    assert body["total"] == 64
    assert [s["index"] for s in body["soldiers"]] == [60, 61, 62, 63]


def test_full_match_to_completion(client):
    match = create_match(client, max_rounds=10)
    state = match["state"]
    while state["status"] == "in_progress":
        payload = attack_payload(0, 15, 0, 15)
        payload["type"] = state["expected_action"]
        response = client.post(f"/api/matches/{match['id']}/actions", json=payload)
        assert response.status_code == 200, response.text
        state = response.json()["state"]
    assert state["status"] == "finished"

    listed = client.get("/api/matches").json()
    entry = next(m for m in listed if m["id"] == match["id"])
    assert entry["status"] == "finished"


def test_restart_rehydration_reproduces_state(client):
    match = create_match(client)
    for _ in range(5):
        response = client.post(
            f"/api/matches/{match['id']}/actions", json=attack_payload(2, 9, 1, 6)
        )
        assert response.status_code == 200
    before = client.get(f"/api/matches/{match['id']}").json()

    match_service.drop_from_cache(match["id"])  # simulate process restart

    after = client.get(f"/api/matches/{match['id']}").json()
    assert after == before
    # and the rehydrated engine keeps playing correctly
    response = client.post(f"/api/matches/{match['id']}/actions", json=attack_payload())
    assert response.status_code == 200
    assert response.json()["state"]["round"] == before["state"]["round"] + 1
