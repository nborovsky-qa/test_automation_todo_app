# CI configuration

## `config.yaml`

- **platform**: `android` or `ios`. Choosed by the workflow (from this file or manual run inputs).
- **device**: 
  - `any_active` – use the first connected emulator/device (in CI, the one started by the workflow).
  - Or a specific id, e.g. `emulator-5554`, `Pixel_4_API_30`, or a physical device id.

The workflow passes these as env vars (`android_deviceName` / `ios_deviceName`) and as `--platform` to pytest.

## Android APK in CI

To run tests in CI, the Todo app must be on the emulator. Either:

1. **Place an APK in the repo**: put your built `todo.apk` at `ci/todo.apk`. The workflow will install it on the connected / selected device in options. Add `ci/todo.apk` to `.gitignore` if you don’t want to commit it and use a build step or artifact instead.
2. **Pre-install elsewhere**: if the device already has the app installed, leave `ci/todo.apk` absent, no futher changes needed

## Manual run

In GitHub: **Actions → Android Todo App Tests → Run workflow**. You can override **platform** and **device** there; they otherwise come from `ci/config.yaml`.
