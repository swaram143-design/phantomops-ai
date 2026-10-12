from .verifier import ResultVerifier


def main():
    verifier = ResultVerifier()

    assert verifier.verify({"action": "research"}, {"value": 1}) == (True, None)
    assert verifier.verify({"action": "research"}, {"success": True}) == (True, None)

    ok, error = verifier.verify({"action": "research"}, None)
    assert ok is False
    assert error == "no result data"

    ok, error = verifier.verify({"action": "research"}, {"success": False})
    assert ok is False
    assert error == "result reports success=false"

    print("JARVIS-NEXT RESULT VERIFIER OK")


if __name__ == "__main__":
    main()
