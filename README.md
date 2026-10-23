# Lenovo SM8650 common tree (LineageOS 24)

Plain LineageOS 24 (lineage-24.0) common tree for Lenovo devices on the
Qualcomm Snapdragon 8 Gen 3 (SM8650, pineapple), used by the Lenovo Yoga Tab
Plus (lapis, TB520FU).

It contains the board configuration, the Qualcomm init scripts and fstab,
recovery, VINTF manifests, the USB composition list and the hardware HAL
packages (audio, Bluetooth, camera, display, media, KeyMint/StrongBox, WiFi).
It has no Lenovo applications, overlays or vendor-specific framework changes.

Proprietary blobs come from proprietary_vendor_lenovo_sm8650-common and the
GKI kernel from kernel/lenovo/sm8650. Device trees include
BoardConfigCommon.mk and inherit common.mk; their extract-files.py extracts both
blob lists with device_with_common.
