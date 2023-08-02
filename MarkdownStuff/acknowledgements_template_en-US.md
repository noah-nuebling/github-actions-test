<details>
  <summary>󠁧󠁿{current_language}</summary>
  
{language_list}
  [Help translate Mac Mouse Fix to different languages!](https://google.com)
</details>

# Acknowledgements

Big thanks to any one using Mac Mouse Fix / and giving feedback! Y'all are what makes this fun / what keeps me going!

I want to especially thank these people:

## Translations 🌏

Thanks for bringing Mac Mouse Fix ppl **around the globe**!

- 🇨🇳 Chinese translation: [@groverlynn](https://github.com/groverlynn)

## Money 💰


### Very Generous Contributors 🚀

These people bought me an **Incredible Milkshake**. Thanks for the _sugar rush_! 

{very_generous}

### Generous Contributors ⭐️

These people **paid more** for Mac Mouse Fix than the base price. Thanks for your _support_!

{generous}

### Other

Thanks also to everyone else who bought me a milkshake and to all {sales_count} people who bought Mac Mouse Fix! Ya'll are the bomb. Thanks to you I can spend lots of time on sth I love doing.

## Other software 👾

__Apps__ that inspired Mac Mouse Fix:

- [SteerMouse](https://plentycom.jp/en/steermouse/index.html) - The OG mouse software for Mac. Inspiration for many features. I often thought "this is is probably not possible" but then I saw "oh SteerMouse does it" and then 3 years later I figured out how to do it, too.
- [Calftrail Touch](https://github.com/calftrail/Touch) - Basis for "reverse engineering" work powering MMFs best-in-class and first-of-a-kind touch simulation!
- [SensibleSideButtons](https://github.com/archagon/sensible-side-buttons) - Basis for early implementation of Back and Forward feature. Made me find Calftrail Touch?
- [SmoothMouse](https://smoothmouse.com/) - It's creator [Dae](https://dae.me/) answered some important questions for me about Pointer Speed 
- [Gifski by sindresorhus](https://github.com/sindresorhus/Gifski) - Greatly inspired the Mac Mouse Fix README.md
- MOS - Inertial Scrolling feel, App-Specific Settings Implementation and more were inspired by the MOS

__People__ that inspired Mac Mouse Fix:

- @DrJume for teaching me about debouncing and inspiring the UI for entering and displaying keyboard modifiers on the scroll tab
- German guy for inspiring the tab-based layout in MMF 3
- Guy who helped tune the fast scrolling in that pull request
- So many others I can't think of right now. Thanks to everybody else who shared their thoughts!

Mac Mouse Fix was built with the help of these **great libraries**:

- [ReactiveSwift](https://github.com/ReactiveCocoa/ReactiveSwift) - Streams of values over time. Tailored for Swift.
- [CocoaLumberjack](https://github.com/CocoaLumberjack/CocoaLumberjack) - Fast & simple, yet powerful & flexible logging
- [Swift Markdown](https://github.com/apple/swift-markdown) - Parse, build, edit, and analyze Markdown documents
- [BartyCrouch](https://github.com/FlineDev/BartyCrouch) - Keep translation files in sync with Source Code and Interface Builder files
- [Sparkle](https://github.com/sparkle-project/Sparkle) - A software update framework for macOS
- [SnapKit](https://github.com/SnapKit/SnapKit) - Making Auto Layout easy on both iOS and OS X
- [MASShortcut](https://github.com/shpakovski/MASShortcut) - API and user interface for recording, storing and using system-wide keyboard shortcuts -> Using this to display keyboard keys in the UI.
- [CGSInternal](https://github.com/NUIKit/CGSInternal) - A collection of private CoreGraphics routines -> used for all sorts of stuff Mac Mouse Fix does.

---

# To build this

- Dynamic readme: 
  - https://github.com/marketplace/actions/dynamic-readme
  - https://github.com/bitflight-devops/github-action-readme-generator
  - https://github.com/marketplace/actions/generate-update-markdown-content
  - https://github.com/marketplace/actions/github-readme-generator
  - > F this I'll just write a simple pythin script that takes a template as format string and then generates this. Maybe run it periodically using github actions
