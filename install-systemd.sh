#/bin/sh

INFO='\e[38;05;14m'
NC='\033[0m' # No Color

echo "Installing python requirements..."
echo -e "${INFO}pip install -r requirements.txt${NC}";
pip install -r requirements.txt
echo "Setting ownership..."
echo -e "${INFO}chown pi:pi ~/guid_counter_bot/*.*${NC}";
sudo chown pi:pi ~/guid_counter_bot/*.*
echo "Installing systemd service..."
echo -e "${INFO}cp ~/guid_counter_bot/guid_counter.service /lib/systemd/system/${NC}";
sudo cp ~/guid_counter_bot/guid_counter.service /lib/systemd/system/
echo -e "${INFO}systemctl enable guid_counter${NC}";
sudo systemctl enable guid_counter
echo -e "${INFO}systemctl daemon-reload${NC}";
sudo systemctl daemon-reload
echo -e "${INFO}systemctl start guid_counter${NC}";
sudo systemctl start guid_counter
echo -e "${INFO}systemctl status guid_counter${NC}";
sudo systemctl status guid_counter
