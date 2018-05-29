#!/bin/bash

echo "Welcome!"
echo "This script will run commands to install the packages necessary to run Harmonizer"
while true; do
	read -p "Do you want to run the script? [y/n] : " answer
	case $answer in
		[Yy]* ) 
			echo "Starting..." 
			break
			;;
		[Nn]* ) 
			exit
			;;
		* ) 
			echo "Please answer yes or no"
			;;
	esac
done
echo "Updating system..."
sudo apt update
sudo apt-get update

echo "Installing PIP..."
sudo apt install python3-pip
pip3 --version

echo "Installing Numpy..."
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

echo "Installing appJar..."
sudo pip3 install appjar

echo "Installing packages for pyautogui..."
pip3 install python3-xlib
sudo apt-get install scrot
sudo apt-get install python3-tk
sudo apt-get install python3-dev

echo "Installing pyautogui..."
pip3 install pyautogui

echo "Installing display theme tool..."
pip3 install ttkthemes

echo "Installation done."
while true; do
	read -p "Run Harmonizer? [y/n] " run
	case $run in
		[Yy]* ) 
			echo "Launching Harmonizer" 
			python3 gui.py &> /dev/null & 
			break
			;;
		[Nn]* ) 
			exit
			;;
		* ) 
			echo "Please answer yes or no"
			;;
	esac
done