out=egs/Marathidataset/tr
noisy=/ssd_scratch/cvit/aparna/VGGSound/VGGSound
clean=/ssd_scratch/cvit/aparna/NLTM_Speech/surabhi/train_data/kb_data_clean_m4a/marathi/train/audio
mkdir -p $out
python -m denoiser.audio $noisy > $out/noisy.json
python -m denoiser.audio $clean > $out/clean.json
