# bgfx-conan

bgfx conan recipe (currently windows only).

## Feature
- Build bgfx with Genie with options

# Usage
- Windows:
  - Ensure that VS is installed
    - 2019 (tested)
    - 2017 (untested)
  - Use the command below to use it locally
    - conan create . bgfx/2021.03.22@\<user\>/\<channel\>
  - Add the require to the conanfile.txt or conanfile.py
