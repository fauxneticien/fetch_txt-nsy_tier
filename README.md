# Match and extract transcriptions for individual tracks in 'main' ELAN file

Assuming there is a 'main' ELAN file of the form `NSY-20191105-C.eaf` accompanied by three audio files starting with the same name (e.g. `NSY-20191105-C_S1.wav`, `NSY-20191105-C_S2.wav`, `NSY-20191105-C_S3.wav`. In the main ELAN file, there are three tiers named of the form `A_Transcription-txt-nsy`, `B_Transcription-txt-nsy`, and `C_Transcription-txt-nsy`.

For each wav file (S1, S2, S3), this script finds the best matching transcription tier (based on average loudness in transcription intervals defined for the tier) and extracts this single tier into a separate ELAN file, e.g. `NSY-20191105-C_S1.eaf`.

Before:

```
- NSY-20191105-C.eaf
- NSY-20191105-C_S1.wav
- NSY-20191105-C_S2.wav
- NSY-20191105-C_S3.wav
```

After:

```
- NSY-20191105-C.eaf
- NSY-20191105-C_S1.wav
- NSY-20191105-C_S1.eaf
- NSY-20191105-C_S2.wav
- NSY-20191105-C_S2.eaf
- NSY-20191105-C_S3.wav
- NSY-20191105-C_S3.eaf
```

## Usage

### Setup

- Open a command line interface and download the git repository onto your computer:

	```
	git clone https://github.com/fauxneticien/fetch_txt-nsy_tier.git
	cd fetch_txt-nsy_tier
	```
	
- Install the necessary dependencies:

	```
	pip install -t requirements.txt
	```
	
### Usage

- Supply a directory containing S-suffixed wav files (and corresponding main eaf files):

	```python
	python fetch_txt-nsy_tier.py /path/to/dir/with/S-files
	```
