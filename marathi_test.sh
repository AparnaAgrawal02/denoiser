out=egs/Marathidataset/tt
noisy=/ssd_scratch/cvit/aparna/NLTM_Speech/surabhi/noisy_test/kb_data_noisy_m4a/marathi/test_known/audio 
clean=/ssd_scratch/cvit/aparna/NLTM_Speech/surabhi/clean_test/kb_data_clean_m4a/marathi/test_known/audio
mkdir -p $out
python -m denoiser.audio $noisy > $out/noisy.json
python -m denoiser.audio $clean > $out/clean.json

