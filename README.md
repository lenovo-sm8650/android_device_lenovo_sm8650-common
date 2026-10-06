# Lenovo SM8650 common tree

Common configuration for Lenovo devices on the Qualcomm Snapdragon 8 Gen 3
(SM8650, pineapple), used by the Lenovo Yoga Tab Plus (lapis, TB520FU):
board configuration, platform blobs (proprietary_vendor_lenovo_sm8650-common),
Qualcomm init scripts and fstab, recovery, VINTF and the GKI kernel
(kernel/lenovo/sm8650).

Device trees include BoardConfigCommon.mk and inherit common.mk; their
extract-files.py extracts both blob lists with device_with_common.
