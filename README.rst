TiktokScraper
=============

Introduction
------------
With this package you can collect TikTok videos, comments and user information, perform keyword search and collect the followers, followings and videos of a user.

Half of the packages (collect video metadata, collect comments, collect user information) works with simple requests. You do not need a TikTok profile for this.

The other half of the package (perform keyword search and collect the followers, followings and videos of a user) works with Selenium. For this, you need to have a Chrome browser installed and you need a TikTok profile, so you can login to the platform. This part will work a bit slower to prevent getting blocked.

Prerequisites
-------------
To install the package, execute the following command::

    $ pip install git+https://github.com/jpfefferlab/tiktokscraper.git

If you want to execute the selenium functions, we recommend you to install any chrome browser on your system first. By this, the start_selenium-function will not use a test browser, but a normal chrome browser, which prevents many troubles when collecting data on TikTok.

To use the TiktokScraper in a project, put the following command in your python script::

    import tiktokscraper

To see how to use the package, you can run the `example.py` script located in the root directory.

License
-------
This project is licensed under the MIT License - see the LICENSE file for details.

Contributions
-------------
This package was developed by Angelina Voggenreiter (angelina.voggenreiter@tum.de) as part of the research project 'Understanding, Detecting, and Mitigating Online Misogyny Against Politically Active Women' at the Technical University of Munich. This research project is funded by the Bavarian Research Institute for Digital Transformation (bidt), an institute of the Bavarian Academy of Sciences and Humanities. A special thanks goes to our collaborator Rafael Giebisch, whose contributions have helped advance our understanding of TikTok's structure. 