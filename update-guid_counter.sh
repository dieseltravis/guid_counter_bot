#/bin/sh

INFO='\e[38;05;14m'
NC='\033[0m' # No Color

# Status:
sudo systemctl status guid_counter && ps -eo pid,vsz,rss,comm | grep -i python3 && free -m

echo "Shutting down guid_counter..."
echo -e "${INFO}systemctl stop guid_counter${NC}";
sudo systemctl stop guid_counter
echo "Updating guid_counter..."
echo -e "${INFO}git fetch${NC}";
sudo git fetch
echo -e "${INFO}git pull${NC}";
sudo git pull
echo "Starting up guid_counter..."
echo -e "${INFO}systemctl start guid_counter${NC}";
sudo systemctl start guid_counter

sudo systemctl status guid_counter && ps -eo pid,vsz,rss,comm | grep -i python3 && free -m