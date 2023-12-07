#ifndef __CODEC_H
#define __CODEC_H


#include "stm32f4xx_hal.h"
#include "i2c.h"

#define CODEC_STANDARD 0x04

#define AUDIO_MUTE_ON  1
#define AUDIO_MUTE_OFF 0

#define AUDIO_MUTE_ON  1
#define AUDIO_MUTE_OFF 0

#define OUTPUT_DEVICE_HEADPHONE 0xAF

#define I2C_MAX_TIMEOUT   0xA000

#define CODEC_I2C_ADDR    0x94

#define CODEC_RESET_Pin        GPIO_PIN_4
#define CODEC_RESET_GPIO_Port  GPIOD

/** CS43l22 Registers  ***/
#define   CODEC_REG_ID                  0x01
#define   CODEC_REG_POWER_CTL1          0x02
#define   CODEC_REG_POWER_CTL2          0x04
#define   CODEC_REG_CLOCKING_CTL        0x05
#define   CODEC_REG_INTERFACE_CTL1      0x06
#define   CODEC_REG_INTERFACE_CTL2      0x07
#define   CODEC_REG_PASSTHR_A_SELECT    0x08
#define   CODEC_REG_PASSTHR_B_SELECT    0x09
#define   CODEC_REG_ANALOG_ZC_SR_SETT   0x0A
#define   CODEC_REG_PASSTHR_GANG_CTL    0x0C
#define   CODEC_REG_PLAYBACK_CTL1       0x0D
#define   CODEC_REG_MISC_CTL            0x0E
#define   CODEC_REG_PLAYBACK_CTL2       0x0F
#define   CODEC_REG_PASSTHR_A_VOL       0x14
#define   CODEC_REG_PASSTHR_B_VOL       0x15
#define   CODEC_REG_PCMA_VOL            0x1A
#define   CODEC_REG_PCMB_VOL            0x1B
#define   CODEC_REG_BEEP_FREQ_ON_TIME   0x1C
#define   CODEC_REG_BEEP_VOL_OFF_TIME   0x1D
#define   CODEC_REG_BEEP_TONE_CFG       0x1E
#define   CODEC_REG_TONE_CTL            0x1F
#define   CODEC_REG_MASTER_A_VOL        0x20
#define   CODEC_REG_MASTER_B_VOL        0x21
#define   CODEC_REG_HEADPHONE_A_VOL     0x22
#define   CODEC_REG_HEADPHONE_B_VOL     0x23
#define   CODEC_REG_SPEAKER_A_VOL       0x24
#define   CODEC_REG_SPEAKER_B_VOL       0x25
#define   CODEC_REG_CH_MIXER_SWAP       0x26
#define   CODEC_REG_LIMIT_CTL1          0x27
#define   CODEC_REG_LIMIT_CTL2          0x28
#define   CODEC_REG_LIMIT_ATTACK_RATE   0x29
#define   CODEC_REG_OVF_CLK_STATUS      0x2E
#define   CODEC_REG_BATT_COMPENSATION   0x2F
#define   CODEC_REG_VP_BATTERY_LEVEL    0x30
#define   CODEC_REG_SPEAKER_STATUS      0x31
#define   CODEC_REG_TEMPMONITOR_CTL     0x32
#define   CODEC_REG_THERMAL_FOLDBACK    0x33
#define   CODEC_REG_CHARGE_PUMP_FREQ    0x34

uint32_t Codec_Init();
uint32_t Codec_Play();
uint32_t Codec_Stop();
uint32_t Codec_SetVolume(uint8_t volume);
uint32_t Codec_SetMute(uint8_t cmd);


#endif
