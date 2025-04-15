# Advanced Port Scanner Tool

## Overview

The **Advanced Port Scanner** is a Python-based tool designed to scan IP addresses or domains for open ports. It supports multiple port scanning techniques (connect and SYN) and attempts to retrieve service banners from open ports to help identify running services.

The tool is interactive and provides an easy-to-use command-line interface (CLI) that lets you scan specific IPs or domains for open ports within a defined range. It also stores the results in a text file for later analysis.

## Features

- Interactive CLI for scanning IPs/domains and port ranges.
- Two scan types: `connect` and `SYN`.
- Attempts to grab banners from open ports to identify services.
- Saves results to a `scan_results.txt` file.

## Requirements

To use this tool, you need Python installed on your system. This tool also requires the `colorama` package for coloring the terminal output.

1. **Python version**: Python 3.x

2. **Dependencies**: You can install the required dependencies using:

   ```bash
   pip install -r requirements.txt
