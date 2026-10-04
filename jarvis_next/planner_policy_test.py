from .planner import MissionPlanner, PlanValidationError

def main():
    plan = MissionPlanner.deterministic(None, 'find revenue opportunities')
    assert plan['steps'][-1]['action'] == 'external_send'
    assert plan['steps'][-1]['capability'] == 'external_send'
    try:
        MissionPlanner.validate('bad', {'steps':[{'capability':'research','action':'publish'}]})
        raise AssertionError('unsafe action accepted')
    except PlanValidationError:
        pass
    print('JARVIS-NEXT PLANNER POLICY OK')

if __name__ == '__main__':
    main()