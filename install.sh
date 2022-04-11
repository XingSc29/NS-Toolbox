#!/bin/bash

BETTERCAP_DIR=/usr/share/bettercap
HANDSHAKE_DIR=/opt/NS-Handshake
APACHE2_DIR=/etc/apache2
WEB_SERVER_DIR=/var/www/html

# Install Python libraries (stored in requirements.txt)

# Installation
echo "[+] Installing xterm"
apt install -y xterm
echo -e "\n[+] Installing bettercap"
apt install -y bettercap
echo -e "\n[+] Installing hostapd"
apt install -y hostapd
echo
  
# Setup Apache2 rewrite engine mod
if test -d "$APACHE2_DIR" && test -d "$WEB_SERVER_DIR"; then
  echo "[+] Enabling rewrite engine mod in apache2 server..." 
  cp /etc/apache2/mods-available/rewrite.load /etc/apache2/mods-enabled
else
  echo "[-] $APACHE2_DIR or $WEB_SERVER_DIR don't exist, please use the default Kali configuration."
  exit 1
fi

# Setup Bettercap custom scripts
if test -d "$BETTERCAP_DIR"; then
  echo -e "\n[+] Installing custom scripts..." 
  git clone https://github.com/XingSc29/hstshijack.git
  rm -r "$BETTERCAP_DIR/caplets/hstshijack"
  mv "hstshijack" "$BETTERCAP_DIR/caplets/"
else
  echo -e "\n[-] $BETTERCAP_DIR doesn't exist. Unable to continue, exiting..."
  exit 1
fi

# Setup Handshake directory for WPA/WPA2 Handshake Snooper
if test -d "$HANDSHAKE_DIR"; then
  echo
  echo -n "[+] $HANDSHAKE_DIR exists. Delete and recreate a new one? (Please backup $HANDSHAKE_DIR first if needed!) [y/n]: "
  read -n 1 ans
  if [[ $ans == "y" ]]; then
    rm -r "$HANDSHAKE_DIR"
    echo -e "\n[+] $HANDSHAKE_DIR created."
    mkdir "$HANDSHAKE_DIR"
  else
    echo 
  fi
else
  mkdir "$HANDSHAKE_DIR"
  echo -e "\n[+] $HANDSHAKE_DIR created."
fi

# Install python libraries and dependencies
echo -e "\n[+] Installing dependencies"
apt-get install -y build-essential python-dev-is-python3 libnetfilter-queue-dev
apt install -y python3-pip
echo -e "\n[+] Completed, please run: pip3 install -r requirements.txt"
