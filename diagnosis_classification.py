import re


def word_boundary_pattern_wrap(pattern_list):
    pattern_str = r'\b(' + '|'.join(pattern_list) + r')\b'
    return re.compile(pattern_str, re.IGNORECASE)


def overall_exclusion_pattern_wrap(pattern_list):
    pattern_str = '(' + '|'.join(pattern_list) + ')'
    return re.compile(pattern_str, re.IGNORECASE)


def is_cancer(diag_str):
    overall_exclusion_re = overall_exclusion_pattern_wrap([
        r'^\s*\?',            # queries
        r'\bscreen(ing)?\b',  # tests for cancer
    ])

    inclusion_re = word_boundary_pattern_wrap([
        'cancer',
        'cancerous'
        r'malig\w*',
        'ca',
        r'carc\w*',
        r'adenoca\w*',
        r'tumo\w*',
    ])

    exclusion_re = word_boundary_pattern_wrap([
        'skin',
        'fear',
        'worried',
        'fhx',
        'family history',
        'husband',
        'fob...negative',
        'h/t',
        'lentigo',
        'compression',
        'pre',
        'no',
        'not',
        'coronary',
        'oxalate',
        'review',
        'basal',
        'adrenal',
        'pituitary',
        'proclatin',
        '.benign',
    ])

    if not overall_exclusion_re.search(diag_str):
        if (inclusion_re.search(diag_str) and
                not exclusion_re.search(diag_str)):
            return 1
    return 0


def is_metastatic_disease(diag_str):
    overall_exclusion_re = overall_exclusion_pattern_wrap([
        r'^\s*\?',            # queries
        r'\bscreen(ing)?\b',  # tests for cancer
    ])

    inclusion_re = word_boundary_pattern_wrap([
        r'metas\w*',
    ])

    if not overall_exclusion_re.search(diag_str):
        if inclusion_re.search(diag_str):
            return 1
    return 0


def is_chemotherapy(diag_str):
    inclusion_re = word_boundary_pattern_wrap([
        r'chemo\w*',
    ])

    if inclusion_re.search(diag_str):
        return 1
    return 0


def is_radiotherapy(diag_str):
    inclusion_re = word_boundary_pattern_wrap([
        r'radiot\w*',
        r'radiation*',
    ])

    exclusion_re = word_boundary_pattern_wrap([
        'bbc',
    ])

    if (inclusion_re.search(diag_str) and
            not exclusion_re.search(diag_str)):
        return 1
    return 0


def is_dementia(diag_str):
    overall_exclusion_re = overall_exclusion_pattern_wrap([
        r'^\s*\?',
        r'\bscreen(ing)?\b',
        r'\bearly\b',
        r'\bmild\b',
        r'\bpseudo.?\w*\b',
        r'\brequest\b'
    ])

    inclusion_re = word_boundary_pattern_wrap([
        r'alz\w*',
        r'demen\w*',
    ])

    if not overall_exclusion_re.search(diag_str):
        if (inclusion_re.search(diag_str)):
            return 1
    return 0


def is_chronic_heart_failure(diag_str):
    overall_exclusion_re = overall_exclusion_pattern_wrap([
        r'^\s*\?',
        r'\bmild\b',
    ])

    inclusion_re = word_boundary_pattern_wrap([
        'chf',
        'ccf',
        r'heart fail\w*',
        r'cardiac fail\w*',
    ])

    exclusion_re = word_boundary_pattern_wrap([
        'no',
    ])

    if not overall_exclusion_re.search(diag_str):
        if (inclusion_re.search(diag_str) and
                not exclusion_re.search(diag_str)):
            return 1
    return 0


def is_copd(diag_str):
    overall_exclusion_re = overall_exclusion_pattern_wrap([
        r'^\s*\?',
    ])

    inclusion_re = word_boundary_pattern_wrap([
        'copd',
        'emphysema',
        'airways limitation',
        'chronic obstructive pulmonary disease',
        'cal',
    ])

    exclusion_re = word_boundary_pattern_wrap([
        'spur',
    ])

    if not overall_exclusion_re.search(diag_str):
        if (inclusion_re.search(diag_str) and
                not exclusion_re.search(diag_str)):
            return 1
    return 0


def is_chronic_renal_failure(diag_str):
    inclusion_re = word_boundary_pattern_wrap([
        'kidney failure',
        'kidney disease',
        'renal failure',
        'renal disease',
        'crf',
        r'\w*dialysis\w*',
    ])

    exclusion_re = word_boundary_pattern_wrap([
        'acute',
    ])

    if (inclusion_re.search(diag_str) and
            not exclusion_re.search(diag_str)):
        return 1
    return 0


def is_stage_4_or_5_renal_failure(diag_str):
    inclusion_re = word_boundary_pattern_wrap([
        'end stage',
        'stage 4',
        'stage 5',
        'stage iv',
        'stage v',
    ])

    if (is_chronic_renal_failure(diag_str) and
            inclusion_re.search(diag_str)):
        return 1
    return 0


def is_dialysis(diag_str):
    inclusion_re = word_boundary_pattern_wrap([
        r'\w*dialysis\w*',
    ])

    if (is_chronic_renal_failure(diag_str) and
            inclusion_re.search(diag_str)):
        return 1
    return 0


def is_chronic_liver_failure(diag_str):
    overall_exclusion_re = overall_exclusion_pattern_wrap([
        r'^\s*\?',
    ])

    inclusion_re = word_boundary_pattern_wrap([
        'liver failure',
        'hepatic failure',
        'liver disease',
        'hepatic disease',
        'ascites',
        r'cirrh\w*',
        'encephalopathy',
        'variceal'
    ])

    exclusion_re = word_boundary_pattern_wrap([
        'empathis',
        'mild',
        'biliary'
    ])

    if not overall_exclusion_re.search(diag_str):
        if (inclusion_re.search(diag_str) and
                not exclusion_re.search(diag_str)):
            return 1
    return 0


def classify(diagnosis):
    diag_str = str(diagnosis).casefold()

    return {
        'cancer': is_cancer(diag_str),
        'metastatic_disease': is_metastatic_disease(diag_str),
        'chemotherapy': is_chemotherapy(diag_str),
        'radiotherapy': is_radiotherapy(diag_str),
        'dementia': is_dementia(diag_str),
        'chronic_heart_failure': is_chronic_heart_failure(diag_str),
        'copd': is_copd(diag_str),
        'chronic_renal_failure': is_chronic_renal_failure(diag_str),
        'stage_4_or_5_renal_failure': is_stage_4_or_5_renal_failure(diag_str),
        'dialysis': is_dialysis(diag_str),
        'chronic_liver_failure': is_chronic_liver_failure(diag_str),
    }
