"""Post-seal public answer/comment acquisition. Never used for recruitment."""
import json
from collect import P, get, REV_FILTER, utc


def pages(path, params, stem):
    result = []
    for page in range(1, 21):
        data = get(path, dict(params, page=page, pagesize=100), f'raw/outcomes/{stem}_{page}.json')
        result.extend(data.get('items', []))
        print(stem, page, len(data.get('items', [])), 'has_more', data.get('has_more'), flush=True)
        if not data.get('has_more'):
            return result
    raise RuntimeError('pagination incomplete: ' + stem)


def main():
    cases = [json.loads(x) for x in (P / 'revisions.jsonl').read_text().splitlines()]
    ids = ';'.join(str(x['question_id']) for x in cases)
    # Exposure starts only after the R1 pair commit, recorded separately from fetch time.
    seal = 'f048885abfbfcca1ffd8840899bf2911cd35da60'
    inc = '.items;.has_more;.backoff;.quota_remaining;.error_id;.error_message;question.question_id;question.creation_date;question.last_edit_date;question.accepted_answer_id;question.answer_count;question.owner;question.link;shallow_user.user_id;shallow_user.display_name;shallow_user.link;shallow_user.user_type'
    filt = get('filters/create', dict(base='none', include=inc), 'raw/outcomes/question_filter.json')['items'][0]['filter']
    questions = pages('questions/' + ids, dict(site='stackoverflow', filter=filt), 'questions')
    answers = pages('questions/' + ids + '/answers', dict(site='stackoverflow', filter='withbody', sort='creation', order='asc'), 'answers')
    aids = ';'.join(str(x['answer_id']) for x in answers)
    revisions = pages('posts/' + aids + '/revisions', dict(site='stackoverflow', filter=REV_FILTER), 'answer_revisions') if aids else []
    postids = ids + (';' + aids if aids else '')
    comments = pages('posts/' + postids + '/comments', dict(site='stackoverflow', filter='withbody', sort='creation', order='asc'), 'comments')
    bundle = dict(acquired_utc=utc(), answer_exposure_after_commit=seal, questions=questions, answers=answers, answer_revisions=revisions, comments=comments)
    (P / 'outcome_packet.json').write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + '\n')
    print('acquired', len(questions), 'questions', len(answers), 'answers', len(revisions), 'answer revisions', len(comments), 'comments')


if __name__ == '__main__':
    main()
