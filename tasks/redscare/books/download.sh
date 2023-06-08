#!/usr/bin/env bash
set -e

for part in {01..55}; do
	wget "https://leninism.su/images/PSS/FB2/t-$part.zip"
	unzip "t-$part.zip"
	rm "t-$part.zip"
done
