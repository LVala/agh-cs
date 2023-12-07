#ifndef __SYNTH_H
#define __SYNTH_H

#include <math.h>
#include <stdint.h>
#include "i2s.h"
#include "stm32f4xx_hal.h"
#include "wavetable.h"

extern Wavetable_State wavetable;

#define POLY_MAX 3
#define AUDIO_BUFFER_FRAMES   128
#define AUDIO_BUFFER_CHANNELS 2
#define AUDIO_BUFFER_SAMPLES AUDIO_BUFFER_FRAMES * AUDIO_BUFFER_CHANNELS

void Synth_Init(void);
uint8_t Synth_Play(void);
void Synth_NoteOn(uint8_t midi_param0, uint8_t midi_param1);
void Synth_NoteOff(uint8_t midi_param0, uint8_t midi_param1);

#endif
