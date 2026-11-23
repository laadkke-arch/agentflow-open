"""Read public Casdoc appendix without executing its Java/JAR or publishing rows."""
from pathlib import Path
import csv,io,json,re,zipfile,hashlib,collections,argparse
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parent

def decode(data):
    try:return data.decode('utf-8-sig'),'utf-8-sig'
    except UnicodeDecodeError:return data.decode('cp1252'),'cp1252'

def seconds(value):
    parts=value.strip().split(':')
    if len(parts) not in (2,3):raise ValueError('not a clock timestamp')
    result=0.0
    for p in parts:result=result*60+float(p)
    return result

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--zip',default=str(ROOT/'cache/casdoc-artifact.zip'));a=parser.parse_args()
    archive=Path(a.zip);raw=archive.read_bytes();z=zipfile.ZipFile(io.BytesIO(raw))
    def table(name):
        text,enc=decode(z.read(name));rows=list(csv.reader(io.StringIO(text),delimiter='\t'))
        header=rows[0];data=rows[1:]
        if any(len(r)!=len(header) for r in data):raise ValueError('ragged TSV: '+name)
        return header,data,enc
    evnames=sorted(n for n in z.namelist() if re.fullmatch(r'analysis-data/phase1-session-events/P\d+\.tsv',n))
    people={Path(n).stem for n in evnames}
    evtotal=0;evfull_duplicates=0;evtimestamp_duplicate_excess=0
    events=collections.Counter();starts=set();split_starts=set();encodings=collections.Counter();evtimefail=0
    for name in evnames:
        h,rows,enc=table(name);encodings[enc]+=1;evtotal+=len(rows)
        evfull_duplicates+=len(rows)-len(set(tuple(r) for r in rows))
        evtimestamp_duplicate_excess+=len(rows)-len(set(r[0] for r in rows))
        pid=Path(name).stem
        for row in rows:
            try:seconds(row[0])
            except ValueError:evtimefail+=1
            task=row[h.index('Task')]
            if task:events[task]+=1
            match=re.fullmatch(r'instr-(\d+)',task)
            if match:starts.add((pid,int(match.group(1))))
            for token in task.split('/'):
                split_match=re.fullmatch(r'instr-(\d+)',token.strip())
                if split_match:split_starts.add((pid,int(split_match.group(1))))
    h2,rows2,enc2=table('analysis-data/phase2-search-fragments.tsv')
    h3,rows3,enc3=table('analysis-data/phase3-navigation-patterns.tsv')
    ids2=[r[h2.index('ID')] for r in rows2];ids3=[r[h3.index('ID')] for r in rows3]
    index3={r[0]:r for r in rows3}
    required2=['ID','Participant','Task','Start','End']
    nullkeys2=sum(any(not r[h2.index(k)].strip() for k in required2) for r in rows2)
    nullkeys3=sum(not r[0].strip() for r in rows3)
    dup2=len(ids2)-len(set(ids2));dup3=len(ids3)-len(set(ids3))
    unmatched2=sum(i not in index3 for i in ids2)
    unmatched3=sum(i not in set(ids2) for i in ids3)
    joined=[(r,index3[r[0]]) for r in rows2 if r[0] in index3]
    assert not dup2 and not dup3 and not nullkeys2 and not nullkeys3
    durations=[];badclock=0;negative=0;taskgroups=set();unmatchedpeople=0;normalized_unmatchedpeople=0
    formatcounts=collections.Counter();total_seconds_by_format=collections.Counter()
    for r,code in joined:
        try:
            dur=seconds(r[h2.index('End')])-seconds(r[h2.index('Start')]);durations.append(dur)
            negative+=int(dur<0)
        except ValueError:badclock+=1;continue
        pid=r[h2.index('Participant')];task=r[h2.index('Task')]
        taskgroups.add((pid,task));unmatchedpeople+=int(pid not in people)
        normalized_pid='P'+pid if re.fullmatch(r'\d+',pid) else pid
        normalized_unmatchedpeople+=int(normalized_pid not in people)
        # First four category columns are unique. Later headers repeat by format;
        # don't use DictReader, which would silently overwrite duplicated labels.
        flags=[h3[i] for i in range(1,5) if code[i].strip()]
        assert len(flags)==1, 'format categories must be exclusive per guide'
        formatcounts[flags[0]]+=1;total_seconds_by_format[flags[0]]+=dur
    code,codeenc=decode(z.read('study-replication/tasks/src/task/JdbcTask.java'))
    objectives=sorted(set(int(i) for i in re.findall(r'public static[^\n]*\bobjective(\d+)\(',code)))
    duplicate_headers={k:v for k,v in collections.Counter(h3).items() if v>1}
    relevant_names=['README.md','analysis-data/coding-guide.md','study-replication/intervention-guide.md','study-replication/documentation-sources.txt','study-replication/tasks/src/task/JdbcTask.java','study-replication/sample-solutions/JdbcTask.java']
    required_fields={'assignment_condition','period','submitted_at','final_pass','final_score','withdrawal_reason'}
    out={
        'checked_at_utc':datetime.now(timezone.utc).isoformat(),
        'archive_url':'https://zenodo.org/api/records/14868205/files/artifact.zip/content',
        'archive_sha256':hashlib.sha256(raw).hexdigest(),'archive_bytes':len(raw),
        'regular_files':sum(not i.is_dir() for i in z.infolist()),
        'phase1':{'participant_files':len(evnames),'distinct_file_participant_keys':len(people),'rows':evtotal,'exact_duplicate_rows_within_file':evfull_duplicates,'timestamp_duplicate_excess_within_file':evtimestamp_duplicate_excess,'timestamp_parse_failures':evtimefail,'encoding_file_counts':dict(encodings),'Task_code_counts':dict(events),'exact_singleton_instruction_person_task_including0':len(starts),'exact_singleton_instruction_person_task_excluding0':sum(t>0 for _,t in starts),'slash_split_instruction_person_task_including0':len(split_starts),'slash_split_instruction_person_task_excluding0':sum(t>0 for _,t in split_starts),'compound_code_rule':'split slash-separated instr-0/instr-1 into two codes; both counts descriptive only','instruction_rows_are_not_allocations_or_pass_flags':True},
        'phase2':{'rows':len(rows2),'columns':h2,'encoding':enc2,'unique_ID':len(set(ids2)),'duplicate_ID_excess':dup2,'required_key_null_rows':nullkeys2,'participant_keys':len(set(r[h2.index('Participant')] for r in rows2)),'person_task_search_groups':len(taskgroups)},
        'phase3':{'rows':len(rows3),'column_count':len(h3),'columns_by_position':[{'index':i,'name':n} for i,n in enumerate(h3)],'encoding':enc3,'unique_ID':len(set(ids3)),'duplicate_ID_excess':dup3,'null_ID_rows':nullkeys3,'duplicate_column_labels':duplicate_headers},
        'actual_join':{'left':'phase2-search-fragments.tsv','right':'phase3-navigation-patterns.tsv','key':['ID'],'cardinality':'1:1 search-fragment coding','left_input_rows':len(rows2),'right_input_rows':len(rows3),'joined_rows':len(joined),'left_unmatched':unmatched2,'right_unmatched':unmatched3,'is_assignment_time_quality_join':False},
        'participant_file_reference':{'literal_string_unmatched_fragment_rows':unmatchedpeople,'prefix_normalization':'digits Participant value -> P+digits filename stem','prefix_normalized_unmatched_fragment_rows':normalized_unmatchedpeople,'basis':'README one event file per participant and compatible filename/numeric-ID domains; document this convention, not an allocation export','not_used_to_infer_pass_or_assignment':True},
        'descriptive_search_intervals':{'valid_clock_rows':len(durations),'clock_parse_failures':badclock,'negative_duration_rows':negative,'format_fragment_counts':dict(formatcounts),'total_seconds_by_format':dict(total_seconds_by_format),'unit':'search fragments chosen by participants; not assigned people or final task times','no_treatment_contrast_computed':True},
        'task_materials':{'objective_numbers':objectives,'planned_person_objective_opportunities_if13_all_assigned':13*len(objectives),'basis':'13 participant-file keys crossed with task instructions; not observed allocation roster','sha256':{n:hashlib.sha256(z.read(n)).hexdigest() for n in relevant_names}},
        'target_join':{'status':'미실시','reason':'No randomized/assigned format contrast; no submitted final answers or scored pass ledger keyed to participant/task; coding test event is an attempted execution, not verdict.','assignment_roster_rows':'미확인','target_rows':'미확인 for assigned contrast','joined_rows':'미확인','left_unmatched':'미확인','required_additional_fields':sorted(required_fields)},
        'executed_boundary':'Read ZIP/TSV and text; did not execute Java/JAR, change web app, fetch submitted-private URLs, or construct participant-level outcomes.'}
    (ROOT/'casdoc-audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':'passed','phase1_rows':evtotal,'phase2_rows':len(rows2),'phase3_rows':len(rows3),'actual_join':out['actual_join'],'task_materials':{k:v for k,v in out['task_materials'].items() if k!='sha256'},'formats':dict(formatcounts),'duplicate_header_labels':duplicate_headers},ensure_ascii=False))

if __name__=='__main__':main()
