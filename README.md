# neo

### Description
neo - New Events Officer (No Events Officer?)

This is a little tool I hope to develop steadily over the next little while. While the title is a joke, it should be able to perform most of the tasks an Events Officer does in Redbrick.

__Important:__ If you aren't a 'Team Member' on the Redbrick Facebook, this won't work for you. Same applies for the calendar.

---

### Installation

- #### On your own machine:
    - Clone this repo by running:
    ```git clone https://github.com/theycallmemac/neo.git```
    - cd into the clone and run ```python3 setup.py install``` as root to install.

---

### Usage
After installation simply run something like:

```neo LG26 15:00 16:00 10/3/2018```

---

### Dependencies
- click==6.7
- selenium==3.9.0
- pyyaml==3.12.0
- geckodriver==0.20.0 / chromedriver==2.x.0
- firefox==59.0.0 / chrome==65.0.0

### What it can do
The main aim of this program is to perform Facebook event creation, Google Calendar event creation, and event location booking. This will be done use the ```concurrent.futures``` library.

So far the tool can:

- [x] create Facebook events
- [x] create Google Calendar events
- [x] book rooms for the event

---

Probably will be best when used with [dcurooms](https://github.com/theycallmemac/dcurooms).
