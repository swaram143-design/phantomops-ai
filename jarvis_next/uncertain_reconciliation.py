import json


def _record_unknown_once(state, mission_id, raw_result, state_payload):
    """Atomically persist an unresolved decision exactly once."""
    result_payload = dict(state_payload)
    result_payload["reconciliation"] = {
        "resolution": "unknown",
        "previous_next_step": int(state_payload.get("next_step", 0)),
    }
    result_json = json.dumps(result_payload, default=str)
    now = state.now()
    try:
        # Serialize competing reconcilers before evaluating the CAS predicate.
        # Each worker may have performed a read that opened a deferred SQLite
        # transaction, so close that snapshot before acquiring the write lock.
        state.conn.commit()
        state.conn.execute("BEGIN IMMEDIATE")
        cursor = state.conn.execute(
            "UPDATE missions SET result=?, updated_at=? WHERE id=? AND status='failed' AND result=?",
            (result_json, now, mission_id, raw_result),
        )
        if cursor.rowcount == 0:
            current = state.get_mission(mission_id)
            if not current:
                state.conn.rollback()
                raise KeyError(mission_id)
            current_result = json.loads(current["result"] or "{}")
            if current_result.get("reconciliation", {}).get("resolution") == "unknown":
                state.conn.commit()
                return current_result
            state.conn.rollback()
            raise ValueError("Mission is no longer awaiting uncertain-outcome reconciliation")
        state._insert_event(
            "mission.updated",
            {"status": "failed", "reconciliation": "unknown"},
            mission_id,
        )
        # Keep the reconciliation event itself idempotent at the database
        # boundary as a second guard against duplicate writers.
        state.conn.execute(
            "INSERT INTO events(mission_id,kind,payload,created_at) "
            "SELECT ?,?,?,? WHERE NOT EXISTS ("
            "SELECT 1 FROM events WHERE mission_id=? AND kind='worker.uncertain_reconciled' "
            "AND json_extract(payload,'$.resolution')='unknown')",
            (
                mission_id,
                "worker.uncertain_reconciled",
                json.dumps({"resolution": "unknown", "resumed": False}),
                state.now(),
                mission_id,
            ),
        )
        state.conn.commit()
        return result_payload
    except Exception:
        state.conn.rollback()
        raise


async def reconcile_uncertain(runtime, mission_id, resolution):
    """Require an explicit human decision before resuming an uncertain external write.

    ``confirmed_applied`` advances past the uncertain step.
    ``confirmed_not_applied`` retries the uncertain step.
    ``unknown`` records that no execution decision is authorized and leaves the
    mission failed. Unknown decisions are persisted atomically and idempotently.
    """
    if resolution not in ("confirmed_applied", "confirmed_not_applied", "unknown"):
        raise ValueError(resolution)
    mission = runtime.state.get_mission(mission_id)
    if not mission:
        raise KeyError(mission_id)
    if mission["status"] != "failed" or not mission["result"]:
        raise ValueError("Mission is not awaiting uncertain-outcome reconciliation")
    raw_result = mission["result"]
    state = json.loads(raw_result)
    if not state.get("side_effect_uncertain"):
        existing = state.get("reconciliation", {}).get("resolution")
        if resolution == "unknown" and existing == "unknown":
            return {"mission_id": mission_id, "status": "failed", "reconciliation": "unknown"}
        raise ValueError("Mission does not contain an uncertain external outcome")
    if resolution == "unknown":
        _record_unknown_once(runtime.state, mission_id, raw_result, state)
        return {"mission_id": mission_id, "status": "failed", "reconciliation": "unknown"}

    plan = json.loads(mission["plan"])
    current = int(state.get("next_step", 0))
    next_step = current + 1 if resolution == "confirmed_applied" else current
    state["next_step"] = next_step
    state["reconciliation"] = {
        "resolution": resolution,
        "previous_next_step": current,
    }
    state.pop("side_effect_uncertain", None)
    claimed = runtime.state.reconcile_uncertain_transition(
        mission_id,
        raw_result,
        plan,
        state,
        {
            "resolution": resolution,
            "previous_next_step": current,
            "next_step": next_step,
        },
    )
    if not claimed:
        raise ValueError("Mission is no longer awaiting uncertain-outcome reconciliation")
    return await runtime.resume_mission(mission_id)
