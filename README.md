# Lena

Lena was designed to be a simple library for Dex manipulation. It was written in order to assist Ronin, by modifying APK's main method in order to include Ronin's shared library.

## Implementation

Lena is heavily relying on [Androguard](https://github.com/androguard/androguard) library in order to parse APK files and various Dex objects. The usage of Androguard was meant to be temporary solution to the release of a stable POC.
The implementation of the Writer class responsible for rebuilding the modified .dex file is mimicking the [dexgen](https://android.googlesource.com/platform/dalvik/+/master/dexgen/src/com/android/dexgen) project from Android's official repository.

### Bugs

The project was never finished due to limited free time. It should be noted that, it is certain to have bugs, logic errors, late night ranting commit messages and not recommended pythonic implementations of things.

## Acknowledgments
[rotlogix](https://github.com/rotlogix) for actually reviewing an early idea of Ronin and prompting me to *actually* begin writing Lena.
