# kaniwani-runner
Endless runner game for Wanikani content


# Apple Silicon

The sound does not work on Apple Silicon as well as Kivy 2.0 makes issues. Perform the steps below.

```bash
xcode-select --install
brew install gst-plugins-bad
brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
# In your virtualenv
python -m pip install "kivy[base] @ https://github.com/kivy/kivy/archive/master.zip"
```

## Using the Kivy.app environment

Download and open the [DMG](https://kivy.org/downloads/ci/osx/app/Kivy.dmg)
Drag the Kivy.app to Applications

Execute the following.

```bash
pushd /Applications/Kivy.app/Contents/Resources/venv/bin
source activate
source kivy_activate
popd
pip install -U setuptools pip
pip install -Ur requirements/requirements.txt
```
