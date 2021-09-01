# kaniwani-runner
Endless runner game for Wanikani content


# Apple Silicon

The sound does not work on Apple Silicon as well as Kivy 2.0 makes issues. Perform the steps below.

```
xcode-select --install
brew install gst-plugins-bad
brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
# In your virtualenv
python -m pip install "kivy[base] @ https://github.com/kivy/kivy/archive/master.zip"
```
