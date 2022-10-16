# subot - Automated Course Registerer for Sabanci University

## Introduction
Course registration periods in Sabanci University can be painful, especially if you could not login in time due to high loads on servers and had to check for an available seat for an already full class for 5 days, by hand. subot is designed to eliminate and automate this time consuming process.

## What does it do?
Using Google Chrome installed on your computer:

- tries to login to the site and register desired classes
- checks the number of available seats in the course until a space is available, on the possibility that anyone who has successfully taken the course will drop out, then, immediately, fills the space

## Built with

- [Python](https://www.python.org) - A powerful scripting language
- [Qt Creator](https://www.qt.io/product/development-tools) - An app for interface design
- [PyQt5](https://pypi.org/project/PyQt5/) - GUI library for Python
- [Selenium](https://www.selenium.dev/documentation/) - A library for browser automation
- [PyInstaller](https://pyinstaller.org/en/stable/) - A library for creating executable Python apps

## Installation

- Click <a id="raw-url" href="https://raw.githubusercontent.com/mustafaaycll/sabanci-adddropbot/main/release_AppleSilicon/subot.dmg">here</a> if you use an ARM Mac (M1, M1 Pro, M1 Max, M2)
- Click <a id="raw-url" href="https://raw.githubusercontent.com/mustafaaycll/sabanci-adddropbot/main/release_IntelSilicon/sorry.txt">here</a> if you use an Intel Mac
- There is no MS Windows version, feel free to copy and modify the code to develop one.
