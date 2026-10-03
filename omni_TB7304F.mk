#
# Copyright (C) 2026 The Android Open Source Project
#
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base.mk)

# Inherit some common Omni stuff.
$(call inherit-product, vendor/omni/config/common.mk)

# Inherit from TB7304F device
$(call inherit-product, device/lenovo/TB7304F/device.mk)

PRODUCT_DEVICE := TB7304F
PRODUCT_NAME := omni_TB7304F
PRODUCT_BRAND := Lenovo
PRODUCT_MODEL := Lenovo TB-7304F
PRODUCT_MANUFACTURER := LENOVO
