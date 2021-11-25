import librosa
import re

import numpy as np
import pympi.Elan as Elan
import soundfile as sf

from argparse import ArgumentParser
from glob import glob
from os import path

parser = ArgumentParser(
    prog='ELAN eaf tier extractor for individual wav files',
    description='Extract relevant tier from an eaf file into individual eaf files',
)

parser.add_argument('input_Sx_dir', help = "directory with S-suffixed wav files, e.g. 'NSY-20191105-C_S1.wav', assuming NSY-20191105-C.eaf exists in same directory.")
args = parser.parse_args()

Sx_files = glob(args.input_Sx_dir + '/*_S*.wav')

assert len(Sx_files) > 0, "No relevant wav files ending with _Sx found in directory {}".format(args.input_Sx_dir)

for input_sX_wav in Sx_files:

    assert re.search(r"S[1-3]\.(wav|WAV)$", input_sX_wav), "Filename {} does not end in S1, S2, or S3".format(input_sX_wav)

    eaf_file = re.sub(r"_S[1-3]\.(wav|WAV)$", ".eaf", input_sX_wav)

    assert path.exists(eaf_file), "Could not find expected ELAN file at {}".format(eaf_file)

    print(f'Processing {input_sX_wav}')

    wav_values, sample_rate = sf.read(input_sX_wav, dtype=np.float32)
    wav_values = wav_values.T # Transpose soundfile array for librosa

    hop_length = 256
    frame_length = 512

    rms_values = librosa.feature.rms(wav_values, frame_length=frame_length, hop_length=hop_length, center=True)
    rms_values = rms_values[0]

    rms_times  = librosa.frames_to_time(range(len(rms_values)), sr=sample_rate, hop_length=hop_length)

    eaf_data   = Elan.Eaf(eaf_file)
    tier_names = eaf_data.get_tier_names()

    tiers_of_interest = [ t for t in tier_names if 'Transcription-txt-nsy' in t ]
    mean_rms_on_tier  = []

    for toi in tiers_of_interest:
        annots = eaf_data.get_annotation_data_for_tier(toi)

        annots = np.array([ np.where((rms_times >= start/1000) & (rms_times <= end/1000)) for (start, end, text) in annots ], dtype=object)
        annots = np.ndarray.flatten(annots)
        annots = np.concatenate(annots).ravel()

        mean_rms_on_tier.append(np.mean(rms_values[annots]))

    tier_to_extract = tiers_of_interest[ np.argmax(mean_rms_on_tier) ]

    extracted_tier  = eaf_data
    extracted_tier.remove_tiers([ t for t in tier_names if t != tier_to_extract ])

    new_file = re.sub(r"\.(wav|WAV)$", ".eaf", input_sX_wav)

    extracted_tier.to_file(new_file)
