# kaniwani-runner
Endless runner game for Wanikani content


# Apple Silicon

The sound does not work on Apple Silicon as well as Kivy 2.0 makes issues. Perform the steps below.

```
brew install gst-plugins-bad
# In your virtualenv
python -m pip install "kivy[base] @ https://github.com/kivy/kivy/archive/master.zip"
```
