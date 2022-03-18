#!/bin/bash

BETTERCAP_DIR=/usr/share/bettercap
HANDSHAKE_DIR=/opt/NS-handshake
APACHE2_DIR=/etc/apache2
WEB_SERVER_DIR=/var/www/html

# Install Python libraries (stored in requirements.txt)

# Installation
echo "Installing xterm"
apt -qq install -y xterm
echo -e "\n\nInstalling bettercap"
apt -qq install -y bettercap
echo -e "\n"
  
# Setup Apache2 rewrite engine mod
if test -d "$APACHE2_DIR" && test -d "$WEB_SERVER_DIR"; then
  cp /etc/apache2/mods-available/rewrite.load /etc/apache2/mods-enabled
else
  echo "$APACHE2_DIR or $WEB_SERVER_DIR don't exist, please use the default Kali configuration."
fi

# Setup Bettercap custom scripts
if test -d "$BETTERCAP_DIR"; then
  echo -n "$BETTERCAP_DIR exists. Install customized scripts and replace the original one to downgrade HTTPS traffic to HTTP? [y/n]: "
  read -n 1 ans
  if [[ $ans == "y" ]]; then
    # install bettercap custom scripts and replace the original one here
    echo -e "\nInstalling custom scripts..." 
    git clone https://github.com/XingSc29/hstshijack.git
    rm -r "$BETTERCAP_DIR/caplets/hstshijack"
    mv "hstshijack" "$BETTERCAP_DIR/caplets/"
  else
    echo -e "\nCustomized scripts are not installed, the sslstrip function in NS-Toolbox may not work correctly!"
  fi
else
  echo "$BETTERCAP_DIR doesn't exist. Unable to continue, exiting..."
  exit 1
fi

# Setup Handshake directory for WPA/WPA2 Handshake Snooper
if test -d "$HANDSHAKE_DIR"; then
  echo
  echo -n "$HANDSHAKE_DIR exists. Delete and recreate a new one? [y/n]: "
  read -n 1 ans
  if [[ $ans == "y" ]]; then
    rm -r "$HANDSHAKE_DIR"
    echo -e "\n$HANDSHAKE_DIR created."
    mkdir "$HANDSHAKE_DIR"
  fi
else
  mkdir "$HANDSHAKE_DIR"
  echo -e "\n$HANDSHAKE_DIR created."
fi
