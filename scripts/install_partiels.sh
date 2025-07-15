#!/bin/bash

# This script installs Partiels and its main plugins. 

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_EXECUTABLE=$(command -v python3 || command -v python)

PARTIELS_URL="https://github.com/Ircam-Partiels/Partiels/releases/download"
PARTIELS_VERSION=$($PYTHON_EXECUTABLE $SCRIPT_DIR/../src/partielspy/version.py)
IRCAM_VAMP_URL="https://github.com/Ircam-Partiels/ircam-vamp-plugins/releases/download"
IRCAM_VAMP_VERSION="2.1.0"
VAX_VAMP_VERSION="1.0.0"
CREPE_VAMP_URL="https://github.com/Ircam-Partiels/crepe-vamp-plugin/releases/download"
CREPE_VAMP_VERSION="3.0.0"
WHISPER_VAMP_URL="https://github.com/Ircam-Partiels/whisper-vamp-plugin/releases/download"
WHISPER_VAMP_VERSION="3.0.0"

while [[ $# -gt 0 ]]; do
    case $1 in
    # Check for --help or -h
        --help | -h)
            echo "Usage: $0 [--partiels_version <version>] [--ircam_vamp_version <version>] [--vax_vamp_version <version>] [--crepe_vamp_version <version>] [--whisper_vamp_version <version>]"
            echo "Default versions will be used if no arguments are provided."
            exit 0
            ;;
        --partiels_version)
            PARTIELS_VERSION="$2"
            shift 2
            ;;
        --ircam_vamp_version)
            IRCAM_VAMP_VERSION="$2"
            shift 2
            ;;
        --vax_vamp_version)
            VAX_VAMP_VERSION="$2"
            shift 2
            ;;
        --crepe_vamp_version)
            CREPE_VAMP_VERSION="$2"
            shift 2
            ;;
        --whisper_vamp_version)
            WHISPER_VAMP_VERSION="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done    

# Check if the script is running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    TEMP_DIR=$(mktemp -d)
    echo -e '\033[0;34m' "Temporary directory created at: $TEMP_DIR"
    echo -e '\033[0m'
    cd "$TEMP_DIR" || exit 1

    echo -e '\033[0;34m' "Downloading Partiels and plugins..."
    echo -e '\033[0m'
    curl -L --show-error --silent -o Partiels-MacOS.dmg $PARTIELS_URL/$PARTIELS_VERSION/Partiels-MacOS.dmg
    curl -L -o Ircam-Vamp-Plugins-MacOS.zip $IRCAM_VAMP_URL/$IRCAM_VAMP_VERSION/Ircam-Vamp-Plugins-MacOS.zip
    curl -L -o VAX-Vamp-Plugin-v$VAX_VAMP_VERSION-MacOS.zip $IRCAM_VAMP_URL/$IRCAM_VAMP_VERSION/VAX-Vamp-Plugin-v$VAX_VAMP_VERSION-MacOS.zip
    curl -L -o Crepe-MacOs.pkg $CREPE_VAMP_URL/$CREPE_VAMP_VERSION/Crepe-MacOs.pkg
    curl -L -o Whisper-MacOs.pkg $WHISPER_VAMP_URL/$WHISPER_VAMP_VERSION/Whisper-MacOs.pkg
    echo -e '\033[0;34m' "Done"
    echo -e '\033[0m'

    echo -e '\033[0;34m' "Installing Partiels and plugins..."
    echo -e '\033[0m'
    MOUNT_DIR=$(hdiutil attach Partiels-MacOS.dmg | grep Volumes | awk '{print $3}')
    rm -rf "/Applications/Partiels.app"
    sudo cp -rf "$MOUNT_DIR/Partiels.app" /Applications/
    hdiutil detach "$MOUNT_DIR" -quiet
    unzip Ircam-Vamp-Plugins-MacOS.zip
    sudo installer -pkg "Ircam Vamp Plugins.pkg" -target /
    unzip VAX-Vamp-Plugin-v$VAX_VAMP_VERSION-MacOS.zip
    sudo installer -pkg VAX-Vamp-Plugin-MacOS.pkg -target /
    sudo installer -pkg Crepe-MacOs.pkg -target /
    sudo installer -pkg Whisper-MacOs.pkg -target /
    echo -e '\033[0;34m' "Done"
    echo -e '\033[0m'

    rm -rf "$TEMP_DIR"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    TEMP_DIR=$(mktemp -d)
    echo -e '\033[0;34m' "Temporary directory created at: $TEMP_DIR"
    echo -e '\033[0m'
    cd "$TEMP_DIR" || exit 1

    echo -e '\033[0;34m' "Downloading Partiels and plugins..."
    echo -e '\033[0m'
    wget -q $PARTIELS_URL/$PARTIELS_VERSION/Partiels-Linux.tar.gz
    wget -q $IRCAM_VAMP_URL/$IRCAM_VAMP_VERSION/Ircam-Vamp-Plugins-Linux.zip
    wget -q $IRCAM_VAMP_URL/$IRCAM_VAMP_VERSION/VAX-Vamp-Plugin-v$VAX_VAMP_VERSION-Linux.zip
    wget -q $CREPE_VAMP_URL/$CREPE_VAMP_VERSION/Crepe-Linux.tar.gz
    wget -q $WHISPER_VAMP_URL/$WHISPER_VAMP_VERSION/Whisper-Linux.tar.gz
    echo -e '\033[0;34m' "Done"
    echo '\033[0m'

    echo -e '\033[0;34m' "Installing Partiels and plugins..."
    echo -e '\033[0m'
    mkdir -p $HOME/vamp $HOME/.config/Ircam
    tar -xzf Partiels-Linux.tar.gz
    sh Partiels/Partiels-install.sh
    unzip Ircam-Vamp-Plugins-Linux.zip
    sh Ircam-Vamp-Plugins-Linux/Install.sh
    unzip VAX-Vamp-Plugin-v$VAX_VAMP_VERSION-Linux.zip
    tar -xzf VAX-Vamp-Plugin-Linux.tar.gz
    sh VAX-Vamp-Plugin/Install.sh
    tar -xzf Crepe-Linux.tar.gz
    sh Crepe/Install.sh
    tar -xzf Whisper-Linux.tar.gz
    sh Whisper/Install.sh
    echo -e '\033[0;34m' "Done"
    echo -e  '\033[0m'

    rm -rf "$TEMP_DIR"
else
    echo -e '\033[0;31m' "Unsupported OS: $OSTYPE"
    echo -e '\033[0;31m' "This script is intended for macOS or Linux only."
    echo -e '\033[0m'
    exit 1
fi
