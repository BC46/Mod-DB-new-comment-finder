# Mod DB new comment finder
Web scraper that finds new comments across numerous Mod DB comment sections and pages.

## The problem
Mods listed on Mod DB often have numerous pages with comment sections where users can leave comments. These are usually articles, home pages, and download pages. One issue is that Mod DB's page layout isn't the most user friendly because comments are often simply shown on top of each other without much structure. It's also never clear what the comment section pagination exactly represents. Worst of all is that mod owners don't actually get notified whenever a user comments on one of those pages.
As a result, mod owners have to reguarly view all their comment sections and pages to see if new comments have been posted, which is very inconvenient.

## The solution
This repository contains a Python web scraper that automatically finds comments that have been posted in the past hour. Every 45 minutes, it checks all given comment sections and even paginates through all of them. If a recent comment has been found, it'll show what was posted, by who, and on which page it was found.

The web scraper is a simple Proof of Concept that by default looks at pages from the Freelancer: HD Edition mod. However, this can be edited so the scraper will look at other pages. Additionally, this scraper can be integrated into a Discord bot or custom notification system for example. This'll ensure that mod owners can view and/or reply to new comments as soon as possible.
