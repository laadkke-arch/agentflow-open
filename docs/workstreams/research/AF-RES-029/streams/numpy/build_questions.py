"""Serialize the frozen NumPy first-text questions; no network or route execution."""
from pathlib import Path
import datetime
import hashlib
import json
import re
import copy

ROOT = Path(__file__).resolve().parent
REPO_PREFIX = 'docs/workstreams/research/AF-RES-029/streams/numpy/'
NOW = datetime.datetime.now(datetime.timezone.utc).isoformat()

def pos(section, first, last):
    return {'section': section, 'line_start': first, 'line_end': last}

def pred(identifier, statement, section, first, last, falsifier, inherits=None, qualification=None):
    result = {'id': identifier, 'predicate': statement, 'source_positions': [pos(section, first, last)], 'falsifying_input': falsifier}
    if inherits:
        result['inherits'] = inherits
    if qualification:
        result['qualification'] = qualification
    return result

def named(names, role, section, first, last):
    return {'names': names, 'role_in_initial_text': role, 'source_positions': [pos(section, first, last)], 'knowledge_class': 'explicitly_named_in_first_text'}

META = {
    'Q09': {'nep':50,'classification':'partial','period':'2021-2022','pr':21103,'created':'2022-02-21T22:54:44Z','commit':'ff5e9b79b1f94e0b438c459f630e505610382670','blob':'6d69da10e7432ff20b90ba3138fa7d3e1f59a081','path':'doc/neps/nep-0050-scalar-promotion.rst','file':'NEP-50.rst','title':'NEP 50 — Promotion rules for Python scalars'},
    'Q10': {'nep':47,'classification':'whole','period':'2021-2022','pr':18456,'created':'2021-02-21T15:54:21Z','commit':'0f2b4b235eb580590eaa744bf015d51e2e675afc','blob':'19965c20d908aa3c19fabea67ffcc130261022d3','path':'doc/neps/nep-0047-array-api-standard.rst','file':'NEP-47.rst','title':'NEP 47 — Adopting the array API standard'},
    'Q11': {'nep':55,'classification':'whole','period':'2023-2024','pr':24483,'created':'2023-08-21T20:32:31Z','commit':'1c013e78112a94e7a2975212df2304606b0d1d1c','blob':'233a84d70d6aaf99501521de3955c67e695ebb49','path':'doc/neps/nep-0055-string_dtype.rst','file':'NEP-55.rst','title':'NEP 55 — Add a UTF-8 Variable-Width String DType to NumPy'},
    'Q12': {'nep':53,'classification':'partial','period':'2023-2024','pr':23579,'created':'2023-04-13T17:37:40Z','commit':'bf0835ac5d7a7301f05706ae0d5adce191d43ec2','blob':'35aac33763858798096e13465f083c72a2d126ff','path':'doc/neps/nep-0053-c-abi-evolution.md','file':'NEP-53.md','title':'NEP 53 — Evolving the NumPy C-API for NumPy 2.0'},
}

questions = []
for qid, m in META.items():
    data = (ROOT/'first_texts'/m['file']).read_bytes()
    git_blob = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    assert git_blob == m['blob']
    url = 'https://github.com/numpy/numpy/blob/'+m['commit']+'/'+m['path']
    q = {
        'id':qid, 'ledger':'numpy', 'canonical_id':'NEP-'+str(m['nep']), 'title':m['title'],
        'whole_or_partial':m['classification'], 'period':m['period'], 'initial_date':m['created'],
        'initial_date_basis':'Earliest verified official numbered-NEP proposal PR creation; immutable initial head corroboration. Not an inference from Created headers or commit author time, and not a claim about all earlier related public discussions.',
        'initial_url':url, 'first_public_event_url':'https://github.com/numpy/numpy/pull/'+str(m['pr']),
        'version':{'commit':m['commit'],'git_blob':m['blob'],'original_repository_path':m['path'],'version_kind':'initial PR head text, before subsequent review edits'},
        'first_text':{'source_id':qid+'-FIRST','path':REPO_PREFIX+'first_texts/'+m['file'],'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha1':git_blob,'bytes':len(data),'lines':len(data.splitlines()),'checked_utc':NOW,'checked_utc_basis':'Stored immutable text and Git-blob hash verified at serialization; remote fetch occurred earlier in this session.'},
        'sampling_hash':hashlib.sha256(('AF-RES-029|v1|numpy|'+m['period']+'|NEP-'+str(m['nep'])).encode()).hexdigest(),
        'queries_frozen_before_common_search':True, 'supplier_searches_performed':False,
        'question_origin':'Analyst request boundary and predicates derived only from the recovered initial text; exact normative source positions retained.',
        'source_interpretation_rule':'Proposed behavior is the frozen target; alternatives, unresolved details and aspirational performance are not silently made established supplier capabilities.'
    }
    questions.append(q)

q=questions[0]
q.update({
    'request':'Find an existing dtype-promotion component that can resolve a result type for Python scalars mixed with explicitly typed NumPy arrays or scalars, using types rather than scalar values and preserving the specified weak-scalar behavior.',
    'classification_reason':'The selected request is the bounded promotion operation within NumPy arithmetic/casting machinery. Its output dtype is independently usable before arithmetic and conversion are integrated. The full redesign is retained in whole_must.',
    'caller':{'text':'NumPy binary-operator or ufunc dispatch code, including code handling user-defined DTypes.', 'source_positions':[pos('Motivation and Scope',59,69),pos('Implementation',309,319)]},
    'input':{'text':'Python int, float or complex scalars together with typed NumPy scalars, 0-D arrays or N-D arrays; promotion consumes scalar kind and concrete array dtype, not scalar magnitude.', 'source_positions':[pos('Abstract',18,49),pos('Proposed Weak Promotion',277,293)]},
    'output':{'text':'A concrete result dtype determined without value inspection; Python scalar kinds may resolve to the other operand dtype, while explicitly typed NumPy values retain their type strength.', 'source_positions':[pos('Impact on operators functions involving NumPy arrays or scalars',105,112),pos('Proposed Weak Promotion',277,293)]},
    'limits':[
        {'kind':'boundary','text':'Partial action resolves promotion; executing ufuncs, unsafe scalar conversion, warnings and can_cast integration remain outside the partial action.', 'source_positions':[pos('Implementation',309,338)]},
        {'kind':'unresolved_first_draft','text':'The draft proposes weak behavior for most ufuncs but contains an apparently inconsistent np.multiple(float32_arr, 2.) example and explicitly discusses operator-only alternatives. Do not silently correct the typo or infer a finalized rule.', 'source_positions':[pos('Impact on functions involving Python int, float, complex',149,160),pos('Backward compatibility',213,219),pos('Do not use weak scalar logic in functions',365,384)]},
        {'kind':'proposed_with_alternative','text':'Strict integer overflow rejection and warning-plus-infinity for float overflow are proposed, while the alternatives explicitly allow later relaxation. They are frozen as the proposed whole-design branch, not as historical implementation facts.', 'source_positions':[pos('Impact on operators involving Python int, float, complex',132,143),pos('Handling conversion of scalars when unsafe',404,413)]},
        {'kind':'preference','text':'An optional compatibility-warning mode is planned, and future defaults for user-defined DTypes are tentative; neither is needed to complete the selected partial resolver.', 'source_positions':[pos('Usage and Impact',75,80),pos('Proposed Weak Promotion',286,290)]}
    ],
    'named_original_families_components':[
        named(['NumPy','np.result_type','np.can_cast','np.multiply','np.asarray','ufuncs'],'Target family and explicit operations','Abstract; Impact; Implementation',18,160),
        named(['JAX','JAX promotion','jnp.array'],'Named related weak-scalar system; first text notes that JAX also remembers weak typing on arrays','Related Work',298,303),
        named(['NEP 42','DType','Integral','Floating','ComplexFloatin'],'Named extensible dtype machinery and abstract scalar-kind labels (last spelling retained from draft)','Proposed Weak Promotion; Implementation',274,319),
        named(['__array_ufunc__'],'Named array-like integration protocol','Do not use weak scalar logic in functions',381,384)
    ],
    'whole_must':[
        pred('Q09-W01','Result-type promotion must never inspect operand values; changing only a Python scalar value cannot choose a wider dtype.','Abstract; Proposed Weak Promotion',43,49,'Resolve an int8-array/Python-int pair twice, with scalar values 1 and 255. Returning int8 once and int16 the other time falsifies value independence.'),
        pred('Q09-W02','Explicit NumPy scalars and 0-D arrays must promote like N-D arrays of the same dtype, rather than lose their declared dtype because of shape.','Abstract; Impact on NumPy arrays or scalars',43,112,'Add a uint8 array to np.int64(1), np.array(1,dtype=int64), and np.array([1],dtype=int64). Downcasting only either scalar-shaped input falsifies the rule.'),
        pred('Q09-W03','Python int, float and complex inputs must be weak scalar kinds; an appropriate concrete counterpart dtype may retain its precision instead of forcing a default int64/float64 result.','Proposed Weak Promotion',277,293,'Promote a UInt16 operand with a Python integer. Unconditionally returning the platform default integer rather than permitting UInt16 falsifies this operation.'),
        pred('Q09-W04','The proposed arithmetic/conversion branch rejects an out-of-range Python integer rather than silently widening from its value or wrapping before the operation.','Impact on Python scalar operators; Handling conversion',132,143,'np.arange(10,dtype=int8) + 256 must report a conversion error; an int16 result selected from 256 or an int8 wrapped result falsifies the proposed branch.',qualification='Provisional proposal branch: explicit alternatives at lines 404–413 discuss relaxing this requirement.'),
        pred('Q09-W05','The proposed floating conversion behavior warns on overflow to infinity before performing the operation in the retained lower-precision dtype.','Impact on Python scalar operators',139,143,'Multiply a float32 array by Python 1e200. Silently widening to float64 from the value, or silently producing infinity without the specified warning, falsifies this branch.'),
        pred('Q09-W06','can_cast must stop consulting scalar values and must reject the formerly value-safe int64-to-uint8 scalar examples.','Impact on can_cast',83,99,'np.can_cast(np.int64(100), np.uint8) returning True solely because 100 fits falsifies the whole casting change.')
    ],
    'partial_must':[
        pred('Q09-P01','Return a result dtype without inspecting scalar values.','Proposed Weak Promotion',277,293,'Hold operand types fixed while replacing Python int 1 with 255; a different resolved dtype falsifies the partial operation.',inherits=['Q09-W01']),
        pred('Q09-P02','Preserve the type strength of explicitly typed NumPy scalar and 0-D inputs exactly as their N-D counterparts.','Abstract; Impact on NumPy arrays or scalars',43,112,'A resolver that treats int64(1) as weak but an int64 array as strong fails the partial action.',inherits=['Q09-W02']),
        pred('Q09-P03','Represent Python int/float/complex as weak kinds and allow the concrete other dtype to determine their promotion, including UInt16 plus Integral producing UInt16.','Proposed Weak Promotion',277,293,'A system offering only strong Python int-to-int64 and float-to-float64 conversion cannot resolve UInt16 + Integral to UInt16.',inherits=['Q09-W03'])
    ],
    'independent_partial_purpose':'Resolve the concrete dtype for a mixed scalar/array operation before choosing a numerical loop or allocating its result. The resolved dtype is useful even if no arithmetic loop, overflow conversion policy or can_cast integration has yet been migrated.',
    'remaining_adapter':'Map NumPy concrete DTypes and Python scalar kinds into the component and connect its result to ufunc dispatch. Integrate value-independent can_cast, scalar conversion errors/warnings and remaining operator behavior separately. If the adapter has to invent the weak-promotion algorithm or reconcile 0-D type strength itself, partial completion is not established.',
    'same_name_wrong_actor_output_failure':'A scalar converter called result_type that inspects 255 to pick int16, or a Python-language numeric-tower description that returns a Python class without resolving NumPy array dtype, has the wrong operation/output. A JAX API that makes every explicitly created 0-D array weak would also need a demonstrated adapter preserving the frozen NumPy type-strength rule.',
    'neutral_query':'array dtype promotion Python scalars weak typing value independent result type',
    'a_queries':['weakly typed Python scalars NumPy zero dimensional arrays result type promotion','Python int float complex weak scalar promotion preserve array dtype without inspecting values'],
    'first_text_sections':[pos('Abstract and scope',8,69),pos('Usage and compatibility',72,219),pos('Detailed description and implementation',222,338),pos('Alternatives and references',341,438)],
    'initial_recovery':{'evidence_files':['raw/nep-50-pr-events.json','raw/nep-50-force-push-fragments.html','raw/nep-50-original-head.json','raw/nep-50-pr-commits.json'],'finding':'First force-push event at 2022-02-21T23:08:57Z links from ff5e9b79... to e98393c6.... The from-commit adds the file, has author/committer time 22:51:10Z before PR creation 22:54:44Z, and is the original head. Later rebase commit 27733042... was not used.','limitations':'Created header says 2021-01-10 and earlier related discussions are linked; those do not establish the public availability of this numbered NEP text. The date field is explicitly the earliest verified numbered-NEP PR event.'}
})

q=questions[1]
q.update({
    'request':'Find an implementation or reusable design covering a separate, 2021-standard-conforming Python array namespace and array object, including portable operations, dtype/indexing behavior, device syntax and zero-copy interchange.',
    'classification_reason':'This is a multi-operation API subsystem with its own array object, execution namespace, input contracts, casting/indexing semantics and integration protocols.',
    'caller':{'text':'Downstream numerical library authors and end users who want one function implementation to accept arrays from conforming libraries without hard dependencies on each library.', 'source_positions':[pos('Abstract',19,23),pos('Adoption in downstream libraries',97,123)]},
    'input':{'text':'Conforming array objects and supported Python scalars, shape/axis arguments, supported dtype literals and CPU device information. Array-like coercion is a separate explicit step.', 'source_positions':[pos('High-level design',182,215),pos('Functions in the namespace',231,259),pos('Device support',313,328)]},
    'output':{'text':'Arrays from the selected conforming namespace with the prescribed dtype, shape and device semantics; a single selected element remains a 0-D array. Interchange produces an ndarray view on producer memory.', 'source_positions':[pos('High-level design',182,210),pos('DLPack support',270,297),pos('Indexing',389,395)]},
    'limits':[
        {'kind':'boundary','text':'The target is the 2021 standard and the separate NumPy namespace. Changes to the upstream standard itself are out of scope.', 'source_positions':[pos('Motivation and Scope',61,81)]},
        {'kind':'boundary','text':'Only bool, 8/16/32/64-bit signed/unsigned integers and 32/64-bit floats are in this initial standard. Complex, string, object, datetime and structured dtypes are outside the described portable core.', 'source_positions':[pos('Dtypes and casting rules',334,349),pos('High-level design',211,215)]},
        {'kind':'undefined','text':'Mixed-kind casting, Python scalar overflow, clipping beyond the slice extent and mutation mixed with possible views are not portable guarantees in this first text.', 'source_positions':[pos('Dtypes and casting rules',351,364),pos('Indexing',397,409),pos('The array object',422,426)]},
        {'kind':'preference','text':'The namespace name and array class name are tentative; exact class hierarchy and dtype object implementation are alternatives. Matching the operational contracts matters more than those spellings.', 'source_positions':[pos('Motivation and Scope',63,69),pos('The array object',428,430),pos('The dtype objects',475,507)]}
    ],
    'named_original_families_components':[
        named(['NumPy','Tensorflow','TensorFlow','PyTorch','Dask','JAX','CuPy','MXNet','SciPy','scikit-learn'],'Named array providers and downstream users','Motivation and downstream adoption',38,109),
        named(['Python array API standard','Consortium for Python Data API Standards','numpy.array_api','data-apis/numpy array-api prototype'],'Named standard, namespace and initial prototype','Abstract; Implementation',19,23),
        named(['DLPack','ndarray.__dlpack__','from_dlpack','buffer protocol','PEP 3118','__array_interface__','__array_struct__','__array__'],'Explicitly named interchange protocols and functions','DLPack support',267,300),
        named(['__array_namespace__','get_namespace','__array_ufunc__','__array_function__','__array_module__','__duckarray__','NEP 30','NEP 37','NEPs 40-43'],'Named dispatch, namespace and dtype work','Motivation; Adoption; Appendix',61,143),
        named(['CUDA','ROCm','OpenCL','CPU','GPU','TPU'],'Named device contexts; NumPy remains CPU-only','DLPack and device support',282,328),
        named(['numpy.linalg','np.argmin','np.argmax','np.asarray','jax.numpy'],'Explicit API components and related work','High-level design; Related Work',217,222)
    ],
    'whole_must':[
        pred('Q10-W01','Provide the separate standard array namespace and array object needed for portable array construction and numerical operations across conforming libraries, with namespace discovery for downstream callers.','Abstract; Adoption in downstream libraries; High-level design',19,123,'Run a downstream function that obtains xp from two same-library arrays and uses xp.mean and xp.std. A wrapper tied only to a global NumPy namespace, with no conforming array namespace, fails the full design.'),
        pred('Q10-W02','Array operations obey the described array-object/indexing contract: no ordinary methods beyond dunders, no integer advanced indexing, single-array boolean indexing, and scalar selection returns a 0-D array.','High-level design; Indexing',182,191,'For a 2-D array, a[0,0] returning a NumPy scalar or silently accepting forbidden integer-array advanced indexing falsifies this contract.'),
        pred('Q10-W03','Functions use explicit supported array inputs, positional-only/keyword-only contracts, inline type annotations and dtype literals, without relying on __array_ufunc__ or __array_function__ dispatch.','High-level design; Functions in the namespace',193,264,'Call a namespace reduction with a Python list or an object that only implements __array_function__, or give dtype="float32". Implicit coercion/legacy dispatch or acceptance of string dtype syntax fails the frozen namespace contract.'),
        pred('Q10-W04','Supported dtype promotion is value independent and treats 0-D arrays like higher-dimensional arrays; dtype objects can be compared for equality and reused as dtype arguments.','Dtypes and casting rules; The dtype objects',334,369,'Promote two same-kind array dtypes while varying only scalar-shaped operand values; a result-type change, or inability to pass x.dtype to array creation, falsifies the contract.'),
        pred('Q10-W05','Support DLPack producer export via __dlpack__ and consumer import via from_dlpack, yielding an ndarray view without copying the exchanged array data.','DLPack support for zero-copy data interchange',267,300,'Import a supported CPU producer and inspect whether the returned ndarray shares its storage. A materialized copy, Python list or metadata-only descriptor fails this exchange action.'),
        pred('Q10-W06','Expose device identity on arrays and device selection in creation calls, with the NumPy implementation accepting CPU and rejecting unsupported devices.','Syntax for device support',303,328,'Create an array with an unsupported GPU device through the NumPy namespace. Silent CPU allocation despite that request, or no readable device attribute, falsifies the contract.'),
        pred('Q10-W07','Integrate the required underlying operations: matrix stacks for missing linalg functions, keepdims on argmin/argmax, and an asarray mode that never copies.','High-level design',217,222,'Ask asarray never-copy conversion to transform storage that would require copying, or request argmin(..., keepdims=True). Silently copying or dropping the axis instead of preserving it fails full integration.'),
        pred('Q10-W08','The new namespace must not deprecate, remove or otherwise break the existing NumPy API as its adoption mechanism.','Backward compatibility',165,169,'Install/use the new namespace and rerun existing main-namespace NumPy calls. Removal or changed legacy behavior caused by the new namespace falsifies the compatibility boundary.')
    ],
    'partial_must':[
        pred('Q10-P01','Accept a producer object supporting __dlpack__ and return an ndarray through a consumer import function.','DLPack support',293,297,'Pass a supported producer; a result that is only a capsule, shape descriptor or serialized payload fails the requested array output.',inherits=['Q10-W05']),
        pred('Q10-P02','The imported ndarray views producer data without an exchange-time data copy.','DLPack support',270,279,'Exchange a CPU array and compare backing storage; allocating a separate buffer falsifies zero-copy interchange.',inherits=['Q10-W05']),
        pred('Q10-P03','Provide the NumPy producer-side __dlpack__ export as well as consumer import, retaining a device-aware interchange protocol.','DLPack support',282,297,'A consumer-only helper with no NumPy producer export, or a protocol unable to identify its supported device, is incomplete for this interchange component.',inherits=['Q10-W05'])
    ],
    'independent_partial_purpose':'Exchange a supported CPU array between NumPy and another conforming producer/consumer without copying. That data handoff is useful before the standardized namespace, new array class and all numerical operations are complete.',
    'remaining_adapter':'Wire the provided exchange functions into NumPy object methods and namespace entry points while respecting the provider lifetime contract. Full namespace functions, casting, indexing, devices and compatibility remain. If the adapter must implement the DLPack producer/consumer conversion or copying avoidance itself, the returned component has not completed the partial action.',
    'same_name_wrong_actor_output_failure':'A similarly named array API page that merely lists mathematical functions, or a from_dlpack helper yielding a tensor from a different library without a NumPy ndarray consumer, does not establish the exact partial output. A serialization format called zero-copy without a live producer-to-ndarray memory view also fails.',
    'neutral_query':'standard Python array namespace portable tensor functions zero copy data interchange',
    'a_queries':['Python array API standard __array_namespace__ casting indexing array object','NumPy from_dlpack __dlpack__ zero copy CPU array interoperability'],
    'first_text_sections':[pos('Abstract, scope and usage',16,169),pos('High-level design and functions',172,264),pos('Interchange and devices',267,328),pos('Dtypes, indexing and array objects',331,430),pos('Implementation, appendix and references',433,590)],
    'initial_recovery':{'evidence_files':['raw/nep-47-pr-commits.json','raw/nep-47-pr-events.json','raw/nep-47-initial-commit.json'],'finding':'PR commit list contains one commit 0f2b4b23..., authored and committed at 2021-02-21T15:42:22Z before PR creation. The file is added there; the complete eight-event metadata response contains no force-push event.','limitations':'The first NEP links a November 2020 mailing-list discussion of the general array API standard. This sample unit is the first numbered NumPy adoption proposal PR, not the origin of that upstream standard. Earlier background links were not opened as suppliers or counted as first designs.'}
})

q=questions[2]
q.update({
    'request':'Find a reusable variable-width UTF-8 string datatype subsystem for NumPy, covering construction, missing values, strict coercion, storage/mutation, vector operations, C/Python integration and serialization.',
    'classification_reason':'The initial proposed work describes a complete datatype subsystem with multiple public operations and storage/serialization integration, rather than one string conversion routine.',
    'caller':{'text':'NumPy users and downstream libraries currently using object string arrays, including Pandas, scikit-learn, h5py and PyTables.', 'source_positions':[pos('Usage and Impact',176,193)]},
    'input':{'text':'N-dimensional arrays or array-like data of arbitrarily sized Python strings; optional user-provided missing sentinel and coerce flag; numeric/other inputs may be converted to strings by default or rejected in strict mode.', 'source_positions':[pos('Python API',331,370),pos('Missing data support',498,523),pos('Coercing non-strings',610,628)]},
    'output':{'text':'A first-class NumPy StringDType array backed by variable-width UTF-8 storage, yielding Python str scalars and supporting mutations, vector operations and serialization with the specified missing-data behavior.', 'source_positions':[pos('Abstract',16,29),pos('Python API',331,364),pos('Detailed description',295,307)]},
    'limits':[
        {'kind':'out_of_scope','text':'Do not change ordinary dtype inference for strings; no new built-in missing sentinel, unknown-encoding memory-map dtype, generic bytes fix or fast SIMD string implementation is required.', 'source_positions':[pos('Proposed work',144,171),pos('Backward compatibility',285,290)]},
        {'kind':'environment','text':'Target integration is NumPy 2.0 but the new DType and file format can slip to 2.1. The initial external prototype requires NUMPY_EXPERIMENTAL_DTYPE_API. These are initial proposal constraints, not current-environment claims.', 'source_positions':[pos('Implementation',722,734),pos('Implementation',778,782)]},
        {'kind':'unsupported_interface','text':'Python buffer protocol and idiomatic Cython typed memoryviews are explicitly unsupported for this layout without future changes.', 'source_positions':[pos('Cython Support and the Buffer Protocol',480,493)]},
        {'kind':'preference','text':'Small-string optimization, a 32-bit length field and the exact np.strings rename are alternatives or future optimizations, not mandatory gates. Locale-aware ordering, case folding and normalization are future work.', 'source_positions':[pos('Memory layout',423,435),pos('Casts and ufuncs',638,642),pos('np.strings namespace',667,670)]},
        {'kind':'performance_not_threshold','text':'Preliminary prototype benchmark numbers are reported by the author; they do not define a required speedup. Arbitrary missing sentinels may require holding the GIL while sorting.', 'source_positions':[pos('Performance',195,283),pos('Other Sentinels',579,590)]}
    ],
    'named_original_families_components':[
        named(['NumPy','StringDType','np.dtypes','np.dtype("T")','NPY_VSTRING','npy_static_string'],'Target family and exact proposed datatype/API names','Python API; Memory layout',309,421),
        named(['pandas','Pandas','scikit-learn','h5py','PyTables','HDF5'],'Named downstream users and storage ecosystem','Usage and Impact',176,193),
        named(['numpy-user-dtypes/stringdtype','stringdtype/tests','ngoldbaum/pandas stringdtype branch','NUMPY_EXPERIMENTAL_DTYPE_API'],'Explicit initial prototype, tests and downstream prototype','Implementation and References',722,821),
        named(['PyArrow','Apache Arrow','Arrow C data interface','Julia','tensorflow','RaggedTensor'],'Named related storage/array families and interfaces','Cython Support; Related Work',480,493),
        named(['np.char','np.strings','np.char.chararray','bytes_','unicode','object','NEP 26','npy','npz','pickle'],'Named legacy, proposed string APIs and serialization','Proposed work; Serialization',124,171),
        named(['Cython','Python buffer protocol','SSO-23','malloc','free','pd.NA','np.nan'],'Named implementation mechanisms and missing sentinels','Missing data; Implementation; References',498,553)
    ],
    'whole_must':[
        pred('Q11-W01','Provide a first-class NumPy variable-width UTF-8 string DType with no per-array maximum string-length parameter and Python str scalar behavior, while leaving ordinary string inference unchanged.','Abstract; Python API; Backward compatibility',16,29,'Construct a multidimensional array containing "a", "é" and a much longer later element, then extract an item. Truncation, an object-only container, fixed maximum width, or changing np.array(["a"]) inference falsifies full integration.'),
        pred('Q11-W02','Support default non-string-to-string coercion and a coerce=False mode that rejects non-string data during array creation.','Coercing non-strings',607,628,'Create StringDType(coerce=False) from ["x", 7]. Silently stringifying 7, or requiring a separate caller validation pass because the DType does not enforce the rule, falsifies this contract.'),
        pred('Q11-W03','Accept user-provided missing sentinels with the proposed categories: NaN-like propagation and sorting-last behavior, string sentinels treated as strings, and errors for unsupported-object comparisons.','Missing data support',495,590,'Create an array with na_object=np.nan and add/sort it; losing the sentinel or sorting it as an ordinary string fails. With na_object=None, silently comparing/sorting it as a string also fails.'),
        pred('Q11-W04','Store variable-length data outside fixed-size array entries through the proposed per-array arena/metadata interface, and provide allocation, copy and free access through the NumPy C API.','Memory layout and Managing Heap Allocations',383,421,'A downstream C loop receiving the array entries must obtain each UTF-8 byte buffer through a supported allocation interface. A bare array of Python-object references with no datatype-managed buffer interface fails this storage design.'),
        pred('Q11-W05','Support in-place string mutation, including length growth, with the proposed allocation/locking discipline preventing data races and use-after-free during concurrent access.','Mutation and Thread Safety',437,478,'Enlarge one string while another thread reads it. Reallocating/freeing its buffer without the described guarded lifetime, or forbidding all element mutation, falsifies this part of the design.'),
        pred('Q11-W06','Provide round-trip casts to built-in dtypes, comparisons in Unicode-code-point order, string add, string/integer multiply, isnan, and rejection of binary operations between unequal StringDType parameterizations.','Casts, ufunc support, and string manipulation functions',630,648,'Concatenate two string arrays or call isnan on a NaN sentinel; absent ufunc dispatch fails. Combining unequal na_object/coerce descriptors without the specified error also fails.'),
        pred('Q11-W07','Provide serialization of variable-width string payloads in npy/npz sidecar storage without requiring pickle, while also supporting pickling when requested.','Serialization',672,695,'Save and reload a StringDType array with long and non-ASCII strings under allow_pickle=False. Refusing the file or losing sidecar bytes fails this complete-design requirement.'),
        pred('Q11-W08','Integrate the new DType with supported NumPy array functionality and string manipulation operations, including advanced indexing and the Python/C DType interfaces.','Usage and Impact; Python API; Implementation',176,193,'Apply advanced indexing and a string uppercase operation to a multidimensional StringDType array. A standalone one-dimensional string store that cannot participate in NumPy indexing/ufunc behavior fails this subsystem requirement.')
    ],
    'partial_must':[
        pred('Q11-P01','Construct a NumPy array of variable-width UTF-8 strings of unequal lengths without a maximum-length scan or truncation, retaining the first-class string dtype.','Problems with Fixed-Width Strings; Python API',78,87,'Construct ["a", "é", "a much longer string"] and later store an even longer item. A fixed-width truncated result or generic Python list fails the partial storage/construction purpose.',inherits=['Q11-W01']),
        pred('Q11-P02','In strict mode reject non-string inputs during construction rather than silently coercing them or requiring a second caller-side validation pass.','Coercing non-strings',610,628,'Pass ["ok", 42] with coerce=False. A successful array containing "42" falsifies strict validation.',inherits=['Q11-W02']),
        pred('Q11-P03','Return a NumPy array that supports its ordinary shape/indexing use and produces Python string scalars; a foreign scalar or one-dimensional-only container is not this output.','Usage and Impact; Python API',176,193,'Construct a 2-by-2 string array and select a scalar element. A foreign table-column object lacking NumPy array shape/indexing is insufficient.',inherits=['Q11-W01','Q11-W08'])
    ],
    'independent_partial_purpose':'Load and validate heterogeneous-length UTF-8 text into a typed NumPy array in one construction pass. This immediately replaces an object-array sanitization pass even before the entire allocator, missing-data matrix, serialization and string namespace migration are finished.',
    'remaining_adapter':'Select/import the provided dtype, pass coerce=False and translate an existing array-like input boundary. Full first-design work still includes all sentinel semantics, arena/C interfaces, thread-safe mutation, casts/ufuncs and npy/npz sidecar serialization. If the adapter must implement variable-width storage or strict validation itself, partial completion is not established.',
    'same_name_wrong_actor_output_failure':'Pandas StringDtype, an Apache Arrow string column, a TensorFlow RaggedTensor or a fixed-width NumPy Unicode dtype may share string terminology, but the partial action requires a multidimensional typed NumPy array with strict construction semantics. Converting such a foreign object to a generic object array is not the requested output.',
    'neutral_query':'NumPy variable width UTF-8 string dtype missing values strict coercion',
    'a_queries':['NumPy StringDType variable width strings coerce False na_object','UTF-8 variable length string arrays arena allocation mutation serialization sidecar'],
    'first_text_sections':[pos('Abstract and motivation',13,171),pos('Usage, performance and compatibility',173,290),pos('Python API and storage',292,493),pos('Missing data and coercion',495,628),pos('Casts, namespaces and serialization',630,695),pos('Related work, implementation and references',697,826)],
    'initial_recovery':{'evidence_files':['raw/nep-55-pr-events.json','raw/nep-55-force-push-fragments.html','raw/nep-55-pre-force-history.json','raw/nep-55-initial-commit.json'],'finding':'First force-push HTML links the pre-rebase head 426f6d06.... Its path history leads to first added commit 1c013e78... at 2023-08-21T20:22:53Z before PR creation at 20:32:31Z; the next commit adds discussion links at 20:37:46Z. That first added text is used instead of rebased d7434377... or the review-updated head.','limitations':'Commit author time (2023-06-30) and Created header (2023-06-29) precede verified public PR availability and are not used as public dates. The initial text already describes prototypes and related work; those names are explicit initial knowledge, not new discoveries.'}
})

q=questions[3]
q.update({
    'request':'Find a build-time C-API target-selection mechanism that lets a downstream NumPy extension compile with newer headers while choosing an older minimum runtime API, with newer symbols hidden unless explicitly opted into.',
    'classification_reason':'The selected boundary is the bounded NPY_TARGET_VERSION compilation operation inside a larger NumPy 2.0 C-API/ABI migration. The entire migration, API-table compatibility and downstream adaptation requirements remain visible in whole_must.',
    'caller':{'text':'A downstream C/Cython extension maintainer building against NumPy headers and distributing a binary extension.', 'source_positions':[pos('Abstract',15,42),pos('Backwards compatible builds',90,107)]},
    'input':{'text':'Downstream extension source, newer NumPy headers and an optional NPY_TARGET_VERSION baseline such as NPY_1_22_API_VERSION; absence of the macro selects a suitably old API by default.', 'source_positions':[pos('Backwards compatible builds',93,107)]},
    'output':{'text':'A binary built with the newer headers that exposes/uses only the selected compatible API surface and runs on the chosen older NumPy baseline; the wider design additionally seeks one rebuilt binary for both NumPy 1.x and 2.0.', 'source_positions':[pos('Abstract',22,42),pos('Backwards compatible builds',93,107),pos('Implementation',213,218)]},
    'limits':[
        {'kind':'partial_boundary','text':'The bounded action is compile-time API selection for an older baseline. NumPy 2.0 API-table translation, layout changes, downstream source edits and packaging are remaining full-design integration.', 'source_positions':[pos('Implementation',213,245)]},
        {'kind':'out_of_scope','text':'Passing state/context for CPython subinterpreters or HPy is not part of this design. Concrete API removals are illustrative and may be reconsidered case by case.', 'source_positions':[pos('Motivation and Scope',63,84),pos('Alternatives',250,257)]},
        {'kind':'version_branch','text':'The first design discusses NumPy 1.25 followed by 2.0; Cython 3 could hide struct-layout changes, while supporting Cython 2.x would require downstream macro/Python-object changes. Do not assume either ecosystem transition already occurred.', 'source_positions':[pos('Abstract',33,42),pos('Impact on Cython users',158,175)]},
        {'kind':'public_date_caveat','text':'The initial text reports presentation at a 2023-04-03 planning meeting. No meeting contents or immutable first meeting design were retrieved. The recorded initial_date is the verified numbered-NEP PR creation on 2023-04-13, and both dates remain in the same sampling period.', 'source_positions':[pos('Discussion',271,277)]}
    ],
    'named_original_families_components':[
        named(['NumPy','NumPy 1.17','NumPy 1.25','NumPy 2.0','SciPy','SciPy 1.10','Cython'],'Named target/downstream families and example versions','Abstract',15,42),
        named(['NPY_TARGET_VERSION','NPY_1_22_API_VERSION','NPY_NO_DEPRECATED_API','numpy2_compat','import_array()'],'Named target-selection and compatibility mechanisms','Motivation; Backwards compatible builds; API table changes',48,104),
        named(['PyArrayObject_fields','PyArray_Descr','PyDataType_ITEMSIZE','PyArray_DescrProto','NPY_MAXDIMS','PyArray_Mean','PyArray_Std','MapIter','theano'],'Named ABI/API changes and historic consumer','Breaking the C-API and changing the ABI',112,156),
        named(['CPython','subinterpreters','HPy','Cython 3','Cython 2.x','cimport numpy as cnp'],'Named context and tooling, including explicitly out-of-scope state changes','Adding state; Impact on Cython users',67,84),
        named(['PR 23528','scipy/oldest-supported-numpy','oldest-support-numpy'],'Explicit first implementation pointer and previous build strategy (draft spelling retained)','Implementation; Discussion; References',213,291)
    ],
    'whole_must':[
        pred('Q12-W01','Compile against newer NumPy while targeting an older API by default, with an explicit target-version selection mechanism and opt-in access to newer API.','Abstract; Backwards compatible builds',33,42,'Build an extension with newer headers and target NPY_1_22_API_VERSION. If only installing old build headers can target 1.22, the requested new-header build mechanism is absent.'),
        pred('Q12-W02','Hide struct fields and API functions introduced after the selected target unless the caller opts into a newer API surface.','Implementation',213,218,'At an old selected target, compile source that refers to a field/function introduced only after that target. If the default/old-target headers expose it as usable without opt-in, the gate is falsified.'),
        pred('Q12-W03','After recompilation/adaptation against NumPy 2.0, allow one downstream binary to work with both NumPy 1.x and 2.0, rather than requiring two incompatible binary distributions.','Abstract; End-user and packaging impact',22,42,'Compile one downstream extension against the 2.0 design and import it under the supported 1.x and 2.0 runtimes. Failure on either solely due to the intended cross-version compatibility mechanism falsifies the full migration goal.'),
        pred('Q12-W04','Support changed NumPy API tables with a compatibility layer translating the 1.x table into the 2.x table, integrated through import_array and reporting a missing required compatibility dependency.','NumPy 2 compatibility and API table changes',227,245,'Run a rebuilt extension on a 1.x runtime whose API table order/layout differs. Incorrect function pointers or absence of a useful import error when the compatibility layer is missing falsifies this design.'),
        pred('Q12-W05','Permit ABI evolution such as larger dtype item sizes/new flags while providing downstream adaptation interfaces for direct descriptor-field and static-DType users.','Breaking the C-API and changing the ABI',127,140,'A downstream dtype consumer reads itemsize or registers a static dtype after the descriptor layout changes. An unadaptable binary layout assumption, without the proposed accessor/descriptor bridge, fails this evolution requirement.'),
        pred('Q12-W06','Manage the C-API break through explicit downstream recompilation and documented replacements/adaptation for removed or changed API, keeping large state/context rewrites outside this proposal.','Adding state; Implementation; Backward compatibility',67,84,'A downstream extension using a changed/removed C-API entry must have a documented adaptation path after recompilation. Requiring every call to gain an unrelated HPy context, or no replacement guidance for a changed entry, fails the full migration boundary.')
    ],
    'partial_must':[
        pred('Q12-P01','Let the caller select the oldest supported NumPy API at compile time while using newer NumPy headers.','Backwards compatible builds',93,104,'With newer headers, request NPY_1_22_API_VERSION. Requiring a separate installation of 1.22 headers instead of honoring the target setting falsifies the partial operation.',inherits=['Q12-W01']),
        pred('Q12-P02','Default to an older compatible API and hide newer fields/functions unless a newer target is selected.','Abstract; Implementation',33,37,'Omit the target macro and attempt to reference an API addition newer than the advertised default target; exposure without opt-in falsifies the compatibility gate.',inherits=['Q12-W01','Q12-W02']),
        pred('Q12-P03','The resulting extension using only the selected API must actually be compatible with that older NumPy runtime; changing a preprocessor label alone is insufficient.','Backwards compatible builds',93,104,'Compile a source that uses only the selected baseline API with newer headers and load it on that baseline runtime. An ABI/import failure caused by the target mechanism falsifies the promised output.',inherits=['Q12-W01'])
    ],
    'independent_partial_purpose':'Build a downstream extension using current build headers while retaining an older runtime baseline. This directly removes the need to compile only against the oldest supported NumPy, even before NumPy 2.0 table/layout migration is implemented.',
    'remaining_adapter':'Set the version macro/build flag and choose a supported baseline in the extension build. Wider 2.0 compatibility still requires descriptor access adaptation, API-table translation/import handling, recompilation and packaging. If the adapter must hide new APIs or implement binary compatibility itself, the returned item has not completed this partial action.',
    'same_name_wrong_actor_output_failure':'CPython Py_LIMITED_API or a Python packaging requires-python marker selects a different actor/API boundary; neither proves compatibility with an older NumPy C-API. A version string printed by a build tool without controlling exported NumPy symbols or resulting binary compatibility also fails.',
    'neutral_query':'NumPy C API compile newer headers target older runtime API version',
    'a_queries':['NumPy NPY_TARGET_VERSION backward compatible extension builds','C API target version opt in new functions compile latest headers older runtime'],
    'first_text_sections':[pos('Abstract and scope',12,84),pos('Usage and impact',87,207),pos('Implementation and compatibility',210,268),pos('Discussion and references',271,297)],
    'initial_recovery':{'evidence_files':['raw/nep-53-pr-commits.json','raw/nep-53-pr-events.json','raw/nep-53-initial-commit.json'],'finding':'First PR commit bf0835ac... adds doc/neps/nep-0053-c-abi-evolution.md before PR creation; its committer time is 2023-04-13T17:26:40Z. The complete seven-event metadata response has no force-push. Later .rst filename/history begins only with a June formatting rename and was not treated as first text.','limitations':'Created header is 2022-04-10, while the actual first PR is in 2023 and the text reports an earlier 2023-04-03 meeting. Header/author dates are not public-availability evidence. The older meeting text remains unverified and does not move the sampling period.'}
})

# Add exact secondary positions for predicates spanning multiple initial sections.
extra_positions = {
    'Q09-W01':[pos('Proposed Weak Promotion',277,293)],
    'Q09-W02':[pos('Impact on NumPy arrays or scalars',105,112)],
    'Q10-W01':[pos('High-level design',175,215),pos('Appendix namespace selector',545,564)],
    'Q10-W02':[pos('Indexing',389,409),pos('The array object',416,426)],
    'Q10-W04':[pos('The dtype objects',467,473)],
    'Q11-W01':[pos('Python API',331,364),pos('Backward compatibility',285,290)],
    'Q11-W08':[pos('Python API',309,376),pos('Casts, ufuncs and string namespace',630,670),pos('Implementation',745,771)],
    'Q11-P01':[pos('Python API',331,341)],
    'Q11-P03':[pos('Python API',331,364)],
    'Q12-W01':[pos('Backwards compatible builds',93,107)],
    'Q12-W03':[pos('End-user and packaging impact',177,190)],
    'Q12-W06':[pos('Implementation',221,225),pos('Backward compatibility',263,268)],
    'Q12-P02':[pos('Implementation',213,218)]
}
for q in questions:
    for field in ['whole_must','partial_must']:
        for p in q[field]:
            p['source_positions'].extend(extra_positions.get(p['id'], []))
            if p['id']=='Q11-P01':
                p['falsifying_input']='Construct ["a", "é", "a much longer string"]. A fixed-width truncated result, a required maximum-width scan, or a generic Python list fails the partial storage/construction purpose.'

questions[1]['named_original_families_components'][1]['source_positions'].append(pos('Implementation',441,448))
questions[1]['named_original_families_components'][3]['source_positions'].extend([pos('Array object implementation',458,461),pos('Related Work',521,523),pos('Appendix namespace selector',545,564)])
questions[1]['named_original_families_components'][5]['source_positions'].append(pos('Related Work',525,528))
questions[2]['named_original_families_components'][3]['source_positions'].append(pos('Related Work',700,716))
questions[2]['named_original_families_components'][4]['source_positions'].extend([pos('History of string support',41,74),pos('String namespace and serialization',650,695)])
questions[2]['named_original_families_components'][5]['source_positions'].extend([pos('Cython Support',480,493),pos('Implementation',722,728),pos('References',814,820)])
questions[3]['named_original_families_components'][1]['source_positions'].append(pos('API table changes',227,245))
questions[3]['named_original_families_components'][3]['source_positions'].append(pos('Impact on Cython users',158,175))

revisions=[]
def move_branch(q, old_id, new_id, branch, reason, replacement=None):
    old=next(p for p in q['whole_must'] if p['id']==old_id)
    before=copy.deepcopy(old)
    alternative=copy.deepcopy(old)
    alternative.update(id=new_id, original_draft_predicate_id=old_id, branch=branch, aggregation='separate sensitivity only; not a universal whole/partial gate')
    q.setdefault('branch_specific_predicates',[]).append(alternative)
    if replacement:
        old['predicate']=replacement['predicate']
        old['source_positions']=replacement['source_positions']
        old['falsifying_input']=replacement['falsifying_input']
        old.pop('qualification',None)
        after=copy.deepcopy(old)
    else:
        q['whole_must'].remove(old)
        after=None
    revisions.append({'revision_id':'NUMPY-PRESEAL-'+old_id,'recorded_utc':NOW,'stage':'prospective input QA before any common or supplier search','question_id':q['id'],'reason':reason,'before':before,'after_universal_predicate':after,'retained_branch_predicate':alternative,'no_supplier_results_seen':True})

move_branch(questions[0],'Q09-W04','Q09-B01','strict integer conversion','The initial draft explicitly allows relaxing unsafe conversion to warning or silent wrapping and says it may be a separate issue (lines 335–338, 404–413). Preserve the proposed strict branch without making it necessary for the dtype-promotion outcome.')
move_branch(questions[0],'Q09-W05','Q09-B02','warn-and-infinity floating conversion','The selected operation is dtype promotion. The draft overflow conversion policy is retained as a separate branch, not a universal completion gate for the promotion/casting redesign.')
questions[0]['limits'][2]['text']='Strict integer overflow rejection and warning-plus-infinity for floating overflow are proposed conversion branches. Their original drafted predicates are retained under branch_specific_predicates; they are not universal whole_must or partial_must gates.'

move_branch(questions[3],'Q12-W04','Q12-B01','compatibility package with API-table translation','The first text explicitly allows header-only translation and notes that many changes could be made without the separate compatibility package (lines 232–257). Freeze the compatibility outcome, not one deployment architecture.',{
    'predicate':'Newly compiled downstream extensions must reach compatible runtime implementations when the NumPy C-API/ABI evolves across the supported runtimes; the compatibility integration must not dispatch through incompatible API-table entries.',
    'source_positions':[pos('Abstract',22,42),pos('NumPy 2 compatibility and API table changes',227,245)],
    'falsifying_input':'Import and execute the same rebuilt extension on supported NumPy 1.x and 2.0 runtimes after an API-table change. A call landing at an incompatible function pointer fails the outcome; a correct header-only bridge is not excluded merely for lacking a separate package.'
})
move_branch(questions[3],'Q12-W05','Q12-B02','illustrative PyArray_Descr layout and accessor changes','The draft explicitly labels concrete changes as examples and leaves additions case by case (lines 63–65, 112–114). Retain descriptor-specific sensitivity while requiring the broader C-API evolution/adaptation outcome.',{
    'predicate':'Allow substantive NumPy C-API/ABI evolution through downstream recompilation and documented adaptation, rather than requiring all old binary layouts and exposed API entries to remain frozen indefinitely.',
    'source_positions':[pos('Abstract',22,42),pos('Motivation and Scope',48,65),pos('Implementation',221,225)],
    'falsifying_input':'Propose a supported API removal or public-structure change with a documented downstream adaptation. A design that can maintain its compatibility promise only by forbidding every such C-API/ABI change fails the evolution goal.'
})

move_branch(questions[2],'Q11-W04','Q11-B01','per-array arena with npy_static_string metadata','The arena and exact struct are the initial proposed storage branch. The universal requirement is datatype-managed variable-length storage and downstream access, permitting alternative storage layouts that deliver the same requested operations.',{
    'predicate':'Provide datatype-managed variable-width UTF-8 storage and a supported C interface for allocation, copying and freeing, so downstream code can use string-array data without reducing it to generic Python-object references.',
    'source_positions':[pos('Proposed work',124,142),pos('Memory layout and Managing Heap Allocations',383,421)],
    'falsifying_input':'A downstream C operation needs supported access to the typed string buffers. A generic Python-object array with no datatype-managed string storage or C allocation/access interface fails; a safe alternative allocator is not excluded solely for its layout.'
})
move_branch(questions[2],'Q11-W05','Q11-B02','two-mode arena allocator with specified locking','In-place mutation and safe concurrent access are the requested outcomes. The two-mode arena and exact locking layout are a proposed implementation branch, not a universal requirement.',{
    'predicate':'Support in-place string mutation, including length growth, without data races or use-after-free within the advertised concurrent-access contract.',
    'source_positions':[pos('Mutation and Thread Safety',437,478)],
    'falsifying_input':'Enlarge a string while another thread accesses it under the implementation\'s documented supported concurrency contract. A use-after-free or data race, or forbidding all element mutation, fails the outcome; a different safe synchronization scheme does not.'
})
move_branch(questions[2],'Q11-W07','Q11-B03','npy version 4.0 sidecar serialization','Variable-width string serialization without mandatory pickle is an initial proposed work outcome. Exact version 4.0 and sidecar_size representation are one proposed format branch, retained separately.',{
    'predicate':'Support lossless NumPy npy/npz serialization of variable-width string data without requiring pickle, and support pickling/unpickling when requested.',
    'source_positions':[pos('Proposed work',141,142),pos('Serialization',672,695)],
    'falsifying_input':'Save/reload a variable-width string array with long and non-ASCII elements under allow_pickle=False. Refusal or string loss fails; a supported safe format encoding need not use the exact initially proposed version-4 sidecar header.'
})

for q in questions:
    q['first_text']['read_sections'] = q['first_text_sections']
    for field in ['whole_must','partial_must','branch_specific_predicates']:
        if field not in q:
            q[field]=[]
        for p in q[field]:
            p['source_id'] = q['id']+'-FIRST'
    q['mandatory_interpretation']='whole_must/partial_must express required operational outcomes. Proposed architecture branches and illustrative changes are separately retained in branch_specific_predicates and cannot independently change the universal completion label.'
    q['preseal_qa_revisions']=[r['revision_id'] for r in revisions if r['question_id']==q['id']]
    q['novelty_limit'] = 'All named families, components and linked prototypes in the first text are explicit prior input; a returned page for the same named use cannot be labeled a previously unnamed discovery. Human author knowledge remains unknown.'
    q['sampling_exposure']={'later_status_metadata_seen':True,'first_text_only_selection_and_query_rule':True,'details_path':REPO_PREFIX+'exposures.jsonl','interpretation':'Do not call the sampling reader status-blind; status words were exposed incidentally during metadata recovery but were not used in the frozen hash traversal or query construction.'}

(ROOT/'questions.jsonl').write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in questions))
(ROOT/'predicate-revisions.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in revisions))
(ROOT/'first-text-link-inventory.json').write_text(json.dumps({q['id']:sorted(set(re.findall(r'https?://[^\s<>`]+', (ROOT/'first_texts'/META[q['id']]['file']).read_text()))) for q in questions},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'questions':[(q['id'],q['canonical_id'],q['whole_or_partial']) for q in questions], 'checked_utc':NOW,'file':'questions.jsonl'},indent=2))
