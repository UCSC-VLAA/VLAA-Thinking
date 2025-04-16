

######## PLEASE MODIFY ##########
dataset_root="/abs/path/to/vlaa_thinking_data"
######## PLEASE MODIFY ##########

# images
mkdir -p $dataset_root/images
cd $dataset_root/images
for fname in allava_laion.tar.gz arxivqa.tar.gz chartqa.tar.gz docvqa.tar.gz  clevr_math.tar.gz geoqa170k.tar.gz synthesis.tar.gz vizwiz.tar.gz 
do
    wget -O $dataset_root/images/$fname -c "https://huggingface.co/datasets/UCSC-VLAA/VLAA-Thinking/resolve/main/images/$fname?download=true" &
done
wait

# unzip images
for fname in allava_laion.tar.gz arxivqa.tar.gz  docvqa.tar.gz  clevr_math.tar.gz geoqa170k.tar.gz synthesis.tar.gz vizwiz.tar.gz 
do
    tar -xvzf  $fname  &
done
wait




# coco images
cd $dataset_root/images
mkdir coco && cd coco
wget -O "train2017.zip" -c "http://images.cocodataset.org/zips/train2017.zip" &
wait
unzip train2017.zip

# vg images
cd $dataset_root/images
mkdir vg && cd vg
wget -c "https://cs.stanford.edu/people/rak248/VG_100K_2/images.zip" &
wget -c "https://cs.stanford.edu/people/rak248/VG_100K_2/images2.zip" &
wait
unzip images.zip
unzip images2.zip


# annotation
cd $dataset_root
wget -O "VLAA-Thinking-SFT-126K.json" -c "https://huggingface.co/datasets/UCSC-VLAA/VLAA-Thinking/resolve/main/VLAA-Thinking-SFT-126K.json?download=true"
wget -O "VLAA-Thinking-GRPO-25K.json" -c "https://huggingface.co/datasets/UCSC-VLAA/VLAA-Thinking/resolve/main/VLAA-Thinking-GRPO-25K.json?download=true"


