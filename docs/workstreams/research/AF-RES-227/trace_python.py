"""Read the pinned Python backend's locals without wrapping its matcher."""
import json
import sys


def report(event, **values):
    print('AF227PY ' + json.dumps({'event': event, **values}, separators=(',', ':')), file=sys.stderr)


def instrument(backend):
    filename = backend.__file__

    def dispatch(frame, event, _):
        if event != 'call' or frame.f_code.co_filename != filename:
            return None
        name = frame.f_code.co_name
        if name == 'unique_lcs_py':
            def observe_unique(frame, event, value):
                if event == 'line' and frame.f_lineno == 87:
                    values = frame.f_locals
                    report('unique-candidate', a_local0=values['apos'], b_local0=values['bpos'],
                           pile0=values['k'], ranks_before=list(values['stacks']))
                if event == 'return':
                    report('unique-result', pairs_local0=value)
                return observe_unique

            report('unique-call', n_a=len(frame.f_locals['a']), n_b=len(frame.f_locals['b']))
            return observe_unique

        if name == 'recurse_matches_py':
            values = frame.f_locals
            scope = [values[k] for k in ('alo', 'ahi', 'blo', 'bhi')]
            before = len(values['answer'])
            branch = 'no-unique-no-edge'
            report('recurse-scope', bounds0_half_open=scope, maxrecursion=values['maxrecursion'])

            def observe_recurse(frame, event, value):
                nonlocal branch
                if event == 'line':
                    line = frame.f_lineno
                    if line == 131:
                        branch = 'empty'
                    elif line == 145:
                        branch = 'chain'
                        report('recurse-selected', pair0=[frame.f_locals[k] for k in ('apos', 'bpos')])
                    elif line == 153:
                        branch = 'prefix'
                    elif line == 160:
                        branch = 'suffix'
                    elif line == 128:
                        branch = 'depth-limit'
                if event == 'return':
                    report('recurse-return', bounds0_half_open=scope, branch=branch,
                           appended_pairs0=frame.f_locals['answer'][before:])
                return observe_recurse

            return observe_recurse
        return None

    return dispatch
