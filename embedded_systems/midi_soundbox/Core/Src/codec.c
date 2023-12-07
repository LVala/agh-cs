// Heavily inspired by https://github.com/STMicroelectronics/stm32-cs43l22
#include "codec.h"

#define VOLUME_CONVERT(Volume) (((Volume) > 100)? 255:((uint8_t)(((Volume) * 255) / 100)))

static uint8_t is_codec_stopped = 1;

uint8_t Codec_Write(uint8_t reg, uint8_t val) {
  HAL_StatusTypeDef status = HAL_OK;

  status = HAL_I2C_Mem_Write(&hi2c1, CODEC_I2C_ADDR, reg, I2C_MEMADD_SIZE_8BIT, &val, 1, I2C_MAX_TIMEOUT);

  return status != HAL_OK ? 1 : 0;
}

uint32_t Codec_Init() {
  // expects I2C already initialized

  uint32_t counter = 0;

  // power on the codec (possibely need to turn it off first)
  HAL_GPIO_WritePin(CODEC_RESET_GPIO_Port, CODEC_RESET_Pin, GPIO_PIN_SET);

  // keep codec powered off
  counter += Codec_Write(CODEC_REG_POWER_CTL1, 0x01);
  // set output device to headphone
  counter += Codec_Write(CODEC_REG_POWER_CTL2, 0xAF);
  // cloc configuration: auto detection
  counter += Codec_Write(CODEC_REG_CLOCKING_CTL, 0x81);
  // set slave mode and audio standard
  counter += Codec_Write(CODEC_REG_INTERFACE_CTL1, 0x07);
  // set master volume to 0
  counter += Codec_SetVolume(0);

  // additional configuration, refer to link at the top of the file
  counter += Codec_Write(CODEC_REG_ANALOG_ZC_SR_SETT, 0x00);
  counter += Codec_Write(CODEC_REG_MISC_CTL, 0x04);
  counter += Codec_Write(CODEC_REG_LIMIT_CTL1, 0x00);
  counter += Codec_Write(CODEC_REG_TONE_CTL, 0x0F);
  counter += Codec_Write(CODEC_REG_PCMA_VOL, 0x0A);
  counter += Codec_Write(CODEC_REG_PCMB_VOL, 0x0A);

  return counter;
}

uint32_t Codec_Play() {
  uint32_t counter = 0;

  if (is_codec_stopped) {
    // enable the digital soft ramp
	counter += Codec_Write(CODEC_REG_MISC_CTL, 0x06);
	counter += Codec_SetMute(AUDIO_MUTE_OFF);
	// power on the codec
	counter += Codec_Write(CODEC_REG_POWER_CTL1, 0x9E);
  }

  return counter;
}

uint32_t Codec_Stop() {
  uint32_t counter = 0;

  counter += Codec_SetMute(AUDIO_MUTE_ON);
  // disable digital soft ramp
  counter += Codec_Write(CODEC_REG_MISC_CTL, 0x04);
  // power down the DAC and the speaker
  counter += Codec_Write(CODEC_REG_POWER_CTL1, 0x9F);

  return counter;
}

uint32_t Codec_SetVolume(uint8_t volume) {
  uint32_t counter = 0;
  uint8_t converted_vol = VOLUME_CONVERT(volume);

  if (converted_vol > 0xE6) {
    counter += Codec_Write(CODEC_REG_MASTER_A_VOL, converted_vol - 0xE7);
	counter += Codec_Write(CODEC_REG_MASTER_B_VOL, converted_vol - 0xE7);
  } else {
	counter += Codec_Write(CODEC_REG_MASTER_A_VOL, converted_vol + 0x19);
	counter += Codec_Write(CODEC_REG_MASTER_B_VOL, converted_vol + 0x19);
  }

  return counter;
}

uint32_t Codec_SetMute(uint8_t cmd) {
  uint8_t counter = 0;

  if (cmd == AUDIO_MUTE_ON) {
    counter += Codec_Write(CODEC_REG_POWER_CTL2, 0xFF);
    counter += Codec_Write(CODEC_REG_HEADPHONE_A_VOL, 0x01);
    counter += Codec_Write(CODEC_REG_HEADPHONE_B_VOL, 0x01);
  } else {
	counter += Codec_Write(CODEC_REG_POWER_CTL2, OUTPUT_DEVICE_HEADPHONE);
    counter += Codec_Write(CODEC_REG_HEADPHONE_A_VOL, 0x00);
    counter += Codec_Write(CODEC_REG_HEADPHONE_B_VOL, 0x00);
  }

  return counter;
}
