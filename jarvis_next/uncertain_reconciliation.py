import json


async def reconcile_uncertain(runtime, mission_id, resolution):
    """Require an explicit human decision before resuming an uncertain external write.

    ``confirmed_applied`` advances past the uncertain step.
    ``confirmed_not_applied`` retries the uncertain step.
    ``unknown`` records that no execution decision is authorized and leaves the
    mission failed.
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
        raise ValueError("Mission does not contain an uncertain external outcome")
    if resolution == "unknown":
        runtime.state.event(
            "worker.uncertain_reconciled",
            {"resolution": resolution, "resumed": False},
            mission_id,
        )
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
