# Jupyter notebooks for testing some Twitter data collection tools

This repository contains a set of interactive [*Jupyter Notebooks*](https://jupyter.org/) that allow you to try out some of data collection tools for Twitter without the need to install anything on your own computer.

**To access the notebooks simply click the "Launch Binder" button below.** 
This will open a [Jupyter Lab environment](https://jupyterlab.readthedocs.io/en/stable/) in your browser (**NB**: This might take a moment to load).

*Note:* If you are interested in how this works: The tools behind this are [*GESIS Notebooks*](https://notebooks.gesis.org/) and [*Binder*](https://mybinder.org/).

[![Binder](https://notebooks.gesis.org/binder/badge_logo.svg)](https://notebooks.gesis.org/binder/v2/gh/jobreu/twitter-linking-workshop-2021/main?urlpath=lab)

If you have not worked with *Jupyter Notebooks* before, you can check out how to use them by opening the `jupyter_intro.ipynb` file in the *Jupyter Lab environment* that will open in your browser. Otherwise, you can launch one of the other notebooks (i.e, open one of the `.ipynb` files by double-clicking it in the explorer view on the left-hand side) to try out the `R` packages [`rtweet`](http://rtweet.info/) and [`vosonSML`](https://github.com/vosonlab/vosonSML), the [`tweepy`](https://www.tweepy.org/) library for `Python` as well as custom `R` and `Python` functions for retrieving data from the [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api/early-access).

In order to use `rtweet`, `vosonSML`, and `tweepy` you need to have created a Twitter application which requires a [Twitter developer account](https://developer.twitter.com/en/apply-for-access). Once you have done so, you can find the necessary information in the *Keys & Tokens* menu for your app. If you need some guidance or a reminder regarding how to get that information, you can have a look at the documentation of the `rwteet` package which has a [section on this topic](https://rtweet.info/articles/auth.html). Keep in mind, though, that the layout of the Twitter developer pages might change.

For using the custom `R` and `Python` functions for retrieving data from the Twitter API, you need to apply for the [Academic Research product track](https://developer.twitter.com/en/solutions/academic-research/products-for-researchers), and create an app for that.

**NB**: The *GESIS Notebooks* project that you can access via the "Launch Binder" button is only meant for demonstration purposes. It should not be used for actually collecting data. If you want to use (code from) the notebooks to collect your own data, please download the notebook(s) and run them locally on your machine (or your own server). The easiest way to run and create *Jupyter Notebooks* on your local machine is installing and using [*Anaconda*](https://www.anaconda.com/products/individual).

Also note that any changes you make to the files in the *GESIS Notebooks* project are not persistent and will be lost at the end of your user session. If you want to keep the changes you made, you can either download the files and continue to use them locally or create/use a user account by clicking on *Login* or *Try it now* and then on *You are not yet registered?* on the [*GESIS Notebooks* website](https://notebooks.gesis.org/). In addition to being able to save their changes, authenticated users also get allocated more memory for the virtual machine and have a longer inactivity timeout limit (see the [*GESIS Notebooks* FAQ](https://notebooks.gesis.org/faq/)).

## License for the notebooks in this repository
[![Creative Commons Lizenzvertrag](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/)