"""Paired question-cluster percentile intervals. Never treat claims as questions."""
import math,random,statistics
from common import quantile

def value(rows,kind,numerator=None,denominator=None,field=None):
    if kind=='ratio':
        n=sum(r.get(numerator,0) or 0 for r in rows)
        d=sum(r.get(denominator,0) or 0 for r in rows)
        return n/d if d else None
    xs=[r[field] for r in rows if r.get(field) is not None]
    if not xs:return None
    if kind=='mean':return statistics.mean(xs)
    if kind=='median':return statistics.median(xs)
    raise ValueError(kind)

def paired_interval(pairs,kind,numerator=None,denominator=None,field=None,iterations=10000,seed=18018):
    """Each pair contains A/P rows from one question; duplication keeps its claims together."""
    if not pairs:return {'A':None,'P':None,'difference':None,'ci95':[None,None],
                         'questions':0,'iterations':iterations,'valid_replicates':0,'seed':seed}
    def statistic(ps,condition):return value([p[condition] for p in ps],kind,numerator,denominator,field)
    a,p=statistic(pairs,'A'),statistic(pairs,'P');rng=random.Random(seed);differences=[]
    for _ in range(iterations):
        sampled=[pairs[rng.randrange(len(pairs))] for i in range(len(pairs))]
        aa,pp=statistic(sampled,'A'),statistic(sampled,'P')
        if aa is not None and pp is not None:differences.append(pp-aa)
    return {'A':a,'P':p,'difference':p-a if a is not None and p is not None else None,
            'ci95':[quantile(differences,0.025),quantile(differences,0.975)],
            'questions':len(pairs),'iterations':iterations,'valid_replicates':len(differences),
            'seed':seed,'unit':'question; paired A/P; all sampled claims within question retained',
            'small_stratum':len(pairs)<5,
            'limits':'Conditional on this purposive sample and one execution per condition/question; not population sampling or model-repetition uncertainty.'}
