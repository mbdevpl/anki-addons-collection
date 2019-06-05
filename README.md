# Anki addons collection

Written by various authors, collected by Mateusz Bysiek 2018-2019


## How to use

1. Check what operating system are you using. Linux? Mac?

2. Check your Anki version. Are you using v2.0 or v2.1?

3. Navigate to Anki addons folder.

  Linux, Anki v2.0: ```cd "${HOME}/Documents/Anki/addons"```

  Linux, Anki v2.1: ```cd "${HOME}/.local/share/Anki2/addons21"```

  Mac, Anki v2.0: ```cd "${HOME}/Library/Application Support/Anki2/addons"```

  Mac, Anki v2.1: ```cd "${HOME}/?"```

4. Clone this repository there:

  ```
  git clone --recursive https://github.com/mbdevpl/anki-addons-collection .
  ```

5. See list of available addons:

  ```
  python activate_addons.py
  ```

6. Create a file named `active_addons.json`. You can simply copy an example file and modify it.

   ```
   cp active_addons_example.json active_addons.json
   ```

7. Launch Anki and your configured addons will be automatically loaded.


## Extra tip

If you'd like to keep your active addons in sync as much as possible across multiple devices you use,
you can fork my repository and add your `active_addons.json` there,
or alternatively you might just setup your file synchronization software to synchronize
the whole Anki addons directory.

It will work because addons loader in this repository works with Anki 2.0 as well as 2.1
and will not load incompatible addons.
