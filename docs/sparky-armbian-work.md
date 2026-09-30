# Sparky Armbian and SparkyDroid engineering

Reviewed 30 September 2026 by Codex, with Daniel Campos Ramos as project owner
and physical-test lead. This is a public-safe summary of Daniel's owner-held
implementation and test records, not a firmware
download, independent hardware certification or upstream-acceptance announcement.

The project demonstrates **embedded platform engineering across Android and
Linux**, not simply collecting or installing Armbian images. Its core work spans
application interfaces, native ports, audio framework/HAL integration, display
transactions, firmware composition and recovery. Several baselines are installed
and physically tested; newer derivatives retain their own acceptance gates.

Daniel supplies direction, hardware access, integration decisions and hands-on
acceptance. AI partners contribute implementation, investigation and review;
their individual roles stay in the project records. Upstream foundations remain
credited, rather than being presented as original work by this project.

## Evidence and scope

This review followed source, build records, deployment/readback receipts and later
owner observations, rather than treating the root README or an older pending
checklist as the final state. It did not reflash devices or repeat historical
hardware tests. A small host-side Java regression was freshly compiled and run,
as recorded below.

The evidence labels mean:

- **Proven in the reviewed records:** source/build checks or recorded device
  readbacks establish the stated result within their test scope.
- **Owner-confirmed:** Daniel observed the behavior physically; this is not
  automatically an instrumented measurement.
- **Qualified:** implemented or built, but broader compatibility or final
  acceptance still needs testing.
- **Experimental:** a proposed extension or a successor without its required
  live acceptance. This label does not demote an already accepted predecessor.

These are descriptions of project evidence, not third-party certification.
Private receipts remain owner-held; readers cannot independently reproduce a
claim from this summary alone.

## Working device baselines

| Device lane | Implemented and accepted in the reviewed records | Separate remaining boundary |
| --- | --- | --- |
| Rockchip RK3228A TV box | Personal R6 installed, bounded readbacks matched, two boots passed, and Daniel accepted Sony OSD, input and audio behavior. Capability-gated RGB10 and float-processing/24-bit HAL state are recorded. | Newer R8 and educational derivatives are offline-qualified, not physically accepted releases. A later DSP-residency improvement is not retroactively attributed to R6. |
| Allwinner H313 T10 | Personal R22 installed with full image readback and retained userdata. FLauncher, resident JamesDSP, RGB10, warm reboot and display recovery are recorded. Daniel later confirmed full shutdown and IR power-on. | Changed-capability HDMI hotplug/quarantine still needs its separate live test. New educational images and generic frontend successors retain their own gates. |
| AC8227L automotive head unit | R6.1 completed the full OEM OTA/reset and booted. Daniel confirmed Mixer v24 continues working after its UI closes; source and earlier live tests establish the mixer/control/DSP implementation. | R6.2 remains a separately qualified package awaiting device acceptance. A final active-meter image gallery is not a prerequisite for acknowledging the already accepted service persistence. |
| Allwinner H3 Sunvell R69 | Native Android EmulationStation rendered at 1280×720, accepted digital controls worked, and native Exit completed cleanly. Golden R3.4 was installed with matching live BOOT/SYSTEM hashes and reset convergence. Linux-side frontend/core modernization was also applied. | Final shared-card save/removal/reboot lifecycle and matched-game acceptance remain. Installed candidate cores do not imply every game or controller mode was tested. |

One important continuity correction: the T10 installation receipt initially
left manual shutdown pending. The **26 August owner acceptance**, tied to the
same installed image, closes that gate. The original receipt stays immutable;
its earlier pending field is not evidence that the later test never happened.

## Android application and native engineering

**Proven implementation and bounded device acceptance:** the R69 work adapts the
RetroPie EmulationStation engine to Android ARMv7 through SDL2 and the NDK, rather
than replacing it with a superficially similar launcher. Source locks, validated
transformation anchors and package checks constrain the build. Digital-controller
input and graceful native/Android teardown have live acceptance; analog-menu
input and full game-library qualification are separate.

**Proven implementation, qualified successor:** the generic Android frontend adds
declarative storage/emulator profiles, Java setup activities, JNI and native
adapters. Its storage model separates a writable primary library from existing
readable ROM trees, canonicalizes paths and confines launches to admitted roots.
The newer merged view references game data rather than copying it. Version 0.3
was installed and launched on T10; version 0.4 has build/package/security checks
but awaits its merged-library, theme, emulator-return and removable-media tests.

**Proven implementation with recorded host and live checks:** FLauncher changes
include Dart/Flutter directional traversal and wallpaper presentation, plus Java
bridges for Android Back/Home dispatch and ROM-integrated power actions. A key
debugging result distinguished widget shortcuts from Android's actual physical
Back entry path. Regression coverage was extended after the handset test exposed
that difference. Later installed baselines carry the launcher changes; T10's
shutdown/IR acceptance is a physical result, not just a source-contract test.

This supports Java, Dart, Flutter, C/C++, SDL2 and NDK/JNI project-work badges.
It does not imply sole authorship of inherited engines or fluent independent
implementation of every language present in an upstream tree.

## Audio engineering across the whole chain

**Proven implementation:** Head Unit Mixer combines guarded hardware-control
resolution, diagnostic parsing, DSP presets, meters and a persistent Android
service. Its preset transaction captures the previous state, applies both
targets, verifies readback and attempts bounded rollback on failure. DSP control
does not silently take ownership of unrelated analog/master controls.

**Owner-confirmed listening result:** the head-unit gain-staging investigation
identified the physical analog device instead of trusting a misleading driver
label. Daniel reported the corrected hiss/level behavior. This is useful
hardware diagnosis, but not a laboratory noise-floor or distortion measurement.

**Proven in captured software state:** a September T10 comparison held the device
and source file constant while comparing a stock VLC engine with the HiFi
variant. The latter used float output, float resampling and Android float writes;
the captured track, HAL and ALSA states distinguish that path from the control's
earlier 16-bit conversion. Daniel separately confirmed audible HDMI playback.
The captured output remained 48 kHz: neither native 96 kHz nor bit-perfect
playback is claimed.

Internal float precision, HAL/ALSA sample format, electrical transport and a
DAC's effective performance are different facts. The head unit's accepted
speaker edge remains PCM16; it must not inherit the T10's 24-bit transport claim.
Likewise, a software-format readback does not measure converter resolution.

## Display transactions and firmware integration

**Proven source and live recovery:** the T10 C controller admits display changes
from parsed sink capabilities, captures a stable baseline, journals transition
phases and verifies active state against both hardware/sysfs and the vendor
active-mode interface. A live test killed the watcher while 3D was active. Its
replacement recovered the recorded baseline before polling again: RGB10 was
restored and the journal cleared. This is stronger than relying on an exit trap
that cannot execute after `SIGKILL`.

The recorded transition uses YCbCr 4:4:4 8-bit frame packing, then restores RGB
10-bit 2D. **It is not a simultaneous 3D-plus-10-bit result.** The separate nouveau
12-bpc/3D bench work is described in the
[BRAVIA project](https://github.com/danielcamposramos/sony-bravia-linux).

**Experimental extension:** a newer automatic VLC metadata-to-ROM signalling
contract is designed but not built in the reviewed record. That is a successor
to an existing title-triggered display path, not evidence that the native display
controller or its tested recovery is only an idea.

**Proven implementation with bounded deployment:** firmware work includes fixed
partition geometry, restricted image/filesystem mutations, installed-form APK
integration, independent unpack verification, exact target ledgers and rollback
tuples. Forward device-family admission and exact installed-target rollback are
distinct contracts. These installers and recovery records support firmware
integration and reverse-engineering experience, not universal flash safety or
unrestricted compatibility with similarly named retail devices.

## Fresh host regression

On 30 September, Codex compiled the current `MixerPreset`, `PresetTransaction`
and `PresetTransactionTest` Java sources with `javac 17.0.15` in an isolated
host build directory.
`PresetTransactionTest: PASS` covered successful commit, DSP failure rollback,
meter failure rollback and readback-mismatch rollback. No Android device was
accessed. This is a fresh test of transaction logic, not a fresh meter, DSP-engine
or physical-audio acceptance test.

The reviewed source SHA-256 values are:

| Source | SHA-256 |
| --- | --- |
| `MixerPreset.java` | `84b1e0fc3a0e34af8572d8a60c83dc698d60fa0ed290469278b9bf47131f8907` |
| `PresetTransaction.java` | `73f33ac7856f6be2365b43d1103bc81aac800c7c0e927bf48a64d2aa00e1b6e5` |
| `PresetTransactionTest.java` | `f67569b6b829fa2d8467f8fb87e242865a1f1bef15d48d7f05268ffd3b2e23b9` |

## Attribution and publication

The reviewed private inventory includes the live-state record, lane cards,
FLauncher source/tests and upstream-delta audit, Head Unit Mixer source/tests and
live-acceptance report, T10 controller source and watcher-death recovery record,
T10 installation and later shutdown acceptance, R69 native-port/Golden records,
generic frontend implementation, educational-image composition records and the
September VLC stock-control comparison. Some older component summaries still
carry pending states superseded by later receipts.

Foundations include Android/AOSP, Armbian/RetrOrangePi, RetroPie/EmulationStation,
RetroArch, SDL, FLauncher and its maintainers, JamesDSP, VLC/VideoLAN and SoXR.
The project contributes adaptations, integration, diagnostics, safety contracts
and testing; it does not claim to have originated those upstream projects.

Public forks and repository placeholders are not evidence that these current
local changes have been published or merged upstream. Full firmware archives,
signing material, device identities, personal content and third-party application
bytes remain private. Public source/delta releases require their own provenance,
privacy and licensing review. This summary publishes none of those artifacts.

The professional conclusion is **cross-layer embedded platform work with real
device feedback**. Remaining successor gates limit specific releases; they do
not erase the implemented and tested core ideas.
