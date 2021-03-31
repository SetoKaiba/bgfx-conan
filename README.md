# bgfx-conan

bgfx conan recipe (currently Windows & Macos x64 only).

## Feature
- Build bgfx with Genie with options

# Usage
- Use the command below to use it locally(version can be found in conandata.yml)
  - conan create . bgfx/\<version>@\<user\>/\<channel\>
  - Add the require to the conanfile.txt or conanfile.py
- Windows
  - Ensure that VS is installed
    - 2019 (tested)
    - 2017 (untested)
- Macos
  - Initial support for Macos x64 (untested)
