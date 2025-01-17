# RDS collect 2

## Description

Masther thesis in Computer Science at Karlstad University, that is an continuation of an previous work (C-Sand/rds-collect). It contains tools to collect data sets of captured VPN traffic over streaming websites. Includes scripts, configs and container files used.

## Installation
SAME AS RDS COLLECT 1

```
sudo apt update

sudo apt install git
sudo apt install podman
sudo apt install tmux
sudo apt install wireshark-cli

mkdir projectWorkingDirectory
cd projectWorkingDirectory
git clone ourRepository.com

podman pull containerImage
```

## Usage

setup mullvad configs

setup cronjobs for planned capture

```
./capture.sh
```

## Support
In the following email can one get in touch with me if one has questions about the software

rds-collect.wonderingly@8alias.com


## Authors and acknowledgment

The author of this fork is Gustav Rehnholm, But it is only an adaptation of the original code that this is forked from, developed by Christoffer Sandquist and Jon-Erik Ersson.


## License
TODO

# Docs
TODO?

## Some commands to remember

Podman

```
sudo podman build -t --rm name debian_collect
podman run -it -d --rm --privileged --mount type=bind,src=debian_collect/configFiles,target=/etc/wireguard --entrypoint etc/wireguard/startup.sh debian_collect
sudo podman stop -a
sudo podman prune -a
```

Running tshark with fifo pipe which keeps down RAM usage. Might have effect on captures if system is slow since first tshark instance won't write to the pipe unless the second tshark consumes pcaps fast enough. Replace network-interface and outfile.log. Might want to remove pipe afterwards.

```
mkfifo myfifo
tshark -i <network-interface> -l -w myfifo 2>/dev/null & tshark -r myfifo -l -T fields -e frame.time_relative -e ip.addr -e udp.length >> <outfile.log> 2>/dev/null
```

Here is how timeout is used in the script to assign time for how long the capture should run.

```
timeout $capture_time bash -k -c "tshark -i ${network_interfaces[i]} -l -T fields -e frame.time_relative -e ip.addr -e udp.length >>$outFile 2>/dev/null" &
```

Example of how to run the full command. Runs for 20 seconds on network-interface enp6s0 and saves to the file tshark_test.log

```
timeout 20s bash -k -c "tshark -i enp6s0 -l -w myfifo 2>/dev/null & tshark -r myfifo -l -T fields -e frame.time_relative -e ip.addr -e udp.length >> tshark_test.log 2>/dev/null" &
```

Running df-fitness default with training

```
./df-fitness.py -d parsedFiles/ --train
```

If we want to use raw files from the web-traffic dataset (crossFiles). For example when only using the noise data for testing and validation sets.

```
rsync -a crossFiles/ parsedFiles/ --ignore-existing
```

While inside the parsedFiles folder! Removes png files.

```
find . -maxdepth 2 -name '\*.png' -delete
```

Zip parsedFiles

```
zip -r parsedFiles parsedFiles
```

Produce txt file with all capture files used

```
ll -1 filesToParse > captures.txt
```

List the number of uniques streams captured from.

```
ls -1 filesToParse | awk -F '_' '{print $3}' | sort | uniq | wc -l
```
