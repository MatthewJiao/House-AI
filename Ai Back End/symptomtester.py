import tensorflow as tf
import numpy as np
import pandas as pd

import re
import nltk
#nltk.download('stopwords')
#nltk.download('wordnet')

nltk.data.path.append("./nltk_data")

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Flatten, Dense, Embedding, Conv1D, GlobalMaxPooling1D, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

from numpy import array
from numpy import argmax

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

NLmodel = keras.models.load_model('symptoms_model4good.h5')


# stopwords = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]


#regenerated every time model is run
word_index = {'<OOV>': 1, 'pain': 2, 'muscle': 3, 'disorder': 4, 'blood': 5, 'use': 6, 'skin': 7, 'body': 8, 'low': 9, 'eye': 10, 'feel': 11, 'avoid': 12, 'syndrome': 13, 'high': 14, 'movement': 15, 'food': 16, 'eat': 17, 'take': 18, 'stop': 19, 'breath': 20, 'level': 21, 'drink': 22, 'sensation': 23, 'paralysis': 24, 'fluid': 25, 'hand': 26, 'abnormal': 27, 'loss': 28, 'cough': 29, 'drug': 30, 'heart': 31, 'change': 32, 'water': 33, 'weight': 34, 'urine': 35, 'keep': 36, 'sound': 37, 'chest': 38, 'bleeding': 39, 'swell': 40, 'yellow': 41, 'sputum': 42, 'cannot': 43, 'discomfort': 44, 'alcohol': 45, 'side': 46, 'cold': 47, 'leg': 48, 'aphasia': 49, 'fever': 50, 'foot': 51, 'hurt': 52, 'stomach': 53, 'lie': 54, 'sudden': 55, 'decrease': 56, 'weakness': 57, 'pupil': 58, 'increase': 59, 'area': 60, 'joint': 61, 'cause': 62, 'limb': 63, 'consume': 64, 'swollen': 65, 'itch': 66, 'murmur': 67, 'inability': 68, 'progressive': 69, 'hard': 70, 'excessive': 71, 'pressure': 72, 'sleep': 73, 'neck': 74, 'bath': 75, 'abdomen': 76, 'difficulty': 77, 'small': 78, 'face': 79, 'pee': 80, 'breathing': 81, 'speech': 82, 'stool': 83, 'abnormally': 84, 'burning': 85, 'history': 86, 'hallucination': 87, 'gait': 88, 'red': 89, 'tissue': 90, 'control': 91, 'damage': 92, 'nose': 93, 'neem': 94, 'vomit': 95, 'effect': 96, 'seizure': 97, 'state': 98, 'mood': 99, 'mental': 100, 'back': 101, 'lack': 102, 'spin': 103, 'warm': 104, 'abdominal': 105, 'swallow': 106, 'tremor': 107, 'vision': 108, 'large': 109, 'memory': 110, 'auditory': 111, 'dry': 112, 'sweat': 113, 'sickness': 114, 'behavior': 115, 'normal': 116, 'loose': 117, 'hot': 118, 'respiratory': 119, 'wave': 120, 'spasm': 121, 'mass': 122, 'amnesia': 123, 'involuntary': 124, 'language': 125, 'symptom': 126, 'juice': 127, 'smell': 128, 'general': 129, 'irritation': 130, 'sore': 131, 'baby': 132, 'unable': 133, 'heavy': 134, 'motor': 135, 'air': 136, 'output': 137, 'salt': 138, 'positive': 139, 'balance': 140, 'nail': 141, 'poor': 142, 'flare': 143, 'reflex': 144, 'compress': 145, 'slow': 146, 'throat': 147, 'para': 148, 'stiffness': 149, 'pulse': 150, 'bathing': 151, 'ataxia': 152, 'manifestation': 153, 'non': 154, 'cloth': 155, 'temperature': 156, 'check': 157, 'try': 158, 'nerve': 159, 'morbid': 160, 'probiotic': 161, 'lip': 162, 'family': 163, 'cardiac': 164, 'sinus': 165, 'painful': 166, 'leaf': 167, 'chronic': 168, 'st': 169, 'segment': 170, 'move': 171, 'vein': 172, 'gravida': 173, 'twitch': 174, 'productive': 175, 'lesion': 176, 'neurologic': 177, 'wash': 178, 'cover': 179, 'fall': 180, 'liver': 181, 'milk': 182, 'due': 183, 'receive': 184, 'tonic': 185, 'sign': 186, 'perceptual': 187, 'antibiotic': 188, 'disease': 189, 'nasal': 190, 'stiff': 191, 'pregnancy': 192, 'systolic': 193, 'status': 194, 'psychomotor': 195, 'motion': 196, 'unsteadiness': 197, 'unconsciousness': 198, 'concentrate': 199, 'rapid': 200, 'lung': 201, 'impaired': 202, 'consciousness': 203, 'one': 204, 'visual': 205, 'sneeze': 206, 'vitamin': 207, 'consumption': 208, 'spot': 209, 'redness': 210, 'suicidal': 211, 'appetite': 212, 'acute': 213, 'facial': 214, 'distress': 215, 'node': 216, 'zero': 217, 'mucus': 218, 'posturing': 219, 'agitation': 220, 'worry': 221, 'much': 222, 'pu': 223, 'primary': 224, 'depression': 225, 'tenderness': 226, 'wet': 227, 'mosquito': 228, 'rate': 229, 'membrane': 230, 'fatigue': 231, 'unsteady': 232, 'walk': 233, 'early': 234, 'palsy': 235, 'event': 236, 'age': 237, 'left': 238, 'anus': 239, 'rest': 240, 'apraxia': 241, 'obesity': 242, 'consult': 243, 'akathisia': 244, 'maintain': 245, 'cell': 246, 'head': 247, 'energy': 248, 'fear': 249, 'partial': 250, 'scar': 251, 'deep': 252, 'therapy': 253, 'enlarge': 254, 'stand': 255, 'bowel': 256, 'time': 257, 'protein': 258, 'learn': 259, 'coordination': 260, 'mouth': 261, 'syncope': 262, 'continuous': 263, 'induced': 264, 'ophthalmoplegia': 265, 'eats': 266, 'space': 267, 'intolerance': 268, 'two': 269, 'urination': 270, 'numbness': 271, 'claudication': 272, 'retardation': 273, 'healthy': 274, 'prolong': 275, 'shortness': 276, 'get': 277, 'communication': 278, 'irregular': 279, 'passing': 280, 'paraparesis': 281, 'touch': 282, 'open': 283, 'rigidity': 284, 'labor': 285, 'feces': 286, 'spell': 287, 'weak': 288, 'buildup': 289, 'tightness': 290, 'restlessness': 291, 'blackout': 292, 'concentration': 293, 'wheeze': 294, 'little': 295, 'less': 296, 'flat': 297, 'light': 298, 'patch': 299, 'cerebrospinal': 300, 'passage': 301, 'gas': 302, 'always': 303, 'dizzy': 304, 'fatty': 305, 'away': 306, 'affect': 307, 'piriformis': 308, 'mild': 309, 'cord': 310, 'birth': 311, 'inflame': 312, 'lose': 313, 'egophony': 314, 'moan': 315, 'fetal': 316, 'cramp': 317, 'calcium': 318, 'unwell': 319, 'heme': 320, 'vessel': 321, 'confusion': 322, 'rhinorrhea': 323, 'near': 324, 'persistent': 325, 'proper': 326, 'still': 327, 'long': 328, 'arm': 329, 'failure': 330, 'deprivation': 331, 'ramble': 332, 'thinness': 333, 'remove': 334, 'scab': 335, 'horner': 336, 'activity': 337, 'sleepy': 338, 'tingle': 339, 'urinary': 340, 'association': 341, 'witch': 342, 'hazel': 343, 'phlegm': 344, 'gag': 345, 'todd': 346, 'tire': 347, 'epsom': 348, 'hoard': 349, 'spontaneous': 350, 'rupture': 351, 'bump': 352, 'go': 353, 'mark': 354, 'thicken': 355, 'period': 356, 'withdraw': 357, 'calamine': 358, 'case': 359, 'silver': 360, 'like': 361, 'dust': 362, 'soft': 363, 'hemorrhage': 364, 'behind': 365, 'contain': 366, 'exercise': 367, 'know': 368, 'allergy': 369, 'rusty': 370, 'call': 371, 'ambulance': 372, 'rash': 373, 'desire': 374, 'renal': 375, 'angle': 376, 'blur': 377, 'external': 378, 'hip': 379, 'flash': 380, 'edema': 381, 'cranberry': 382, 'waste': 383, 'thistle': 384, 'impairment': 385, 'paresis': 386, 'strange': 387, 'extremeties': 388, 'orthostatic': 389, 'internal': 390, 'calorie': 391, 'vegitables': 392, 'extreme': 393, 'acupuncture': 394, 'rectum': 395, 'breast': 396, 'fetus': 397, 'inflammatory': 398, 'stone': 399, 'fecaluria': 400, 'refer': 401, 'brown': 402, 'sequard': 403, 'feminization': 404, 'infect': 405, 'crust': 406, 'ooze': 407, 'hospital': 408, 'switch': 409, 'cloothing': 410, 'breathlessness': 411, 'massage': 412, 'gerstmann': 413, 'illusion': 414, 'pulsus': 415, 'paradoxus': 416, 'trigger': 417, 'disequilibrium': 418, 'vegetative': 419, 'absence': 420, 'solid': 421, 'stable': 422, 'sugary': 423, 'big': 424, 'nodal': 425, 'eruption': 426, 'papaya': 427, 'terrify': 428, 'blackhead': 429, 'calm': 430, 'mediastinal': 431, 'sugar': 432, 'debilitation': 433, 'ice': 434, 'synkinesis': 435, 'contraction': 436, 'green': 437, 'elevation': 438, 'phantom': 439, 'previous': 440, 'korsakoff': 441, 'feverish': 442, 'throb': 443, 'quality': 444, 'vocal': 445, 'seek': 446, 'help': 447, 'knee': 448, 'unresponsiveness': 449, 'unsterile': 450, 'injection': 451, 'monoclonal': 452, 'blotch': 453, 'public': 454, 'hopeless': 455, 'hematocrit': 456, 'consistency': 457, 'hyperkinesis': 458, 'shallow': 459, 'fast': 460, 'lymph': 461, 'detol': 462, 'stahli': 463, 'line': 464, 'otc': 465, 'reliver': 466, 'spinal': 467, 'slur': 468, 'tic': 469, 'psychophysiologic': 470, 'smack': 471, 'vaccine': 472, 'supranuclear': 473, 'extrapyramidal': 474, 'spicy': 475, 'heating': 476, 'pad': 477, 'pack': 478, 'find': 479, 'lemon': 480, 'balm': 481, 'bandage': 482, 'wheelchair': 483, 'infantile': 484, 'apparent': 485, 'life': 486, 'threaten': 487, 'neologism': 488, 'atrophy': 489, 'rhythm': 490, 'stuffy': 491, 'prodrome': 492, 'prostate': 493, 'tumor': 494, 'invasion': 495, 'condition': 496, 'structure': 497, 'rhd': 498, 'inappropriate': 499, 'system': 500, 'compression': 501, 'radioactive': 502, 'iodine': 503, 'treatment': 504, 'invert': 505, 'feed': 506, 'withdrawal': 507, 'translucency': 508, 'superimposition': 509, 'presence': 510, 'spasticity': 511, 'verbally': 512, 'abusive': 513, 'atrial': 514, 'verbal': 515, 'sip': 516, 'toxic': 517, 'look': 518, 'typhos': 519, 'aura': 520, 'poo': 521, 'date': 522, 'slit': 523, 'ventricle': 524, 'absent': 525, 'first': 526, 'diet': 527, 'night': 528, 'idiopathic': 529, 'venous': 530, 'dark': 531, 'come': 532, 'around': 533, 'rub': 534, 'peel': 535, 'micturition': 536, 'scurring': 537, 'patient': 538, 'clean': 539, 'belly': 540, 'region': 541, 'esophagus': 542, 'bubble': 543, 'mutism': 544, 'hack': 545, 'soapy': 546, 'roll': 547, 'disturbance': 548, 'abrupt': 549, 'beat': 550, 'nonfluent': 551, 'sensory': 552, 'headache': 553, 'susac': 554, 'fruit': 555, 'fiberous': 556, 'meningism': 557, 'tone': 558, 'prominent': 559, 'calf': 560, 'neurobehavioral': 561, 'meditation': 562, 'thyroid': 563, 'speak': 564, 'myalgia': 565, 'neuralgia': 566, 'raise': 567, 'intermittent': 568, 'potassium': 569, 'show': 570, 'murphy': 571, 'swing': 572, 'urinoma': 573, 'pin': 574, 'illness': 575, 'brain': 576, 'echolalia': 577, 'stutter': 578, 'woman': 579, 'wear': 580, 'ppe': 581, 'possible': 582, 'episode': 583, 'ear': 584, 'word': 585, 'transfusion': 586, 'poloroid': 587, 'glass': 588, 'sun': 589, 'tongue': 590, 'choke': 591, 'uncontrollably': 592, 'estrogen': 593, 'rigor': 594, 'associate': 595, 'observation': 596, 'spleen': 597, 'vasovagal': 598, 'bloody': 599, 'rhonchus': 600, 'bruising': 601, 'unknown': 602, 'origin': 603, 'need': 604, 'lethargy': 605, 'floppy': 606, 'fremitus': 607, 'anxiety': 608, 'bloating': 609, 'urge': 610, 'incontinence': 611, 'catch': 612, 'regurgitates': 613, 'soak': 614, 'affected': 615, 'nervous': 616, 'hydrate': 617, 'hold': 618, 'rich': 619, 'oily': 620, 'feature': 621, 'indifferent': 622, 'ejection': 623, 'vaccination': 624, 'thought': 625, 'becomes': 626, 'barking': 627, 'mucous': 628, 'hyperemesis': 629, 'writhe': 630, 'dent': 631, 'anal': 632, 'sleepiness': 633, 'pericardial': 634, 'bladder': 635, 'scratch': 636, 'gasp': 637, 'doctor': 638, 'oxygen': 639, 'milky': 640, 'distort': 641, 'binge': 642, 'aggravate': 643, 'factor': 644, 'dullness': 645, 'yellowish': 646, 'well': 647, 'person': 648, 'nodule': 649, 'bad': 650, 'amount': 651, 'sunken': 652, 'jugular': 653, 'ease': 654, 'see': 655, 'cognition': 656, 'vapour': 657, 'noisy': 658, 'pimple': 659, 'welt': 660, 'oinments': 661, 'follow': 662, 'infant': 663, 'hesitation': 664, 'conduction': 665, 'thin': 666, 'pass': 667, 'write': 668, 'pansystolic': 669, 'friction': 670, 'apply': 671, 'brittle': 672, 'gurgle': 673, 'sting': 674, 'frail': 675, 'nightmare': 676, 'flow': 677, 'hypotension': 678, 'dentition': 679, 'tender': 680, 'mucoid': 681, 'foul': 682, 'clear': 683, 'dehydration': 684, 'room': 685, 'groggy': 686, 'coma': 687, 'torticollis': 688, 'fainting': 689, 'inflammation': 690, 'ache': 691, 'mobility': 692, 'limitation': 693, 'asthenia': 694, 'purpura': 695, 'sex': 696, 'aloe': 697, 'vera': 698, 'anterograde': 699, 'chill': 700, 'sadness': 701, 'physical': 702, 'icterus': 703, 'stream': 704, 'shoot': 705, 'homicidal': 706, 'dizziness': 707, 'qt': 708, 'interval': 709, 'heberden': 710, 'white': 711, 'lot': 712, 'bleed': 713, 'erythema': 714, 'projectile': 715, 'dyspnea': 716, 'snuffle': 717, 'guaiac': 718, 'understand': 719, 'asterixis': 720, 'focal': 721, 'quick': 722, 'plenty': 723, 'thoroughly': 724, 'hypokinesia': 725, 'bruit': 726, 'vagina': 727, 'congestion': 728, 'delirium': 729, 'indigestion': 730, 'intermenstrual': 731, 'otorrhea': 732, 'spastic': 733, 'complication': 734, 'colic': 735, 'dystonia': 736, 'anisocoria': 737, 'distention': 738, 'severe': 739, 'incoherent': 740, 'dont': 741, 'pallor': 742, 'fill': 743, 'proteinuria': 744, 'asymptomatic': 745, 'mydriasis': 746, 'result': 747, 'frothy': 748, 'hyperhidrosis': 749, 'adverse': 750, 'religious': 751, 'belief': 752, 'voice': 753, 'raspy': 754, 'strain': 755, 'rough': 756, 'broca': 757, 'uncontrollable': 758, 'miosis': 759, 'circulation': 760, 'anti': 761, 'sense': 762, 'distend': 763, 'monocytosis': 764, 'point': 765, 'sensitivity': 766, 'athetosis': 767, 'albumin': 768, 'lightheadedness': 769, 'decompensation': 770, 'finger': 771, 'reduce': 772, 'stress': 773, 'growth': 774, 'emphysematous': 775, 'kill': 776, 'inhale': 777, 'exhale': 778, 'difficult': 779, 'drinking': 780, 'metatarsalgia': 781, 'sniffle': 782, 'tylenol': 783, 'diarrhea': 784, 'moody': 785, 'development': 786, 'hyponatremia': 787, 'pas': 788, 'emaciation': 789, 'muscular': 790, 'color': 791, 'intestine': 792, 'prostatism': 793, 'premature': 794, 'posterior': 795, 'agnosia': 796, 'many': 797, 'product': 798, 'hypercapnia': 799, 'dyskinesia': 800, 'disturbed': 801, 'upset': 802, 'drowsiness': 803, 'fat': 804, 'cyanosis': 805, 'polymyalgia': 806, 'prosopagnosia': 807, 'musculuar': 808, 'hydropneumothorax': 809, 'cut': 810, 'paraplegia': 811, 'imitate': 812, 'gesture': 813, 'metastatic': 814, 'homonymous': 815, 'hemianopsia': 816, 'breech': 817, 'presentation': 818, 'sleeplessness': 819, 'narrow': 820, 'right': 821, 'intake': 822, 'ascites': 823, 'reading': 824, 'tetany': 825, 'hunger': 826, 'hypertonicity': 827, 'onset': 828, 'underweight': 829, 'voluntary': 830, 'titubation': 831, 'frozen': 832, 'injury': 833, 'brainstem': 834, 'enuresis': 835, 'weep': 836, 'medicine': 837, 'homelessness': 838, 'full': 839, 'meal': 840, 'aspirin': 841, 'pseudobulbar': 842, 'hyperactive': 843, 'sensitive': 844, 'abortion': 845, 'myokymia': 846, 'catatonia': 847, 'autoimmune': 848, 'clumsiness': 849, 'tenesmus': 850, 'retrograde': 851, 'exhaustion': 852, 'sweling': 853, 'produce': 854, 'anorexia': 855, 'awaken': 856, 'watery': 857, 'limit': 858, 'cachexia': 859, 'uncoordination': 860, 'organ': 861, 'platelet': 862, 'drool': 863, 'seize': 864, 'retropulsion': 865, 'angina': 866, 'pectoris': 867, 'haemoptysis': 868, 'dyslexia': 869, 'pustule': 870, 'lotion': 871, 'hepatomegaly': 872, 'sway': 873, 'sedentary': 874, 'transient': 875, 'global': 876, 'unhappy': 877, 'bradykinesia': 878, 'greasy': 879, 'extremely': 880, 'alcoholic': 881, 'confine': 882, 'bed': 883, 'old': 884, 'specific': 885, 'hirsutism': 886, 'excruciate': 887, 'airway': 888, 'hypotonia': 889, 'ecchymosis': 890, 'harsh': 891, 'neurological': 892, 'cheek': 893, 'enlargement': 894, 'hemodynamically': 895, 'giddy': 896, 'past': 897, 'abscess': 898, 'myotonia': 899, 'express': 900, 'dysuria': 901, 'alien': 902, 'shake': 903, 'scleral': 904, 'chew': 905, 'hyperkalemia': 906, 'malaise': 907, 'bound': 908, 'respiration': 909, 'gastroparesis': 910, 'perceive': 911, 'pitch': 912, 'disrupt': 913, 'airflow': 914, 'shift': 915, 'tract': 916, 'size': 917, 'wernicke': 918, 'half': 919, 'blanch': 920, 'stab': 921, 'cerebellum': 922, 'hypokalemia': 923, 'pregnant': 924, 'primigravida': 925, 'perspiration': 926, 'clammy': 927, 'urgency': 928, 'hypersomnia': 929, 'alter': 930, 'sensorium': 931, 'hypotonic': 932, 'sodium': 933, 'alertness': 934, 'skeletal': 935, 'make': 936, 'sciatica': 937, 'nausea': 938, 'flush': 939, 'overweight': 940, 'weepiness': 941, 'easily': 942, 'hypoalbuminemia': 943, 'tinnitus': 944, 'deviation': 945, 'bruise': 946, 'flatulence': 947, 'cicatrisation': 948, 'ideomotor': 949, 'function': 950, 'sit': 951, 'gain': 952, 'hyperacusis': 953, 'dysdiadochokinesia': 954, 'confuse': 955, 'freeze': 956, 'cardiomegaly': 957, 'aphagia': 958, 'bedridden': 959, 'lump': 960, 'retch': 961, 'macrosomia': 962, 'pound': 963, 'upper': 964, 'frequent': 965, 'volume': 966, 'twice': 967, 'excitement': 968, 'hemiplegia': 969, 'pocket': 970, 'perform': 971, 'cyst': 972, 'hematuria': 973, 'photopsia': 974, 'myoclonus': 975, 'intoxicate': 976, 'especially': 977, 'drain': 978, 'tiredness': 979, 'physician': 980, 'hypertonia': 981, 'dilation': 982, 'tachypnea': 983, 'macule': 984, 'nervousness': 985, 'gland': 986, 'thrombocytopenic': 987, 'stridor': 988, 'breakthrough': 989, 'trismus': 990, 'paresthesia': 991, 'runny': 992, 'empty': 993, 'place': 994, 'ambidexterity': 995, 'lockjaw': 996, 'fasciculation': 997, 'start': 998, 'oneself': 999, 'day': 1000, 'perspire': 1001, 'emphysema': 1002, 'familiar': 1003, 'recognize': 1004, 'relaxation': 1005, 'intractable': 1006, 'dysarthria': 1007, 'atypia': 1008, 'drop': 1009, 'saliva': 1010, 'vegan': 1011, 'acidity': 1012, 'alexia': 1013, 'buttock': 1014, 'digest': 1015, 'certain': 1016, 'transgender': 1017, 'hypesthesia': 1018, 'inherit': 1019, 'urgently': 1020, 'urinate': 1021, 'brief': 1022, 'nonsmoker': 1023, 'sclera': 1024, 'blister': 1025, 'polyuria': 1026, 'arthralgia': 1027, 'babinski': 1028, 'heartburn': 1029, 'formication': 1030, 'hallucinate': 1031, 'hypoxemia': 1032, 'cystic': 1033, 'itchy': 1034, 'anomia': 1035, 'involves': 1036, 'purulent': 1037, 'dysesthesia': 1038, 'irritability': 1039, 'erratic': 1040, 'trunk': 1041, 'cancerous': 1042, 'hypocalcemia': 1043, 'unresponsive': 1044, 'puffy': 1045, 'charleyhorse': 1046, 'nod': 1047, 'cardiovascular': 1048, 'intoxication': 1049, 'overflow': 1050, 'tear': 1051, 'discoloration': 1052, 'stupor': 1053, 'bacteria': 1054, 'sarcopenia': 1055, 'discolor': 1056, 'phonophobia': 1057, 'whistle': 1058, 'cognitive': 1059, 'pneumatouria': 1060, 'discharge': 1061, 'ring': 1062, 'elation': 1063, 'contact': 1064, 'without': 1065, 'child': 1066, 'transaminitis': 1067, 'coldness': 1068, 'wound': 1069, 'hypertrophy': 1070, 'number': 1071, 'alternate': 1072, 'happy': 1073, 'chorea': 1074, 'carbon': 1075, 'dioxide': 1076, 'postherpetic': 1077, '10': 1078, 'ball': 1079, 'hepatosplenomegaly': 1080, 'medication': 1081, 'overload': 1082, 'colon': 1083, 'rectal': 1084, 'clonus': 1085, 'bluish': 1086, 'cast': 1087, 'immobile': 1088, 'satiety': 1089, 'convolute': 1090, 'toe': 1091, 'delicate': 1092, 'coarse': 1093, 'hair': 1094, 'shiver': 1095, 'compliance': 1096, 'jerk': 1097, 'sad': 1098, 'orthostasis': 1099, 'proteinemia': 1100, 'achalasia': 1101, 'pigmentation': 1102, 'daze': 1103, 'phrase': 1104, 'repeat': 1105, 'oliguria': 1106, 'mainly': 1107, 'catalepsy': 1108, 'alovera': 1109, 'incomprehensible': 1110, 'vertigo': 1111, 'excess': 1112, 'cortisol': 1113, 'hormone': 1114, 'clumsy': 1115, 'photophobia': 1116, 'sharpness': 1117, 'palpitation': 1118, 'within': 1119, 'plerual': 1120, 'wake': 1121, 'snore': 1122, 'haemorrhage': 1123, 'wryneck': 1124, 'hemifacial': 1125, 'cavity': 1126, 'decerebrate': 1127, 'maintan': 1128, 'pull': 1129, 'local': 1130, 'bright': 1131, 'flutter': 1132, 'hematochezia': 1133, 'degenerative': 1134, 'total': 1135, 'four': 1136, 'torso': 1137, 'profusely': 1138, 'quadriplegia': 1139, 'distinct': 1140, 'dyspareunia': 1141, 'medical': 1142, 'care': 1143, 'frighten': 1144, 'unpleasant': 1145, 'dream': 1146, 'lethargic': 1147, 'hypothermia': 1148, 'pericarditis': 1149, 'polydipsia': 1150, 'create': 1151, 'new': 1152, 'aborted': 1153, 'itchiness': 1154, 'articulation': 1155, 'affair': 1156, 'holosystolic': 1157, 'hypometabolism': 1158, 'dyschromic': 1159, 'outcome': 1160, 'veg': 1161, 'solute': 1162, 'hypoproteinemia': 1163, 'anosmia': 1164, 'smoke': 1165, 'discolouration': 1166, 'underneath': 1167, 'thirstiness': 1168, 'menstruation': 1169, 'pleuritic': 1170, 'macerate': 1171, 'sweaty': 1172, 'hantavirus': 1173, 'pulmonary': 1174, 'loudly': 1175, 'gravidarum': 1176, 'recumbent': 1177, 'position': 1178, 'snort': 1179, 'grunt': 1180, 'bradycardia': 1181, 'cushing': 1182, 'cushingoid': 1183, 'habitus': 1184, 'pure': 1185, 'another': 1186, 'solution': 1187, 'stuffiness': 1188, 'foamy': 1189, 'pleura': 1190, 'digestive': 1191, 'remain': 1192, 'fine': 1193, 'detail': 1194, 'dysfunctional': 1195, 'unconscious': 1196, 'ulcer': 1197, 'metabolic': 1198, 'metabolism': 1199, 'acid': 1200, 'articulate': 1201, 'ready': 1202, 'asleep': 1203, 'acne': 1204, 'fell': 1205, 'anomic': 1206, 'hydrops': 1207, 'fetalis': 1208, 'enzyme': 1209, 'transaminase': 1210, 'pooping': 1211, 'eliminate': 1212, 'caliber': 1213, 'warmth': 1214, 'kiidney': 1215, 'shingle': 1216, 'present': 1217, 'extra': 1218, 'marital': 1219, 'orthopnea': 1220, 'physcial': 1221, 'vascular': 1222, 'blindness': 1223, 'agraphia': 1224, 'constipation': 1225, 'fingernail': 1226, 'grey': 1227, 'monocyte': 1228, 'bacterial': 1229, 'asprin': 1230, 'nostril': 1231, 'widen': 1232, 'vibratory': 1233, 'felt': 1234, 'palpation': 1235, 'wrist': 1236, 'extend': 1237, 'cerebellar': 1238, 'artery': 1239, 'creates': 1240, 'attitude': 1241, 'sniff': 1242, 'slightly': 1243, 'rale': 1244, 'cry': 1245, 'involuntarily': 1246, 'panic': 1247, 'hoarseness': 1248, 'laugh': 1249, 'acetaminophen': 1250, 'read': 1251, 'harm': 1252, 'tetraplegia': 1253, 'faintness': 1254, 'close': 1255, 'heighten': 1256, 'reason': 1257, 'fart': 1258, 'burst': 1259, 'manner': 1260, 'part': 1261, 'noticeable': 1262, 'insufficiency': 1263, 'temporary': 1264, 'emotional': 1265, 'expression': 1266, 'intense': 1267, 'abort': 1268, 'binging': 1269, 'neve': 1270, 'fiber': 1271, 'subconjunctival': 1272, 'impulsiveness': 1273, 'irritable': 1274, 'splenomegaly': 1275, 'communicate': 1276, 'correctly': 1277, 'pyrexia': 1278, 'developmental': 1279, 'ability': 1280, 'pumped': 1281, 'beating': 1282, 'anxiousness': 1283, 'retardedness': 1284, 'dumbness': 1285, 'genitals': 1286, 'cant': 1287, 'focus': 1288, 'lift': 1289, 'floor': 1290, 'obey': 1291, 'prickle': 1292, 'apyrexial': 1293, 'extramarital': 1294, 'give': 1295, 'quickly': 1296, 'trance': 1297, 'accompany': 1298, 'atypical': 1299, 'adequate': 1300, 'fecal': 1301, 'ocult': 1302, 'onone': 1303, 'talk': 1304, 'woozy': 1305, 'sac': 1306, 'transsexual': 1307, 'happiness': 1308, 'moisture': 1309, 'anxious': 1310, 'negative': 1311, 'constantly': 1312, 'sciatic': 1313, 'think': 1314, 'charley': 1315, 'horse': 1316, 'breathe': 1317, 'restless': 1318, 'fidgety': 1319, 'different': 1320, 'immunoglobulin': 1321, 'needle': 1322, 'ground': 1323, 'ocular': 1324, 'incurable': 1325, 'constriction': 1326, 'pale': 1327, 'colour': 1328, 'heal': 1329, 'bony': 1330, 'interest': 1331, 'fatigability': 1332, 'name': 1333, 'toenail': 1334, 'wild': 1335, 'compensation': 1336, 'breakable': 1337, 'hyperventilation': 1338, 'enthusiasm': 1339, 'wooziness': 1340, 'task': 1341, 'slowly': 1342, 'slowness': 1343, 'malfunction': 1344, 'blacking': 1345, 'frustrate': 1346, 'passageway': 1347, 'whiten': 1348, 'coronary': 1349, 'become': 1350, 'turn': 1351, 'dangerously': 1352, 'soreness': 1353, 'hungry': 1354, 'hotness': 1355, 'ambidextrous': 1356, 'struggle': 1357, 'insect': 1358, 'crawl': 1359, 'meat': 1360, 'discloured': 1361, 'poop': 1362, 'loud': 1363, 'blockage': 1364, 'emergency': 1365, 'thirsty': 1366, 'tummy': 1367, 'weird': 1368, 'dull': 1369, 'tight': 1370, 'enough': 1371, 'comply': 1372, 'acidic': 1373, 'bloat': 1374, 'able': 1375, 'coordinate': 1376, 'ischemia': 1377, 'badly': 1378, 'organize': 1379, 'paralyze': 1380, 'complete': 1381, 'obstruction': 1382, 'conjunctival': 1383, 'home': 1384, 'occurs': 1385, 'exertion': 1386, 'great': 1387, 'uncomfortable': 1388, 'despair': 1389, 'mumble': 1390, 'intellectual': 1391, 'pant': 1392, 'drowsy': 1393, 'incident': 1394, 'far': 1395, 'diminish': 1396, '15': 1397, 'angry': 1398, 'excessively': 1399, 'visible': 1400, 'unsure': 1401, 'collect': 1402, 'forceful': 1403, 'exhalation': 1404, 'pooing': 1405, '16': 1406, 'teeth': 1407, 'formation': 1408, 'prematurely': 1409, 'stuck': 1410, 'intercourse': 1411, 'pattern': 1412, 'appointment': 1413, 'refusal': 1414, 'treat': 1415, 'drunk': 1416, 'rhythmic': 1417, 'exhaust': 1418, 'alochol': 1419, 'numb': 1420, 'obese': 1421, '13': 1422, 'wrinkly': 1423, 'muslim': 1424, 'islam': 1425, 'esophagues': 1426, 'elevate': 1427, 'crackle': 1428, 'larynx': 1429, 'fistula': 1430, 'dura': 1431, 'skull': 1432, 'base': 1433, 'stomch': 1434, 'cream': 1435, 'heard': 1436, 'noise': 1437, 'inablity': 1438, 'homeless': 1439, 'articule': 1440, 'worried': 1441, 'breathless': 1442, 'adult': 1443, 'inner': 1444, 'run': 1445, 'burn': 1446, 'speask': 1447, 'recall': 1448, 'respond': 1449, 'ask': 1450, 'collection': 1451, 'jaw': 1452, 'differs': 1453, 'disability': 1454, 'prevents': 1455, 'dischromic': 1456, 'vaginal': 1457, 'stair': 1458, 'weigh': 1459, 'must': 1460, 'sens': 1461, 'remember': 1462, 'whoosh': 1463, 'swish': 1464, '11': 1465, 'distract': 1466, 'infrequent': 1467, 'form': 1468, 'taks': 1469, '12': 1470, 'smoker': 1471, 'process': 1472, 'information': 1473, 'handedness': 1474, 'unnatural': 1475, 'detect': 1476, 'parkinson': 1477, 'cicatrise': 1478, 'hypertransaminasemia': 1479, 'casuses': 1480, 'impairs': 1481, 'behaviour': 1482, 'agitate': 1483, '14': 1484, 'acquire': 1485, 'indueced': 1486, 'unusual': 1487, 'timing': 1488}



symptom_list = ['Aging, Premature', 'Agnosia', 'Agraphia', 'Akathisia',
       'Akathisia, Drug-Induced', 'Alexia, Pure', 'Alien Hand Syndrome',
       'Amnesia', 'Amnesia, Anterograde', 'Amnesia, Retrograde',
       'Amnesia, Transient Global', 'Anisocoria', 'Anomia', 'Aphasia',
       'Aphasia, Broca', 'Aphasia, Conduction',
       'Aphasia, Primary Progressive', 'Aphasia, Wernicke',
       'Apraxia, Ideomotor', 'Apraxias', 'Articulation Disorders',
       'Asthenia', 'Ataxia', 'Athetosis', 'Auditory Perceptual Disorders',
       'Birth Weight', 'Body Weight', 'Body Weight Changes',
       'Brown-Sequard Syndrome', 'Cachexia', 'Cardiac Output, High',
       'Cardiac Output, Low', 'Case/control', 'Catalepsy', 'Catatonia',
       'Cerebellar Ataxia', 'Cerebrospinal Fluid Otorrhea',
       'Cerebrospinal Fluid Rhinorrhea', 'Chills', 'Chorea', 'Coma',
       'Communication Disorders', 'Confusion', 'Consciousness Disorders',
       'Consult nearest hospital', 'Cough', 'Cyanosis',
       'Decerebrate State', 'Delirium', 'Diarrhea', 'Drug effect',
       'Drug side effect', 'Drug-Induced', 'Dysarthria', 'Dyskinesias',
       'Dyslexia', 'Dystonia', 'Echolalia', 'Edema', 'Edema, Cardiac',
       'Emaciation', 'Eye Hemorrhage', 'Eye Manifestations', 'Eye Pain',
       'Facial Pain', 'Facial Paralysis', 'Fasciculation', 'Fatigue',
       'Feminization', 'Fetal Distress', 'Fetal Macrosomia', 'Fever',
       'Fever of Unknown Origin', 'Flushing', 'Gait Apraxia',
       'Gait Ataxia', 'Gait Disorders, Neurologic', 'Gastroparesis',
       'Gerstmann Syndrome', 'Hallucinations', 'Headache',
       'Heart Murmurs', "Heberden's node", 'Hemifacial Spasm',
       'Hemiplegia', 'Horner Syndrome', 'Hot Flashes', 'Hydrops Fetalis',
       'Hypergammaglobulinemia', 'Hyperkinesis', 'Hypokinesia',
       'Hypothermia', 'Idiopathic', 'Illusions',
       'Infantile Apparent Life-Threatening Event',
       'Intermittent Claudication', 'Korsakoff Syndrome', 'Labor Pain',
       'Language Development Disorders', 'Language Disorders',
       'Learning Disorders', 'Lethargy', 'Low Back Pain',
       'Memory Disorders', 'Meningism', 'Mental Fatigue',
       'Mental Retardation', 'Metatarsalgia', 'Miosis',
       'Mobility Limitation', 'Morbid', 'Motion Sickness',
       "Murphy's sign", 'Muscle Cramp', 'Muscle Hypertonia',
       'Muscle Hypotonia', 'Muscle Rigidity', 'Muscle Spasticity',
       'Muscle Weakness', 'Muscular Atrophy', 'Mutism', 'Myoclonus',
       'Myokymia', 'Myotonia', 'Nausea', 'Neck Pain', 'Neuralgia',
       'Neuralgia, Postherpetic', 'Neurobehavioral Manifestations',
       'Neurologic Manifestations', 'Obesity', 'Obesity, Morbid',
       'Ophthalmoplegia', 'Ophthalmoplegia, Chronic Progressive External',
       'Orthostatic Intolerance', 'Overweight', 'Pain',
       'Pain, Intractable', 'Pain, Referred', 'Paralysis', 'Paraparesis',
       'Paraparesis, Spastic', 'Paraplegia', 'Paresis',
       'Perceptual Disorders', 'Persistent Vegetative State',
       'Phantom Limb', 'Piriformis Muscle Syndrome',
       'Primary Progressive Nonfluent Aphasia', 'Prosopagnosia',
       'Proteinuria', 'Pseudobulbar Palsy', 'Psychomotor Agitation',
       'Psychomotor Disorders', 'Psychophysiologic Disorders',
       'Pupil Disorders', 'Purpura', 'Quadriplegia', 'Reflex, Abnormal',
       'Reflex, Babinski', 'Respiratory Paralysis', 'Sarcopenia',
       'Sciatica', 'Sleep Deprivation', 'Sleep Disorders',
       'Slit Ventricle Syndrome', 'Space Motion Sickness', 'Spasm',
       'Speech Disorders', "Stahli's line", 'Stupor', 'Stuttering',
       'Supranuclear Palsy, Progressive', 'Susac Syndrome',
       'Sweating Sickness', 'Syncope', 'Syncope, Vasovagal', 'Synkinesis',
       'Systolic Murmurs', 'Tetany', 'Thinness', 'Thrombocytopenic',
       'Tics', 'Tonic Pupil', 'Torticollis', 'Tremor', 'Trismus',
       'Unconsciousness', 'Vision Disorders', 'Vocal Cord Paralysis',
       'Vomiting', 'Weight Gain', 'abdomen acute', 'abdominal bloating',
       'abdominal tenderness', 'abdominal_pain', 'abnormal sensation',
       'abnormal_menstruation', 'abnormally hard consistency', 'abortion',
       'abscess bacterial', 'absences finding', 'acetaminophen',
       'achalasia', 'ache', 'acidity', 'acute_liver_failure',
       'adverse effect', 'agitation', 'air fluid level',
       'alcohol binge episode', 'alcoholic withdrawal symptoms',
       'altered_sensorium', 'ambidexterity', 'angina pectoris',
       'anorexia', 'anosmia', 'anti itch medicine', 'antiboitic therapy',
       'anxiety', 'aphagia', 'apply calamine', 'apyrexial', 'arthralgia',
       'ascites', 'asterixis', 'asymptomatic', 'atypia', 'aura',
       'avoid abrupt head movment', 'avoid cold food',
       'avoid fatty spicy food', 'avoid lying down after eating',
       'avoid non veg food', 'avoid oily food', 'avoid open cuts',
       'avoid public places', 'avoid sudden change in body',
       'avoid too many products', 'awakening early', 'back pain',
       'barking cough', 'bath twice', 'bedridden', 'behavior hyperactive',
       'behavior showing increased motor activity', 'belly_pain',
       'blackheads', 'blackout', 'bladder_discomfort', 'blanch',
       'bleeding of vagina', 'blister', 'blood_in_sputum', 'bloody_stool',
       'blurred_and_distorted_vision', 'bowel sounds decreased',
       'bradycardia', 'bradykinesia', 'breakthrough pain',
       'breath sounds decreased', 'breath-holding spell',
       'breathlessness', 'breech presentation', 'brittle_nails',
       'bruising', 'bruit', 'burning sensation', 'burning_micturition',
       'call ambulance', 'cardiomegaly', 'cardiovascular event',
       'catching breath', 'charleyhorse', 'check in pulse',
       'chest discomfort', 'chest tightness', 'chest_pain',
       'chew or swallow asprin', 'choke', 'cicatrisation', 'clammy skin',
       'claudication', 'clonus', 'clumsiness', 'cold baths',
       'cold_hands_and_feets', 'colic abdominal', 'congestion',
       'consciousness clear', 'constipation', 'consult doctor',
       'consume alovera juice', 'consume milk thistle',
       'consume neem leaves', 'consume probiotic food',
       'consume witch hazel', 'continuous_feel_of_urine',
       'continuous_sneezing', 'coordination abnormal',
       'cover area with bandage', 'cover mouth', 'cushingoid habitus',
       'cystic lesion', 'dark_urine', 'debilitation', 'decompensation',
       'decreased stool caliber', 'decreased translucency', 'dehydration',
       'depression', 'difficulty passing urine', 'dischromic _patches',
       'disequilibrium', 'distended abdomen', 'distress respiratory',
       'disturbed family', 'dizziness', 'dizzy spells',
       'dont stand still for long', 'drink cranberry juice',
       'drink papaya leaf juice', 'drink plenty of water',
       'drink sugary drinks', 'drink vitamin c rich drinks', 'drool',
       'drowsiness', 'drying_and_tingling_lips', 'dullness',
       'dysdiadochokinesia', 'dysesthesia', 'dyspareunia', 'dyspnea',
       'dysuria', 'ease back into eating',
       'eat fruits and high fiberous food', 'eat healthy',
       'eat high calorie vegitables', 'ecchymosis', 'egophony', 'elation',
       'eliminate milk', 'emphysematous change', 'energy increased',
       'enlarged_thyroid', 'enuresis', 'erythema', 'estrogen use',
       'excessive_hunger', 'excruciating pain', 'exercise', 'exhaustion',
       'extra_marital_contacts', 'extrapyramidal sign', 'facial paresis',
       'fall', 'family_history', 'fast_heart_rate', 'fear of falling',
       'fecaluria', 'feces in rectum', 'feeling hopeless',
       'feeling strange', 'feeling suicidal', 'feels hot/feverish',
       'flare', 'flatulence', 'floppy', 'fluid_overload',
       'focal seizures', 'follow up', 'food intolerance', 'formication',
       'foul_smell_of urine', 'frail', 'fremitus', 'frothy sputum', 'gag',
       'gasping for breath', 'general discomfort', 'general unsteadiness',
       'get away from trigger', 'get proper sleep', 'giddy mood',
       'gravida 0', 'gravida 10', 'green sputum', 'groggy',
       'guaiac positive', 'gurgle', 'hacking cough', 'haemoptysis',
       'haemorrhage', 'hallucinations auditory', 'hallucinations visual',
       'has religious belief', 'have balanced diet', 'heartburn',
       'heavy feeling', 'heavy legs', 'hematochezia',
       'hematocrit decreased', 'hematuria', 'heme positive',
       'hemianopsia homonymous', 'hemodynamically stable', 'hepatomegaly',
       'hepatosplenomegaly', 'high_fever', 'hip_joint_pain', 'hirsutism',
       'history of - blackout', 'history_of_alcohol_consumption', 'hoard',
       'hoarseness', 'homelessness', 'homicidal thoughts',
       'hydropneumothorax', 'hyperacusis', 'hypercapnia', 'hyperemesis',
       'hyperhidrosis disorder', 'hyperkalemia', 'hypersomnia',
       'hypertonicity', 'hyperventilation', 'hypesthesia',
       'hypoalbuminemia', 'hypocalcemia result', 'hypokalemia',
       'hypometabolism', 'hyponatremia', 'hypoproteinemia', 'hypotension',
       'hypotonic', 'hypoxemia', 'immobile', 'impaired cognition',
       'inappropriate affect', 'incoherent', 'increase vitamin c intake',
       'increased_appetite', 'indifferent mood', 'indigestion',
       'inflammatory_nails', 'intermenstrual heavy bleeding',
       'internal_itching', 'intoxication', 'irregular_sugar_level',
       'irritability', 'irritation_in_anus', 'itching', 'joint_pain',
       'jugular venous distention', 'keep calm', 'keep fever in check',
       'keep hydrated', 'keep infected area dry', 'keep mosquitos away',
       'keep mosquitos out', 'knee_pain', 'labored breathing',
       'lack_of_concentration', 'large-for-dates fetus',
       'left atrial hypertrophy', 'lesion', 'lie down',
       'lie down flat and raise the leg high', 'lie down on side',
       'lightheadedness', 'limit alcohol', 'lip smacking',
       'loose associations', 'loss_of_appetite', 'loss_of_balance',
       'loss_of_smell', 'lung nodule', 'macerated skin', 'macule',
       'maintain healthy weight', 'malaise', 'mass in breast',
       'mass of body structure', 'massage', 'mediastinal shift',
       'meditation', 'mental status changes', 'metastatic lesion',
       'mild_fever', 'milky', 'moan', 'monoclonal', 'monocytosis',
       'mood_swings', 'moody', 'motor retardation', 'movement_stiffness',
       'mucoid_sputum', 'muscle twitch', 'muscle_pain', 'muscle_wasting',
       'myalgia', 'mydriasis', 'nasal discharge present', 'nasal flaring',
       'neck stiffness', 'neologism', 'nervousness', 'night sweat',
       'nightmare', 'no known drug allergies', 'no status change',
       'nodal_skin_eruptions', 'noisy respiration',
       'non-productive cough', 'nonsmoker', 'numbness',
       'numbness of hand', 'oliguria', 'orthopnea', 'orthostasis',
       'out of breath', 'pain foot', 'pain in lower limb',
       'pain_behind_the_eyes', 'pain_during_bowel_movements',
       'pain_in_anal_region', 'painful swallowing', 'painful_walking',
       'pallor', 'palpitation', 'panic', 'pansystolic murmur', 'para 1',
       'para 2', 'paresthesia', 'passage_of_gases', 'passed stones',
       'patches_in_throat', 'patient non compliance',
       'pericardial friction rub', 'phlegm', 'phonophobia', 'photophobia',
       'photopsia', 'pin-point pupils', 'pleuritic pain', 'pneumatouria',
       'polydypsia', 'polymyalgia', 'polyuria', 'poor dentition',
       'poor feeding', 'posterior rhinorrhea', 'posturing',
       'presence of q wave', 'pressure chest', 'previous pregnancies 2',
       'primigravida', 'prodrome', 'productive cough',
       'projectile vomiting', 'prominent_veins_on_calf',
       'prostate tender', 'prostatism', 'proteinemia',
       'puffy_face_and_eyes', 'pulse absent', 'pulsus paradoxus',
       'pus_filled_pimples', 'pustule', 'qt interval prolonged',
       'r wave feature', 'rale', 'rambling speech',
       'rapid shallow breathing', 'receiving_blood_transfusion',
       'receiving_unsterile_injections', 'red blotches',
       'red_sore_around_nose', 'red_spots_over_body', 'redness_of_eyes',
       'reduce stress', 'regurgitates after swallowing',
       'remove scabs with wet compressed cloth', 'renal angle tenderness',
       'rest pain', 'restlessness', 'retch', 'retropulsion',
       'rhd positive', 'rhonchus',
       'rigor - temperature-associated observation', 'rolling of eyes',
       'room spinning', 'rusty_sputum', 'salt baths', 'satiety early',
       'scar tissue', 'scleral icterus', 'scratch marks', 'scurring',
       'sedentary', 'seek help', 'seizure', 'sensory discomfort',
       'shivering', 'shooting pain', 'shortness of breath', 'side pain',
       'silver_like_dusting', 'sinus rhythm', 'sinus_pressure',
       'skin_peeling', 'skin_rash', 'sleeplessness', 'sleepy',
       'slowing of urinary stream', 'slurred_speech',
       'small_dents_in_nails', 'sneeze', 'sniffle', 'snore', 'snuffle',
       'soak affected area in warm water', 'soft tissue swelling',
       'sore to touch', 'spinning_movements', 'splenomegaly',
       'spontaneous rupture of membranes', 'spotting_ urination',
       'sputum purulent', 'st segment depression', 'st segment elevation',
       'stiff_neck', 'stiffness', 'stinging sensation',
       'stomach_bleeding', 'stomach_pain', 'stool color yellow',
       'stop alcohol consumption', 'stop bleeding using pressure',
       'stop eating solid food for while', 'stop irritation',
       'stop taking drug', 'stridor', 'stuffy nose', 'suicidal',
       'sunken_eyes', 'superimposition', 'sweating', 'sweating increased',
       'swelled_lymph_nodes', 'swelling', 'swelling_joints',
       'swelling_of_stomach', 'switch to loose cloothing',
       'swollen_blood_vessels', 'swollen_extremeties', 'swollen_legs',
       'symptom aggravating factors', 'systolic ejection murmur',
       't wave inverted', 'tachypnea', 'take deep breaths',
       'take otc pain reliver', 'take probiotics',
       'take radioactive iodine treatment', 'take vaccine', 'take vapour',
       'tenesmus', 'terrify', 'thicken', 'throat sore',
       'throbbing sensation quality', 'tinnitus', 'tired', 'titubation',
       'todd paralysis', 'tonic seizures', 'toxic_look_(typhos)',
       'transaminitis', 'transsexual', 'tremor resting',
       'try acupuncture', 'try taking small sips of water',
       'tumor cell invasion', 'ulcers_on_tongue', 'unable to concentrate',
       'uncoordination', 'underweight', 'unhappy', 'unresponsiveness',
       'unsteadiness', 'unsteady gait', 'unwell', 'urge incontinence',
       'urgency of micturition', 'urinary hesitation', 'urinoma',
       'use antibiotics', 'use clean cloths',
       'use detol or neem in bathing water',
       'use heating pad or cold pack', 'use hot and cold therapy',
       'use ice to compress itching', 'use lemon balm',
       'use neem in bathing', 'use oinments',
       'use poloroid glasses in sun', 'use vein compression',
       'vaccination', 'verbal auditory hallucinations',
       'verbally abusive behavior', 'vertigo', 'vision blurred',
       'visual_disturbances', 'warm bath with epsom salt',
       'wash hands through', 'wash hands with warm soapy water',
       'watering_from_eyes', 'weakness_in_limbs',
       'weakness_of_one_body_side', 'wear ppe if possible', 'weepiness',
       'weight loss', 'welt', 'wheelchair bound', 'wheezing', 'withdraw',
       'worry', 'yellow sputum', 'yellow_crust_ooze', 'yellow_urine',
       'yellowing_of_eyes', 'yellowish_skin']
#needs to stay alphabetical

def get_symptoms(inputted):
    #parsed = [] 
    good = []
    #final_symptoms = []
    #encoded = []
    #seq = []

    #parsed.clear()
    good.clear()
    #final.clear()
    #encoded.clear()
    #seq.clear()

    good = clean (inputted)
    print(predict(good))
    return (predict(good))
    
#cleans up the text 
def clean (text):
    tempgood = []
    lemmatizer = WordNetLemmatizer() 
    text = text.replace('.', '   ') #replaces periods with triple space
    text = re.sub(r'\s\s+', '  ', text) #removes extra spaces and replaces with double space'
    text = text.lower()
    text = re.sub('[^A-Za-z0-9 ]+', '', text) #removes special characters; #remove space after
    #print ("text is \n" + text)

    parsed = text.split('  ')
    print("parsed: ")
    print(parsed)
    temp = []
    temp2=""
    for x in parsed:
        temp = x.split()
        for y in temp:
            y = lemmatizer.lemmatize(y, get_wordnet_pos(y) )        # will keep sentences together; will separate \n entered symptoms
            if(y not in stopwords.words('english')):
                temp2 = temp2+" "+y
        if(temp2 != ""):
            temp2 = temp2.strip()
            tempgood.append(temp2)
            temp2 = ""
        #print(x)
    return tempgood

#lemmatizer
def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

#takes input as \n separated  - lots of whitespace in between symptoms
#or takes input as paragraph form; 
def predict(good):
    final = []
    final.clear()
    seq = []
    for i in good:
        seq.clear()
        tphrase = i
        print(tphrase)
        tphrase = tphrase.split()
        temp = review_encode(tphrase)
        seq.append(temp)
        print (seq)
        padded = pad_sequences(seq, maxlen=10, padding='post', truncating='post')
       # print(padded)
        pred = NLmodel.predict(padded)
        acc = NLmodel.predict(padded)
        #predicted_label = encode.inverse_transform(pred)
        symptomnum = np.argmax(pred[0])
        #print (symptomnum)
        #print(symptom_list[symptomnum])
        #print(f'Accuracy score: { acc.max() * 100}')
        if(acc.max()*100 > 60):
            final.append(symptom_list[symptomnum])

    have = ["Asthenia", "Ataxia", "Pain", "chest_pain", "Paresis", "Stupor", "Spasm", "seizure", "Sciatica", "Paraparesis", "Overweight", "Obesity", "Myoclonus", "Low Back Pain", "Lethargy", "Hypokinesia", "Hemiplegia", "Vomiting", "Tremor", "Syncope", "Headache", "Flushing", "Fever", "Dysarthria", "Cyanosis", "Cough", "Consult nearest hospital", "Coma", "Catatonia", "Cachexia", "Muscle Cramp", "Weight_loss",  "distended abdomen", "Dyslexia", "dyspnea", "exhaustion", "Birth Weight", "Hot Flashes", "excessive_hunger", "hypersonmia", "Hypothermia", "irritability", "Depressed", "Muscle Weakness", "abdominal_pain", "palpitation", "Paralysis", "itching", "nasal discharge present", "Systolic murmurs", "slurred_speech", "throat sore", "Unconsciousness", "weight loss"]

    add = ["asthenia", "ataxia", "pain", "pain chest", "paresis", "stupor", "spasm", "seizure", "sciatica", "paraparesis", "overweight", "obesity", "myoclonus", "low back pain", "lethargy", "hypokinesia", "hemiplegia", "vomiting", "tremor", "syncope", "headache", "flushing", "fever", "dysarthria", "cyanosis", "cough", "consult nearest hospital", "coma", "catatonia", "cachexia", "cramps", "decreased body weight",  "distention_of_abdomen", "Dyslexia, Acquired", "dyspnea on exertion", "extreme exhaustion", "Fetal Weight", "hot flush", "hunger", "hypersomnolence", "hypothermia, natural", "irritable", "mood depressed", "muscle_weakness", "pain abdominal", "palpitations", "paralyse", "pruritus", "runny_nose", "systolic murmur", "speech slurred", "throat_irritation", "unconscious state", "weight loss"]


    for every1 in range(len(final)):
        for every2 in range(len(have)):
            if final[every1] == have[every2]:
                final.append(add[every2])
                #print("replaced!")

    for every3 in final:
        #print(every3)
        if every3 == "back pain":
            final.append("Pain back")
            final.append("Back_pain")
            #print("replaced1")
        elif every3 == "Fatigue":
            final.append("fatigue")
            final.append("fatgability")
        elif every3 == "Weight Gain":
            final.append("weight gain")
            final.append("weight_gain")
        elif every3 == "Diarrhea":
            final.append("diarrhea")
            final.append("diarrhoea")
        
    return final

def review_encode(s):  
    encoded = []
    encoded.clear()
    for word in s: 
        if word in word_index:
            encoded.append(word_index[word])
    return encoded





# get_symptoms("John has a history of drinking too much alochol. He has anterograde amnesia. He also came in with a very high temperature. Barking cough as well. Very tired and fatigued. Red swollen mark on skin too. Coughing up blood. John has back pain. John has a sore throat")

get_symptoms("john was pain abdominal.	 having pain. it was weight hyperventilation. sadly excruciating pain.	gag.	really bad nausea posturing.	he needed less hemiplegia. he was sore to touch.	haemorrhage.  bad apyrexial. severe food intolerance. maybe	pulse absent. possibly asthenia. mass of body structure thicken")

