# sed -i -e "s/'/@TEMP@/g; s/\"/'/g; s/@TEMP@/\"/g" ../data/australian_user_reviews.json
sed -i -e 's/True/true/g' -e 's/False/false/g' ../data/australian_user_reviews.json 